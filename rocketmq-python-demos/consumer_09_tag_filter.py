# -*- coding: utf-8 -*-
"""Task 9.1: push consumer with tag filter expression (TagA || TagC)."""

import signal
import time

from rocketmq.client import ConsumeStatus, PushConsumer

from common import GROUP_CONSUMER_TAG_FILTER, NAMESRV_ADDR, TOPIC_TAG_FILTER

running = True
TAG_EXPRESSION = "TagA || TagC"


def _stop_handler(_signum, _frame):
    global running
    running = False


def consume_callback(msg):
    tag = msg.tags.decode("utf-8") if isinstance(msg.tags, bytes) else msg.tags
    body = msg.body.decode("utf-8")
    print(
        f"[tag-filter] matched tag={tag} msg_id={msg.id} body={body}"
    )
    return ConsumeStatus.CONSUME_SUCCESS


def main() -> None:
    signal.signal(signal.SIGINT, _stop_handler)
    signal.signal(signal.SIGTERM, _stop_handler)

    consumer = PushConsumer(GROUP_CONSUMER_TAG_FILTER)
    consumer.set_name_server_address(NAMESRV_ADDR)
    consumer.subscribe(TOPIC_TAG_FILTER, consume_callback, expression=TAG_EXPRESSION)
    consumer.start()
    print(
        f"Tag filter consumer started on topic={TOPIC_TAG_FILTER}, "
        f"expression='{TAG_EXPRESSION}'"
    )
    print("Only TagA and TagC messages should appear. Press Ctrl+C to stop.")

    try:
        while running:
            time.sleep(1)
    finally:
        consumer.shutdown()
        print("Tag filter consumer shutdown.")


if __name__ == "__main__":
    main()
