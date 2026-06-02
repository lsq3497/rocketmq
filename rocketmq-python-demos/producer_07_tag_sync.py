# -*- coding: utf-8 -*-
"""Task 7.1: sync send messages with Tag."""

from common import (
    GROUP_PRODUCER_TAG,
    TOPIC_TAG,
    build_message,
    create_producer,
    print_send_result,
)

MESSAGE_COUNT = 10
TAGS = ("TagA", "TagB", "TagC")


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_TAG)
    producer.start()
    print("Tag sync producer started.")

    try:
        for i in range(MESSAGE_COUNT):
            tag = TAGS[i % len(TAGS)]
            msg = build_message(
                TOPIC_TAG,
                f"Sync message with {tag} #{i}",
                tag=tag,
                keys=f"sync-{i}",
            )
            result = producer.send_sync(msg)
            print_send_result(f"sync-{tag}", i, result)
    finally:
        producer.shutdown()
        print("Tag sync producer shutdown.")


if __name__ == "__main__":
    main()
