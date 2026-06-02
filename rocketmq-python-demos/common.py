# -*- coding: utf-8 -*-
"""Shared configuration and helpers for RocketMQ Python homework demos."""

import os
import threading
from typing import Callable, Optional

from rocketmq.client import Message, Producer, SendResult

NAMESRV_ADDR = os.environ.get("ROCKETMQ_NAMESRV", "127.0.0.1:9876")

TOPIC_NORMAL = "HomeworkTopicNormal"
TOPIC_ORDER = "HomeworkTopicOrder"
TOPIC_DELAY = "HomeworkTopicDelay"
TOPIC_TRANSACTION = "HomeworkTopicTransaction"
TOPIC_TAG = "HomeworkTopicTag"
TOPIC_PUSH = "HomeworkTopicPush"
TOPIC_TAG_FILTER = "HomeworkTopicTagFilter"
TOPIC_IDEMPOTENT = "HomeworkTopicIdempotent"

GROUP_PRODUCER_NORMAL = "homework_producer_normal"
GROUP_PRODUCER_ORDER = "homework_producer_order"
GROUP_PRODUCER_DELAY = "homework_producer_delay"
GROUP_PRODUCER_TRANSACTION = "homework_producer_transaction"
GROUP_PRODUCER_TAG = "homework_producer_tag"
GROUP_PRODUCER_TAG_FILTER = "homework_producer_tag_filter"
GROUP_PRODUCER_IDEMPOTENT = "homework_producer_idempotent"

GROUP_CONSUMER_PUSH = "homework_consumer_push"
GROUP_CONSUMER_TAG_FILTER = "homework_consumer_tag_filter"
GROUP_CONSUMER_IDEMPOTENT = "homework_consumer_idempotent"


def create_producer(group_id: str, orderly: bool = False) -> Producer:
    producer = Producer(group_id, orderly=orderly)
    producer.set_name_server_address(NAMESRV_ADDR)
    return producer


def build_message(topic: str, body: str, tag: str = "TagA", keys: Optional[str] = None) -> Message:
    msg = Message(topic)
    msg.set_tags(tag)
    msg.set_body(body)
    if keys:
        msg.set_keys(keys)
    return msg


def print_send_result(prefix: str, index: int, result: SendResult) -> None:
    print(f"[{prefix}] #{index} status={result.status} msg_id={result.msg_id} offset={result.offset}")


def send_async_with_callback(
    producer: Producer,
    msg: Message,
    on_success: Callable[[SendResult], None],
    on_exception: Callable[[Exception], None],
) -> None:
    """Python client has no native async API; emulate Java SendCallback via background thread."""

    def _worker() -> None:
        try:
            result = producer.send_sync(msg)
            on_success(result)
        except Exception as exc:
            on_exception(exc)

    threading.Thread(target=_worker, daemon=True).start()
