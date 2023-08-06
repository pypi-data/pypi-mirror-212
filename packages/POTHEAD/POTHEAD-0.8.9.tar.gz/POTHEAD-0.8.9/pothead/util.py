from errno import EAGAIN
from socket import MSG_DONTWAIT, MSG_PEEK, error as SocketError
from threading import get_ident, Condition
from typing import Optional, Set

from werkzeug.serving import WSGIRequestHandler

from pothead.wsgi_typing import WsgiApplication


class ObjectProxy:
    """Decorator allowing override of attributes on an instance of another object

    >>> s1 = "hello"
    >>> s2 = ObjectProxy(s1)
    >>> s2.encode = lambda: b"goodbye!"
    >>> assert s1.encode() == b"hello"
    >>> assert s2.encode() == b"goodbye!"
    """

    def __init__(self, inner):
        self.__inner = inner

    def __getattr__(self, name):
        return getattr(self.__inner, name)

    def __call__(self, *args, **kwargs):
        return self.__inner(*args, **kwargs)


class ThreadsTracker:
    _threads: Optional[Set[int]]

    def __init__(self):
        self._threads = set()
        self._cond = Condition()

    def __enter__(self):
        self._threads.add(get_ident())
        return self

    def __exit__(self, exc_type, exc_value, trace):
        with self._cond:
            self._threads.remove(get_ident())
            self._cond.notify_all()

    def __len__(self):
        with self._cond:
            return len(self._threads)

    def drain(self):
        with self._cond:
            self._cond.wait_for(lambda: len(self._threads) == 0)


class SocketCheckingWSGIHandler(WSGIRequestHandler):
    def __init__(self, socket, address, server):
        if not isinstance(server, ObjectProxy):
            server = ObjectProxy(server)
        server.app = self._socket_checking_app(server.app)
        super().__init__(socket, address, server)

    def _socket_checking_app(self, app) -> WsgiApplication:
        def application(environ, start_response):
            response_started = [False]

            def wrapped_start_response(*args, **kwargs):
                response_started[0] = True
                return start_response(*args, **kwargs)

            for chunk in app(environ, wrapped_start_response):
                if len(chunk) == 0:
                    # Non-empty chunks will fail by themselves when sending to client.
                    # Empty chunks OTOH, will give us a chance to abort if client is no longer connected

                    try:
                        if len(self.request.recv(1, MSG_DONTWAIT | MSG_PEEK)) == 0:
                            # recv() returns empty slice if client shutdown it's writing side
                            #
                            # Considering "closed for reading" as a sign of abandoned request is not supported by the
                            # HTTP specification, (https://datatracker.ietf.org/doc/html/rfc9112#section-9.6).
                            # However, it _is_ the default behavior of hyper, and we can probably get away with it
                            # https://docs.rs/hyper/0.14.26/hyper/server/struct.Builder.html#method.http1_half_close
                            raise ConnectionError(
                                "Connection closed during response from server"
                            )
                    except SocketError as e:
                        if e.errno != EAGAIN:
                            raise ConnectionError(
                                "Connection closed during response from server"
                            ) from e
                # By allowing empty chunks to be yielded before `start_response`, we enable early abort. But, werkzeug
                # doesn't support even empty chunks to be yielded before `start_response` is called, so we suppress
                # those
                if not response_started[0] and len(chunk) == 0:
                    continue

                yield chunk

        return application
