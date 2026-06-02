# -*- coding: utf-8 -*-
"""Helper producer for task 9.2: send duplicate business keys to demo idempotency."""

from common import (
    GROUP_PRODUCER_IDEMPOTENT,
    TOPIC_IDEMPOTENT,
    build_message,
    create_producer,
    print_send_result,
)

# Same business key appears twice to simulate duplicate delivery.
DUPLICATE_KEYS = ("biz-1001", "biz-1002", "biz-1001", "biz-1003", "biz-1002")


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_IDEMPOTENT)
    producer.start()

    try:
        for i, business_key in enumerate(DUPLICATE_KEYS):
            msg = build_message(
                TOPIC_IDEMPOTENT,
                f"Idempotent demo payload for {business_key} send#{i}",
                tag="TagIdempotent",
                keys=business_key,
            )
            result = producer.send_sync(msg)
            print_send_result(f"idempotent-{business_key}", i, result)
    finally:
        producer.shutdown()


if __name__ == "__main__":
    main()
