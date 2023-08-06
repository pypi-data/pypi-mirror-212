# SPDX-License-Identifier: MIT
"""Race Result System decoder interface."""

from __future__ import division

import Queue
import logging
import socket
import datetime

from . import (decoder, DECODER_LOG_LEVEL)
from metarace import tod
from metarace import sysconf

_log = logging.getLogger(u'metarace.decoder.rrs')
_log.setLevel(logging.DEBUG)

# desired target protocol level
_RRS_PROTOCOL = u'3.2'
# decoder port
_RRS_TCP_PORT = 3601
# passing record length
_RRS_PASSLEN = 20
# status record length
_RRS_STATUSLEN = 25
# Warn if battery voltage is below this many volts
_RRS_LOWBATT = 2.0
_RRS_SYNFMT = u'SETTIME;{:04d}-{:02d}-{:02d};{}'
_RRS_EOL = u'\r\n'
_RRS_MARKER = u'99999'
_RRS_ENCODING = u'iso8859-1'
_RRS_IOTIMEOUT = 1.0
_RRS_PASSIVEID = u'1'

# Error flags from decoder status
_RRS_ERRORFLAGS = {
    1: u'UHF module reports an error',
    16: u'Active loop error',
    32: u'Active loop limit',
    64: u'Active connection lost',
    256: u'GPS time sync error',
    512: u'GPS communication error warning',
    1024: u'Active time sync error'
}


