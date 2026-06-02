# -*- coding: utf-8 -*-
"""Task 6.1: send delay messages using delay time level."""

import time

from common import (
    GROUP_PRODUCER_DELAY,
    TOPIC_DELAY,
    build_message,
    create_producer,
    print_send_result,
)

# RocketMQ default delay levels: 1s 5s 10s 30s 1m ...
# Level 3 means the message is delivered about 10 seconds later.
DELAY_LEVEL = 3
MESSAGE_COUNT = 5


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_DELAY)
    producer.start()
    print("Delay producer started.")

    try:
        for i in range(MESSAGE_COUNT):
            msg = build_message(
                TOPIC_DELAY,
                f"Delay message {i}, expect delivery ~10s later (level={DELAY_LEVEL})",
                tag="TagDelay",
                keys=f"delay-{i}",
            )
            msg.set_delay_time_level(DELAY_LEVEL)
            sent_at = time.strftime("%H:%M:%S")
            result = producer.send_sync(msg)
            print(f"[delay] sent_at={sent_at}", end=" ")
            print_send_result("delay", i, result)
    finally:
        producer.shutdown()
        print("Delay producer shutdown. Start consumer_08_push.py on TOPIC_DELAY to observe delay.")


if __name__ == "__main__":
    main()
