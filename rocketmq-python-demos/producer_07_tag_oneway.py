# -*- coding: utf-8 -*-
"""Task 7.3: oneway send messages with Tag (fire-and-forget)."""

from common import (
    GROUP_PRODUCER_TAG,
    TOPIC_TAG,
    build_message,
    create_producer,
)

MESSAGE_COUNT = 10
TAGS = ("TagA", "TagB", "TagC")


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_TAG)
    producer.start()
    print("Tag oneway producer started.")

    try:
        for i in range(MESSAGE_COUNT):
            tag = TAGS[i % len(TAGS)]
            msg = build_message(
                TOPIC_TAG,
                f"Oneway message with {tag} #{i}",
                tag=tag,
                keys=f"oneway-{i}",
            )
            producer.send_oneway(msg)
            print(f"[oneway-{tag}] #{i} sent (no broker ack returned)")
    finally:
        producer.shutdown()
        print("Tag oneway producer shutdown.")


if __name__ == "__main__":
    main()
