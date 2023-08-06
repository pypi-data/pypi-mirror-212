# SPDX-License-Identifier: MIT
"""Tag Heuer/Chronelec Decoder Interface."""

# todo: handle man, box, and cel combinations:
#	CELL1   <STA 000255 00:00'31"957 01 01 1 1555>
#	CELL2   <BOX 000255 00:01'32"663 01 01 1 1552>
#	MAN     <MAN 000000 00:18'16"964 01 01 1 1541>
#	box L   <B01 093367 03:45'08"388 44 01 0 1522>
#	box R   <B02 093367 03:45'53"976 74 01 0 1529>
#	box Cel <B01 000255 03:47'07"566 00 01 0 1497>

# For connections to multiple decoders, use thbchub

import Queue
import logging
import serial
import socket
import time

from . import (decoder, DECODER_LOG_LEVEL)
from metarace import sysconf
from metarace import tod
from libscrc import mcrf4xx

_log = logging.getLogger(u'metarace.decoder.thbc')
_log.setLevel(logging.DEBUG)

THBC_BAUD = 19200
THBC_UDP_PORT = 2008
THBC_ENCODING = u'iso8859-1'

# THbC protocol messages
ESCAPE = b'\x1b'
HELOCMD = b'MR1'
STOPCMD = ESCAPE + b'\x13\x5c'
REPEATCMD = ESCAPE + b'\x12'
ACKCMD = ESCAPE + b'\x11'

STATCMD = ESCAPE + b'\x05'  # fetch status
CHKCMD = ESCAPE + b'\x06'  # UNKNOWN
STARTCMD = ESCAPE + b'\x07'  # start decoder
SETCMD = ESCAPE + b'\x08'  # set configuration
IPCMD = ESCAPE + b'\x09'  # set IP configuration
QUECMD = ESCAPE + b'\x10'  # fetch configuration

STALVL = ESCAPE + b'\x1e'
BOXLVL = ESCAPE + b'\x1f'

NACK = b'\x07'
CR = b'\x0d'
LF = b'\x0a'
SETTIME = ESCAPE + b'\x48'
STATSTART = b'['
PASSSTART = b'<'

# decoder config consts
IPCONFIG_LEN = 16
CONFIG_LEN = 27
CONFIG_TOD = 0
CONFIG_GPS = 1
CONFIG_TZ_HOUR = 2
CONFIG_TZ_MIN = 3
CONFIG_485 = 4
CONFIG_FIBRE = 5
CONFIG_PRINT = 6
CONFIG_MAX = 7
CONFIG_PROT = 8
CONFIG_PULSE = 9
CONFIG_PULSEINT = 10
CONFIG_CELLSYNC = 11
CONFIG_CELLTOD_HOUR = 12
CONFIG_CELLTOD_MIN = 13
CONFIG_TONE_STA = 15
CONFIG_TONE_BOX = 17
CONFIG_TONE_MAN = 19
CONFIG_TONE_CEL = 21
CONFIG_TONE_BXX = 23
CONFIG_ACTIVE_LOOP = 14
CONFIG_SPARE = 25
CONFIG_FLAGS = {
    CONFIG_TOD: u'Time of Day',
    CONFIG_GPS: u'GPS Sync',
    CONFIG_TZ_HOUR: u'Timezone Hour',
    CONFIG_TZ_MIN: u'Timezone Min',
    CONFIG_485: u'Distant rs485',
    CONFIG_FIBRE: u'Distant Fibre',
    CONFIG_PRINT: u'Serial Print',
    CONFIG_MAX: u'Detect Max',
    CONFIG_PROT: u'Protocol',
    CONFIG_PULSE: u'Sync Pulse',
    CONFIG_PULSEINT: u'Sync Interval',
    CONFIG_CELLSYNC: u'CELL Sync',
    CONFIG_CELLTOD_HOUR: u'CELL Sync Hour',
    CONFIG_CELLTOD_MIN: u'CELL Sync Min',
    CONFIG_TONE_STA: u'STA Tone',
    CONFIG_TONE_BOX: u'BOX Tone',
    CONFIG_TONE_MAN: u'MAN Tone',
    CONFIG_TONE_CEL: u'CEL Tone',
    CONFIG_TONE_BXX: u'BXX Tone',
    CONFIG_ACTIVE_LOOP: u'Active Loop',
    CONFIG_SPARE: u'[spare]'
}
DEFAULT_IPCFG = {
    u'IP': u'192.168.0.10',
    u'Netmask': u'255.255.255.0',
    u'Gateway': u'0.0.0.0',
    u'Host': u'192.168.0.255'
}
DEFPORT = u'/dev/ttyS0'


