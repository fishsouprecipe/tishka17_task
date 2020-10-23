import time


from tishka17_task.blocking_server import BlockingServer


def main() -> int:
    s: BlockingServer = BlockingServer("0.0.0.0", 2222)

    try:
        s.serve()

    except KeyboardInterrupt:
        pass

    finally:
        s.close()

    return 0
