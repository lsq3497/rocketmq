# -*- coding: utf-8 -*-
"""Helper producer for task 8: send messages to push consumer topic."""

from common import GROUP_PRODUCER_NORMAL, TOPIC_PUSH, build_message, create_producer, print_send_result

MESSAGE_COUNT = 10


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_NORMAL)
    producer.start()

    try:
        for i in range(MESSAGE_COUNT):
            msg = build_message(
                TOPIC_PUSH,
                f"Push demo message {i}",
                tag="TagPush",
                keys=f"push-{i}",
            )
            result = producer.send_sync(msg)
            print_send_result("push-feed", i, result)
    finally:
        producer.shutdown()


if __name__ == "__main__":
    main()