def thbc_sum(msgstr=b''):
    """Return sum of character values as decimal string."""
    ret = 0
    for ch in msgstr:
        ret = ret + ord(ch)
    return '{0:04d}'.format(ret)


def val2hexval(val):
    """Convert int to decimal digit equivalent hex byte."""
    ret = 0x00
    ret |= ((val // 10) & 0x0f) << 4  # msd	97 -> 0x90
    ret |= (val % 10) & 0x0f  # lsd   97 -> 0x07
    return ret


def hexval2val(hexval):
    """Unconvert a decimal digit equivalent hex byte to int."""
    ret = 10 * (hexval >> 4)  # tens 0x97 -> 90
    ret += hexval & 0x0f  # ones 0x97 ->  7
    return ret


class thbc(decoder):
    """Tag Heuer / Chronelec thread object class."""

    def __init__(self):
        decoder.__init__(self)
        self._boxname = None
        self._version = u''
        self._decoderconfig = {}
        self._decoderipconfig = {}
        self._io = None
        self._cksumerr = 0
        self._rdbuf = b''  # bytestring read buffer

    # API overrides
    def status(self):
        """Request status message from decoder."""
        self.write(STATCMD)

    def connected(self):
        return self._io is not None and self._boxname is not None

    def stop_session(self):
        """Send a stop command to decoder."""
        self.write(STOPCMD)

    def start_session(self):
        """Send a depart command to decoder."""
        self.write(STARTCMD)

    def clear(self):
        """Start a new session and request time sync."""
        self.stop_session()
        self.start_session()
        self.sync()

    def get_config(self):
        """Request decoder configuration."""
        self.write(QUECMD)

    def ipconfig(self):
        """Request sanity check in decoder thread."""
        self._cqueue.put_nowait((u'_ipcfg', None))

    # Device-specific functions
    def _close(self):
        if self._io is not None:
            _log.debug(u'Close connection')
            cp = self._io
            self._io = None
            try:
                cp.close()
            except Exception as e:
                _log.debug(u'%s closing io: %s', e.__class__.__name__, e)

    def _port(self, port):
        """Re-establish connection to supplied device port."""
        self._close()
        s = None
        self._rdbuf = b''
        if u'/' not in port and u'.' in port:
            _log.debug(u'Attempting UDP on %r', port)
            s = dgram(port, THBC_UDP_PORT)
        else:
            # assume device file
            s = serial.Serial(port, THBC_BAUD, rtscts=False, timeout=0.2)
        self._boxname = None
        self._io = s
        self._write(QUECMD)
        # queue sane through command loop
        time.sleep(0.2)
        self.sane()

    def _sync(self, data=None):
        _log.debug(u'Performing blocking sync')
        acceptval = tod.tod(u'0.001')
        nt = tod.now()
        diff = nt - nt.truncate(0)
        while diff > acceptval and diff < tod.ONE:
            time.sleep(0.0005)
            nt = tod.now()
            diff = nt - nt.truncate(0)
        self._write(self._set_time_cmd(nt))
        _log.info(u'Set decoder time: %r', nt.meridiem())

    def _ipcfg(self, data=None):
        """Alter the attached decoder's IP address."""
        ipcfg = sysconf.get(u'thbc', u'ipconfig')
        cmd = b'\x09\x09'
        for i in [u'IP', u'Netmask', u'Gateway', u'Host']:
            if i not in ipcfg:
                ipcfg[i] = DEFAULT_IPCFG[i]
            cmd += socket.inet_aton(socket.gethostbyname(ipcfg[i]))
        _log.info(u'Attempting IP config update')
        self._v3_cmd(cmd)

    def _sane(self, data=None):
        """Check decoder config against system settings."""
        doconf = False
        if self._boxname is not None:
            if sysconf.has_option(u'thbc', u'decoderconfig'):
                oconf = sysconf.get(u'thbc', u'decoderconfig')
                for flag in self._decoderconfig:
                    key = CONFIG_FLAGS[flag]
                    if key in oconf:
                        if oconf[key] != self._decoderconfig[flag]:
                            _log.info(u'Key mismatch: %r', key)
                            self._decoderconfig[flag] = oconf[key]
                            doconf = True
        else:
            _log.info(u'Decoder not connected')

        # re-write config if required
        if doconf:
            _log.info(u'Re-configuring %r', self._boxname)
            self._set_config()

        # force decoder levels
        if sysconf.has_option(u'thbc', u'levels'):
            lvl = sysconf.get(u'thbc', u'levels')
            self._setlvl(box=lvl[0], sta=lvl[1])

    def _v3_cmd(self, cmdstr=b''):
        """Pack and send a v3 command directly to port."""
        crc = mcrf4xx(cmdstr)
        crcstr = chr(crc >> 8) + chr(crc & 0xff)  # Py2
        self._write(ESCAPE + cmdstr + crcstr + b'>')

    def _serialise_config(self):
        """Convert current decoder setting into a config string"""
        obuf = bytearray(CONFIG_LEN)
        # fill in level bytes
        obuf[CONFIG_SPARE] = 0x13  # will be fixed by subsequent levelset
        obuf[CONFIG_SPARE + 1] = 0x15

        # fill in tone values
        for opt in [
                CONFIG_TONE_STA, CONFIG_TONE_BOX, CONFIG_TONE_MAN,
                CONFIG_TONE_CEL, CONFIG_TONE_BXX
        ]:
            if opt in self._decoderconfig:
                obuf[opt] = val2hexval(self._decoderconfig[opt] // 100)  # xx00
                obuf[opt + 1] = val2hexval(self._decoderconfig[opt] %
                                           100)  # 00xx

        # fill in single byte values
        for opt in [
                CONFIG_TZ_HOUR, CONFIG_TZ_MIN, CONFIG_PROT, CONFIG_PULSEINT,
                CONFIG_CELLTOD_HOUR, CONFIG_CELLTOD_MIN
        ]:
            if opt in self._decoderconfig:
                obuf[opt] = val2hexval(self._decoderconfig[opt] % 100)  # ??

        # fill in flags
        for opt in [
                CONFIG_TOD, CONFIG_GPS, CONFIG_485, CONFIG_FIBRE, CONFIG_PRINT,
                CONFIG_MAX, CONFIG_PULSE, CONFIG_CELLSYNC, CONFIG_ACTIVE_LOOP
        ]:
            if opt in self._decoderconfig:
                if self._decoderconfig[opt]:
                    obuf[opt] = 0x01
        return bytes(obuf)

    def _set_config(self):
        """Write current configuration to decoder."""
        cmd = b'\x08\x08' + self._serialise_config()
        self._v3_cmd(cmd)
        self._write(QUECMD)

    def _set_date(self, timestruct=None):
        """Set the date on the decoder."""
        if timestruct is None:
            timestruct = time.localtime()
        _log.debug(u'Set date on decoder: %s',
                   time.strftime('%Y-%m-%d', timestruct))
        cmd = bytearray(5)
        cmd[0] = 0x0a
        cmd[1] = 0x0a
        cmd[2] = 0xff & timestruct[2]  # day
        cmd[3] = 0xff & timestruct[1]  # month
        cmd[4] = 0xff & (timestruct[0] - 2000)  # year, after 2000
        self._v3_cmd(bytes(cmd))

    def _setlvl(self, box=u'10', sta=u'10'):
        """Set the read level on box and sta channels."""
        # TODO: verify opts
        self.write(BOXLVL + box.encode(THBC_ENCODING))
        self.write(STALVL + sta.encode(THBC_ENCODING))

    def _set_time_cmd(self, t):
        """Return a set time command string for the provided time of day."""
        body = bytearray(4)
        s = int(t.timeval)
        body[0] = s // 3600  # hours
        body[1] = (s // 60) % 60  # minutes
        body[2] = s % 60  # seconds
        body[3] = 0x74
        return SETTIME + bytes(body)

    def _parse_config(self, msg):
        # decoder configuration message.
        ibuf = bytearray(msg)
        self._decoderconfig = {}
        for flag in sorted(CONFIG_FLAGS):  # import all
            # tone values
            if flag in [
                    CONFIG_TONE_STA, CONFIG_TONE_BOX, CONFIG_TONE_MAN,
                    CONFIG_TONE_CEL, CONFIG_TONE_BXX
            ]:
                self._decoderconfig[flag] = 100 * hexval2val(ibuf[flag])
                self._decoderconfig[flag] += hexval2val(ibuf[flag + 1])

            # single byte values
            elif flag in [
                    CONFIG_TZ_HOUR, CONFIG_TZ_MIN, CONFIG_PROT,
                    CONFIG_PULSEINT, CONFIG_CELLTOD_HOUR, CONFIG_CELLTOD_MIN
            ]:
                self._decoderconfig[flag] = hexval2val(ibuf[flag])

            # 'booleans'
            elif flag in [
                    CONFIG_TOD, CONFIG_GPS, CONFIG_485, CONFIG_FIBRE,
                    CONFIG_PRINT, CONFIG_MAX, CONFIG_PULSE, CONFIG_CELLSYNC,
                    CONFIG_ACTIVE_LOOP
            ]:
                self._decoderconfig[flag] = bool(ibuf[flag])

        self._boxname = u''
        for c in msg[43:47]:
            self._boxname += unichr(ord(c) + ord('0'))
        self._version = unicode(hexval2val(ibuf[47]))
        stalvl = hex(ord(msg[25]))  # ? question this
        boxlvl = hex(ord(msg[26]))
        _log.info(u'Info Decoder ID: %s', self._boxname)
        _log.debug(u'Info Firmware Version: %r', self._version)
        _log.debug(u'Levels: STA=%r, BOX=%r', stalvl, boxlvl)
        self._decoderipconfig[u'IP'] = socket.inet_ntoa(msg[27:31])
        self._decoderipconfig[u'Mask'] = socket.inet_ntoa(msg[31:35])
        self._decoderipconfig[u'Gateway'] = socket.inet_ntoa(msg[35:39])
        self._decoderipconfig[u'Host'] = socket.inet_ntoa(msg[39:43])
        for key in [u'IP', u'Mask', u'Gateway', u'Host']:
            _log.debug(u'%r: %r', key, self._decoderipconfig[key])

    def _parse_message(self, msg, ack=True):
        """Return tod object from timing msg or None."""
        ret = None
        if len(msg) > 4:
            if msg[0] == PASSSTART:  # RFID message
                idx = msg.find(b'>')
                if idx == 37:  # Valid length
                    data = msg[1:33]
                    msum = msg[33:37]
                    tsum = thbc_sum(data)
                    if tsum == msum:  # Valid 'sum'
                        pvec = data.decode(THBC_ENCODING).split()
                        istr = pvec[3] + u':' + pvec[5]
                        rstr = pvec[1].lstrip(u'0')
                        cstr = u'C1'
                        if pvec[0] == u'BOX':
                            cstr = u'C2'
                        elif pvec[0] == u'MAN':
                            cstr = u'C0'
                        if pvec[5] == u'3':  # LOW BATTERY ALERT
                            _log.warning(u'Low battery on %r', rstr)
                        ret = tod.tod(pvec[2],
                                      index=istr,
                                      chan=cstr,
                                      refid=rstr,
                                      source=self._boxname)
                        # Log a hardware-specific passing
                        _log.log(DECODER_LOG_LEVEL, msg.strip())
                        if ack:
                            self._write(ACKCMD)  # Acknowledge if ok
                        self._cksumerr = 0
                    else:
                        _log.warning(u'Invalid checksum: %r != %r: %r', tsum,
                                     msum, msg)
                        self._cksumerr += 1
                        if self._cksumerr > 3:
                            # assume error on decoder, so acknowledge and
                            # continue with log
                            # NOTE: This path is triggered when serial comms
                            # fail and a tag read happens before a manual trig
                            _log.error(u'Erroneous message from decoder')
                            if ack:
                                self._write(ACKCMD)
                else:
                    _log.debug(u'Invalid message: %r', msg)
            elif msg[0] == STATSTART:  # Status message
                data = msg[1:22]
                pvec = data.decode(THBC_ENCODING).split()
                if len(pvec) == 5:
                    _log.info(u'%r@%s Noise:%s/%s Levels:%s/%s', self._boxname,
                              pvec[0], pvec[1], pvec[2], pvec[3], pvec[4])
                else:
                    _log.info(u'Invalid status: %r', msg)
            elif b'+++' == msg[0:3] and len(msg) > 53:
                self._parse_config(msg[3:])
            else:
                pass
        else:
            _log.debug(u'Short message: %r', msg)
        return ret

    def _ipcompletion(self):
        """Blocking wait for ipconfig completion - horrible."""
        _log.info(u'IP Config')
        time.sleep(10)
        self.write(QUECMD)

    def _read(self):
        """Read messages from the decoder until a timeout condition."""
        ch = self._io.read(1)
        while ch != b'':
            if ch == LF and len(self._rdbuf) > 0 and self._rdbuf[-1] == CR:
                # Return ends the current 'message', if preceeded by return
                self._rdbuf += ch  # include trailing newline
                #_log.debug(u'RECV: %r', self._rdbuf)
                t = self._parse_message(self._rdbuf.lstrip(b'\0'))
                if t is not None:
                    self._trig(t)
                self._rdbuf = b''
            elif len(self._rdbuf) > 40 and b'\x1e\x86\x98' in self._rdbuf:
                # Assume acknowledge from IP Command
                #_log.debug(u'RECV: %r', self._rdbuf)
                self._rdbuf = b''
                self._ipcompletion()
            else:
                self._rdbuf += ch
            ch = self._io.read(1)

    def _write(self, msg):
        if self._io is not None:
            self._io.write(msg)
            #_log.debug(u'SEND: %r', msg)

    def run(self):
        """Decoder main loop."""
        _log.debug(u'Starting')
        self._running = True
        while self._running:
            try:
                c = None
                if self._io is not None:
                    # Read responses until response complete or timeout
                    try:
                        self._read()
                    except socket.timeout:
                        pass
                    c = self._cqueue.get_nowait()
                else:
                    c = self._cqueue.get()
                self._cqueue.task_done()
                self._proccmd(c)
            except Queue.Empty:
                pass
            except (serial.SerialException, socket.error) as e:
                self._close()
                self._boxname = None
                _log.error(u'%s: %s', e.__class__.__name__, e)
            except Exception as e:
                _log.critical(u'%s: %s', e.__class__.__name__, e)
                self._boxname = None
                self._running = False
        self.setcb()
        _log.debug(u'Exiting')


class dgram(object):
    """Serial-like UDP port object."""

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.settimeout(0.2)
        self._s.bind((u'', self._port))
        self._buf = b''

    def read(self, sz=1):
        ret = b''  # check this condition
        if len(self._buf) == 0:
            nb, addr = self._s.recvfrom(4096)  # timeout raises exception
            if addr[0] == self._host:
                self._buf += nb
        if len(self._buf) > 0:
            ret = self._buf[0]
            self._buf = self._buf[1:]
        return ret

    def write(self, buf=b''):
        return self._s.sendto(buf, (self._host, self._port))

    def close(self):
        self._s.close()
