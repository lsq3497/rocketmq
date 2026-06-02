# -*- coding: utf-8 -*-
"""Task 9.2: push consumer with business-key idempotency."""

import json
import os
import signal
import time
from pathlib import Path

from rocketmq.client import ConsumeStatus, PushConsumer

from common import GROUP_CONSUMER_IDEMPOTENT, NAMESRV_ADDR, TOPIC_IDEMPOTENT

STATE_FILE = Path(__file__).resolve().parent / ".idempotent_state.json"
running = True


def _stop_handler(_signum, _frame):
    global running
    running = False


class IdempotentStore:
    def __init__(self, path: Path):
        self.path = path
        self.processed_keys = self._load()

    def _load(self):
        if not self.path.exists():
            return set()
        with self.path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        return set(data.get("processed_keys", []))

    def _save(self):
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump({"processed_keys": sorted(self.processed_keys)}, fp, indent=2)

    def is_processed(self, business_key: str) -> bool:
        return business_key in self.processed_keys

    def mark_processed(self, business_key: str):
        self.processed_keys.add(business_key)
        self._save()


store = IdempotentStore(STATE_FILE)


def consume_callback(msg):
    business_key = msg.keys.decode("utf-8") if isinstance(msg.keys, bytes) else msg.keys
    body = msg.body.decode("utf-8")

    if store.is_processed(business_key):
        print(f"[idempotent] SKIP duplicate business_key={business_key} msg_id={msg.id}")
        return ConsumeStatus.CONSUME_SUCCESS

    print(f"[idempotent] PROCESS business_key={business_key} msg_id={msg.id} body={body}")
    store.mark_processed(business_key)
    return ConsumeStatus.CONSUME_SUCCESS


def main() -> None:
    signal.signal(signal.SIGINT, _stop_handler)
    signal.signal(signal.SIGTERM, _stop_handler)

    if os.environ.get("RESET_IDEMPOTENT_STATE") == "1":
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        store.processed_keys.clear()
        print(f"Reset idempotent state file: {STATE_FILE}")

    consumer = PushConsumer(GROUP_CONSUMER_IDEMPOTENT)
    consumer.set_name_server_address(NAMESRV_ADDR)
    consumer.subscribe(TOPIC_IDEMPOTENT, consume_callback, expression="*")
    consumer.start()
    print(f"Idempotent consumer started on topic={TOPIC_IDEMPOTENT}")
    print(f"State file: {STATE_FILE}")
    print("Press Ctrl+C to stop.")

    try:
        while running:
            time.sleep(1)
    finally:
        consumer.shutdown()
        print("Idempotent consumer shutdown.")


if __name__ == "__main__":
    main()
