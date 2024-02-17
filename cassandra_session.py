import threading
import time

import cherrypy
from cherrypy.lib.sessions import Session

import marvel


class CassandraSession(Session):
    mc_lock = threading.RLock()
    locks = {}

    @classmethod
    def setup(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.mdb = marvel.Marvel()

    def _exists(self):
        self.mc_lock.acquire()
        try:
            return bool(self.mdb.get_cherry_session(self.id))
        finally:
            self.mc_lock.release()

    def _load(self):
        self.mc_lock.acquire()
        try:
            return self.mdb.get_cherry_session(self.id)
        finally:
            self.mc_lock.release()

    def _save(self, expiration_time):
        timestamp = int(time.mktime(expiration_time.timetuple()))
        self.mc_lock.acquire()
        try:
            self.mdb.set_cherry_session(self.id, self._data, expiration_time, timestamp)
        finally:
            self.mc_lock.release()

    def _delete(self):
        self.mdb.delete_cherry_session(self.id)

    def acquire_lock(self):
        """Acquire an exclusive lock on the currently-loaded session data."""
        self.locked = True
        self.locks.setdefault(self.id, threading.RLock()).acquire()
        if self.debug:
            cherrypy.log('Lock acquired.', 'TOOLS.SESSIONS')

    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        self.locks[self.id].release()
        self.locked = False

    def __len__(self):
        """Return the number of active sessions."""
        raise NotImplementedError
