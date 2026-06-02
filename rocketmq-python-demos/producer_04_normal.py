# -*- coding: utf-8 -*-
"""Task 4: send normal (standard) messages."""

from common import (
    GROUP_PRODUCER_NORMAL,
    NAMESRV_ADDR,
    TOPIC_NORMAL,
    build_message,
    create_producer,
    print_send_result,
)

MESSAGE_COUNT = 10


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_NORMAL)
    producer.start()
    print(f"Normal producer started, namesrv={NAMESRV_ADDR}")

    try:
        for i in range(MESSAGE_COUNT):
            msg = build_message(
                TOPIC_NORMAL,
                f"Hello RocketMQ normal message {i}",
                tag="TagA",
                keys=f"KEY-{i}",
            )
            result = producer.send_sync(msg)
            print_send_result("normal-sync", i, result)
    finally:
        producer.shutdown()
        print("Normal producer shutdown.")


if __name__ == "__main__":
    main()
