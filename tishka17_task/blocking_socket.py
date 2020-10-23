import socket

from typing import Tuple

from tishka17_task import BaseEchoServer

Addr = Tuple[str, int]


BUFFSIZE: int = 512

class BlockingSocketEchoServer(BaseEchoServer):
    def send_to(self, conn: socket.socket, message: bytes) -> None:
        conn.send(message)

    def recv_from(self, conn: socket.socket) -> bytes:
        return conn.recv(BUFFSIZE)

    def close_conn(self, conn: socket.socket) -> None:
        conn.close()

    def accept(self) -> Tuple[socket.socket, Addr]:
        return self.s.accept()

    def stop_serve(self) -> None:
        self.s.close()
