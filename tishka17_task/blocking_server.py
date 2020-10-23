import socket

from typing import Tuple

from threading import Thread

from tishka17_task.constants import DEFAULT_BYTES_READ


class BlockingSocketEchoServer:
    def __init__(self, host: str, port: int):
        self.s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

    def _handle(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
        try:
            while True:
                data: bytes = conn.recv(DEFAULT_BYTES_READ)

                if not len(data):
                    break

                print(data)
                conn.send(data)

        except:
            pass

        finally:
            conn.close()


    def _accept(self) -> None:
        conn, addr = self.s.accept()

        t: Thread = Thread(target=self._handle, args=(conn, addr))
        t.daemon = True
        t.start()

    def serve(self):
        self.s.listen()

        while True:
            self._accept()

    def close(self):
        self.s.close()
