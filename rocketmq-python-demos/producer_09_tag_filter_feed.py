# -*- coding: utf-8 -*-
"""Helper producer for task 9.1: send TagA/TagB/TagC messages for tag filter demo."""

from common import (
    GROUP_PRODUCER_TAG_FILTER,
    TOPIC_TAG_FILTER,
    build_message,
    create_producer,
    print_send_result,
)

TAGS = ("TagA", "TagB", "TagC")
MESSAGE_COUNT = 9


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_TAG_FILTER)
    producer.start()

    try:
        for i in range(MESSAGE_COUNT):
            tag = TAGS[i % len(TAGS)]
            msg = build_message(
                TOPIC_TAG_FILTER,
                f"Tag filter demo message {i} with {tag}",
                tag=tag,
                keys=f"filter-{i}",
            )
            result = producer.send_sync(msg)
            print_send_result(f"filter-{tag}", i, result)
    finally:
        producer.shutdown()


if __name__ == "__main__":
    main()
