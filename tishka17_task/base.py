import abc
import socket
import weakref

from typing import Tuple
from typing import MutableMapping

from threading import Thread
from threading import Event
from threading import RLock

Addr = Tuple[str, int]


class BaseEchoServer(abc.ABC):
    def __init__(self, port: int = 42069):
        self.s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((socket.gethostname(), port))

        self.lock: RLock = RLock()
        self.conns: MutableMapping[socket.socket, bytes] = weakref.WeakKeyDictionary()
        self._serving_event: Event = Event()

    @property
    def serving(self) -> bool:
        return self._serving_event.is_set()

    @serving.setter
    def serving(self, value: bool) -> None:
        e: Event = self._serving_event

        if value:
            e.set()

        else:
            e.clear()

    @abc.abstractmethod
    def stop_serve(self) -> None:
        pass

    @abc.abstractmethod
    def send_to(self, conn: socket.socket, message: bytes) -> None:
        pass

    @abc.abstractmethod
    def recv_from(self, conn: socket.socket) -> bytes:
        pass

    @abc.abstractmethod
    def close_conn(self, conn: socket.socket) -> None:
        pass

    @abc.abstractmethod
    def accept(self) -> Tuple[socket.socket, Addr]:
        pass

    def send_to_all(self, message: bytes) -> None:
        with self.lock:
            for conn in self.conns:
                self.send_to(conn, message)

    def process_data(self, conn: socket.socket, data: bytes) -> None:
        if not self.serving:
            return

        while True:
            end_old_message, lf, start_new_message = data.partition(b'\n')

            if lf:
                message: bytes = self.conns[conn] + end_old_message + lf

                print(message)
                self.send_to_all(message)

                data = start_new_message

            else:
                self.conns[conn] += end_old_message
                break

    def handle(self, conn: socket.socket, addr: Addr) -> None:
        try:
            while self.serving:
                data: bytes = self.recv_from(conn)

                if not data:
                    break

                self.process_data(conn, data)

        except OSError:
            pass

        else:
            self.close_conn(conn)

    def process(self) -> None:
        conn, addr = self.accept()

        if not self.serving:
            self.close_conn(conn)

            return

        self.conns[conn] = b''

        t: Thread = Thread(target=self.handle, args=(conn, addr))
        t.start()

    def serve(self) -> None:
        if self.serving:
            raise RuntimeError('Already serving')

        self.serving = True
        self.s.listen()

        while self.serving:
            self.process()

    def close(self) -> None:
        self.serving = False

        for conn in self.conns:
            self.close_conn(conn)

        self.stop_serve()
