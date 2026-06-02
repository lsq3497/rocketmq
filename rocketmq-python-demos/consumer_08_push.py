# -*- coding: utf-8 -*-
"""Task 8: push mode consumer."""

import os
import signal
import time

from rocketmq.client import ConsumeStatus, PushConsumer

from common import GROUP_CONSUMER_PUSH, NAMESRV_ADDR, TOPIC_PUSH

CONSUME_TOPIC = os.environ.get("ROCKETMQ_TOPIC", TOPIC_PUSH)

running = True


def _stop_handler(_signum, _frame):
    global running
    running = False


def consume_callback(msg):
    body = msg.body.decode("utf-8")
    print(
        f"[push-consumer] topic={msg.topic} tag={msg.tags} "
        f"msg_id={msg.id} body={body}"
    )
    return ConsumeStatus.CONSUME_SUCCESS


def main() -> None:
    signal.signal(signal.SIGINT, _stop_handler)
    signal.signal(signal.SIGTERM, _stop_handler)

    consumer = PushConsumer(GROUP_CONSUMER_PUSH)
    consumer.set_name_server_address(NAMESRV_ADDR)
    consumer.subscribe(CONSUME_TOPIC, consume_callback, expression="*")
    consumer.start()
    print(f"Push consumer started on topic={CONSUME_TOPIC}, group={GROUP_CONSUMER_PUSH}")
    print("Press Ctrl+C to stop.")

    try:
        while running:
            time.sleep(1)
    finally:
        consumer.shutdown()
        print("Push consumer shutdown.")


if __name__ == "__main__":
    main()
