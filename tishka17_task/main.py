import time


from tishka17_task import BlockingSocketEchoServer


def main() -> int:
    s: BlockingSocketEchoServer = BlockingSocketEchoServer(2222)

    try:
        s.serve()

    except KeyboardInterrupt:
        pass

    finally:
        s.close()

    return 0