class rrs(decoder):
    """RRS thread object class."""

    def __init__(self):
        decoder.__init__(self)
        self._io = None
        self._rdbuf = b''
        self._curfile = None
        self._lastpassing = None
        self._dorefetch = True
        self._fetchpending = False
        self._pending_command = None
        self._allowstored = False
        self._passiveloop = _RRS_PASSIVEID

    # API overrides
    def sync(self, data=None):
        self.stop_session(data)
        self._cqueue.put_nowait((u'_sync', data))
        self.start_session(data)

    def start_session(self, data=None):
        self.write(u'STARTOPERATION')
        self.write(u'PASSINGS')

    def stop_session(self, data=None):
        self.write(u'STOPOPERATION')

    def status(self, data=None):
        self.write(u'GETSTATUS')

    def connected(self):
        return self._io is not None

    def clear(self, data=None):
        self.stop_session(data)
        self.write(u'CLEARFILES')
        self._cqueue.put_nowait((u'_sync', data))
        self.start_session(data)

    # Device-specific functions
    def _close(self):
        if self._io is not None:
            _log.debug(u'Close connection')
            cp = self._io
            self._io = None
            try:
                cp.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                _log.debug(u'%s: shutdown socket: %s', e.__class__.__name__, e)
            cp.close()

    def _sane(self, data=None):
        for m in [
                u'GETPROTOCOL',
                u'SETPROTOCOL;{}'.format(_RRS_PROTOCOL),
                u'SETPUSHPREWARNS;0',
                u'SETPUSHPASSINGS;1;0',
                u'GETCONFIG;GENERAL;BOXNAME',
                u'GETCONFIG;ACTIVE;LOOPID',
                u'GETCONFIG;ACTIVE;POWER',
                u'GETCONFIG;UPLOAD;CONNECTION',
                u'GETINTERFACES',
                u'GETSTATUS',
                u'PASSINGS',
        ]:
            self.write(m)

    def _port(self, port):
        """Re-establish connection to supplied device port."""
        self._close()
        addr = (port, _RRS_TCP_PORT)
        _log.debug(u'Connecting to %r', addr)
        self._rdbuf = b''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 5000)
        except Exception as e:
            _log.debug('%s setting socket option: %s', e.__class__.__name__, e)
        s.connect(addr)
        s.settimeout(_RRS_IOTIMEOUT)
        self._io = s
        self.sane()

    def _sync(self, data=None):
        a = datetime.datetime.now()
        nt = tod.now() + tod.tod('0.640')
        syncmd = _RRS_SYNFMT.format(
            a.year, a.month, a.day,
            nt.rawtime(places=3, zeros=True, hoursep=u':'))
        self._write(syncmd)

    def _replay(self, file):
        """RRS-specific replay"""
        if file.isdigit():
            _log.debug(u'Replay passings from %r', file)
            cmd = u'GETFILE;{:d}'.format(file)
            self._write(cmd)
        else:
            _log.error(u'Invalid file specified: %r', file)

    def _write(self, msg):
        if self._io is not None:
            ob = (msg + _RRS_EOL)
            self._io.sendall(ob.encode(_RRS_ENCODING))
            #_log.debug(u'SEND: %r', ob)

    def _passing(self, pv):
        """Process a RRS protocol passing."""
        if len(pv) == _RRS_PASSLEN:
            today = datetime.date.today().isoformat()
            istr = pv[0]  # <PassingNo>
            tagid = pv[1]  # <Bib/TranspCode>
            date = pv[2]  # <Date>
            timestr = pv[3]  # <Time>
            eventid = pv[4]  # <EventID>
            isactive = pv[8]  # <IsActive>
            loopid = pv[10]  # <LoopID>
            wuc = pv[12]  # <WakeupCounter>
            battery = pv[13]  # <Battery>
            adata = pv[15]  # <InternalActiveData>
            bname = pv[16]  # <BoxName>
            hits = pv[5]  # <Hits>
            rssi = pv[6]  # <MaxRSSI>

            # An error here will invalidate the whole passing
            pid = int(istr)
            if self._lastpassing is not None:
                expectpid = self._lastpassing + 1
                if pid != expectpid:
                    _log.debug(u'Ignore out of sequence passing: %r != %r',
                               pid, expectpid)
                    return
            self._lastpassing = pid

            active = False
            try:
                active = bool(int(isactive))
                if eventid == u'0':
                    eventid = u''
            except Exception as e:
                _log.debug(u'%s reading isactive: %s', e.__class__.__name__, e)

            if not loopid:
                loopid = self._passiveloop
            try:
                loopid = u'C' + str(int(loopid))
            except Exception as e:
                _log.debug(u'%s reading loop id: %s', e.__class__.__name__, e)
            activestore = False
            if active and adata:
                activestore = (int(adata) & 0x40) == 0x40
            if not active and tagid and eventid:
                tagid = u'-'.join((eventid, tagid))
            #if tagid.startswith(_RRS_MARKER):
            if tagid == _RRS_MARKER:
                tagid = u''

            if battery and tagid:
                try:
                    bv = float(battery)
                    if bv < _RRS_LOWBATT:
                        _log.warning(u'Low battery %s: %0.1fV', tagid, bv)
                except Exception as e:
                    _log.debug(u'%s reading battery voltage: %s',
                               e.__class__.__name__, e)

            if hits and rssi and tagid:
                try:
                    hitcount = int(hits)
                    if active:
                        rssival = int(rssi, 16)
                        twofour = -90 + ((rssival & 0x70) >> 2)
                        lstrength = 1 + (rssival & 0x0f)
                        if lstrength < 5 or twofour < -82 or hitcount < 4:
                            _log.warning(
                                u'Poor read %s: Hits:%d RSSI:%ddBm Loop:%ddB',
                                tagid, hitcount, twofour, lstrength)
                    else:
                        rssival = int(rssi)
                        if rssival < -82 or hitcount < 4:
                            _log.warning(u'Poor read %s: Hits:%d RSSI:%ddBm',
                                         tagid, hitcount, rssival)
                except Exception as e:
                    _log.debug(u'%s reading hits/RSSI: %s',
                               e.__class__.__name__, e)

            # emit a decoder log line TBD
            _log.log(DECODER_LOG_LEVEL, u';'.join(pv))

            # accept valid passings and trigger callback
            t = tod.mktod(timestr)
            if t is not None:
                t.index = istr
                t.chan = loopid
                t.refid = tagid
                t.source = bname
                if not activestore or self._allowstored:
                    self._trig(t)
                else:
                    pass
        else:
            _log.info(u'Non-passing message: %r', pv)

    def _statusmsg(self, pv):
        """Process a RRS protocol status message."""
        if len(pv) == _RRS_STATUSLEN:
            pwr = pv[2]  # <HasPower>
            opmode = pv[4]  # <IsInOperationMode>
            uhf = pv[8]  # <ReaderIsHealthy>
            batt = pv[9]  # <BatteryCharge>
            active = pv[13]  # <ActiveExtConnected>
            eflag = pv[23]  # <ErrorFlags>
            if batt == u'-1':
                batt = u'[estimating]'
            else:
                batt += u'%'
            loopch = u'n/a'
            loopid = self._passiveloop
            looppower = u'n/a'
            if active == u'1':
                loopch = pv[14]
                loopid = pv[15]
                looppower = pv[16]
            else:
                loopch = pv[3]

            if opmode == u'1':
                _log.info(
                    u'Started, charge:%s, uhf:%s, batt:%s, ch:%s, loop:%s, power:%s',
                    pwr, uhf, batt, loopch, loopid, looppower)
            else:
                _log.warning(
                    u'Not started, charge:%s, uhf:%s, batt:%s, ch:%s, loop:%s, power:%s',
                    pwr, uhf, batt, loopch, loopid, looppower)

            if eflag != u'0':
                stat = int(eflag)
                evec = []
                for bit in _RRS_ERRORFLAGS:
                    if stat & bit == bit:
                        evec.append(_RRS_ERRORFLAGS[bit])
                _log.error(u'Error: %s', u', '.join(evec))

    def _configmsg(self, pv):
        """Process a RRS protocol config message."""
        if len(pv) > 3:
            if pv[1] == u'BOXNAME':
                boxid = pv[3]  # <DeviceId>
                _log.info(u'%r connected', boxid)
            elif pv[1] == u'LOOPID':
                _log.info(u'Config Loop ID: %s', pv[3])
            elif pv[1] == u'POWER':
                _log.info(u'Config Loop Power: %s', pv[3])

    def _protocolmsg(self, pv):
        """Respond to protocol message from decoder."""
        if len(pv) == 3:
            if _RRS_PROTOCOL > pv[2]:
                _log.error(
                    u'Protocol %r unsupported (max %r), update firmware',
                    _RRS_PROTOCOL, pv[2])

    def _passingsmsg(self, pv):
        """Handle update of current passing count."""
        try:
            newfile = None
            if len(pv) > 1:
                newfile = int(pv[1])
            newidx = int(pv[0])
            if newfile != self._curfile:
                _log.debug(u'New passing file %r', newfile)
                self._curfile = newfile
                self._lastpassing = newidx
            else:
                if self._lastpassing is None or newidx < self._lastpassing:
                    # assume new connection or new file
                    _log.debug(u'Last passing %r updated to %r',
                               self._lastpassing, newidx)
                    self._lastpassing = newidx
                else:
                    # assume a broken connection and fetch missed passings
                    _log.debug(u'Missed %r passings, last passing = %r',
                               newidx - self._lastpassing, self._lastpassing)
            self._fetchpending = False
        except Exception as e:
            _log.debug(u'%s reading passing count: %s', e.__class__.__name__,
                       e)

    def _procmsg(self, msg):
        """Process a decoder response message."""
        #_log.debug(u'RECV: %r', msg)
        mv = msg.strip().split(u';')
        if mv[0].isdigit():  # Requested passing
            self._pending_command = u'PASSING'
            self._passing(mv)
        elif mv[0] == u'#P':  # Pushed passing
            self._passing(mv[1:])
        elif mv[0] == u'GETSTATUS':
            self._statusmsg(mv[1:])
        elif mv[0] == u'GETCONFIG':
            self._configmsg(mv[1:])
        elif mv[0] == u'GETPROTOCOL':
            self._protocolmsg(mv[1:])
        elif mv[0] == u'PASSINGS':
            self._passingsmsg(mv[1:])
        elif mv[0] == u'SETTIME':
            _log.info(u'Time set to: %r %r', mv[1], mv[2])
        elif mv[0] == u'STARTOPERATION':
            self._curfile = None
            self._lastpassing = None
            _log.info(u'Start session')
        elif mv[0] == u'STOPOPERATION':
            self._curfile = None
            self._lastpassing = None
            _log.info(u'Stop session')
        elif mv[0].startswith(u'ONLY '):
            self._fetchpending = False
        elif mv[0] == u'':
            _log.debug(u'End of requested passings')
            self._fetchpending = False
            self._pending_command = None
            self._dorefetch = True
        else:
            pass  # Ignore other responses

    def _procline(self):
        """Read and process whole line from decoder, return command status."""
        idx = self._rdbuf.find(b'\n')
        if idx < 0:
            inb = self._io.recv(512)
            if inb == b'':
                _log.info(u'Connection closed by peer')
                self._close()
            else:
                self._rdbuf += inb
            idx = self._rdbuf.find(b'\n')
        if idx >= 0:
            l = self._rdbuf[0:idx + 1].decode(_RRS_ENCODING)
            self._rdbuf = self._rdbuf[idx + 1:]
            self._procmsg(l)
        return self._pending_command is None

    def _refetch(self):
        """Poll decoder for new passings."""
        if not self._fetchpending:
            if self._dorefetch and self._lastpassing is not None:
                self._fetchpending = True
                self._dorefetch = False
                cmd = u'{:d}:32'.format(self._lastpassing + 1)
                self.write(cmd)

    def run(self):
        """Decoder main loop."""
        _log.debug(u'Starting')
        if sysconf.has_option(u'rrs', u'allowstored'):
            self._allowstored = sysconf.get_bool(u'rrs', u'allowstored')
            _log.debug('Allow stored passings: %r', self._allowstored)
        if sysconf.has_option(u'rrs', u'passiveloop'):
            self._passiveloop = sysconf.get_str(u'rrs', u'passiveloop', u'1')
            _log.info(u'Passive loop id set to: %r', self._passiveloop)
        self._running = True
        while self._running:
            try:
                c = None
                if self._io is not None:
                    # Read responses until response complete or timeout
                    try:
                        while not self._procline():
                            pass
                    except socket.timeout:
                        self._dorefetch = True
                    self._refetch()
                    c = self._cqueue.get_nowait()
                else:
                    c = self._cqueue.get()
                self._cqueue.task_done()
                self._proccmd(c)
            except Queue.Empty:
                pass
            except socket.error as e:
                self._close()
                _log.error(u'%s: %s', e.__class__.__name__, e)
            except Exception as e:
                _log.critical(u'%s: %s', e.__class__.__name__, e)
                self._running = False
        self.setcb()
        _log.debug(u'Exiting')
