# -*- coding: utf-8 -*-
"""Task 5: send orderly messages with the same sharding key to one queue."""

from common import (
    GROUP_PRODUCER_ORDER,
    TOPIC_ORDER,
    build_message,
    create_producer,
    print_send_result,
)

MESSAGE_COUNT = 30
SHARDING_KEYS = ("order-001", "order-002", "order-003")


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_ORDER, orderly=True)
    producer.start()
    print("Orderly producer started.")

    try:
        for i in range(MESSAGE_COUNT):
            sharding_key = SHARDING_KEYS[i % len(SHARDING_KEYS)]
            msg = build_message(
                TOPIC_ORDER,
                f"Orderly message {i} for {sharding_key}",
                tag=f"Tag{i % 3}",
                keys=sharding_key,
            )
            result = producer.send_orderly_with_sharding_key(msg, sharding_key)
            print_send_result(f"orderly-{sharding_key}", i, result)
    finally:
        producer.shutdown()
        print("Orderly producer shutdown.")


if __name__ == "__main__":
    main()
