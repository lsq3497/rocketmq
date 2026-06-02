# -*- coding: utf-8 -*-
"""Task 7.2: async send messages with Tag (callback style)."""

import threading

from common import (
    GROUP_PRODUCER_TAG,
    TOPIC_TAG,
    build_message,
    create_producer,
    send_async_with_callback,
)

MESSAGE_COUNT = 10
TAGS = ("TagA", "TagB", "TagC")


def main() -> None:
    producer = create_producer(GROUP_PRODUCER_TAG)
    producer.start()
    print("Tag async producer started.")

    done = threading.Event()
    pending = {"count": MESSAGE_COUNT}
    lock = threading.Lock()

    def on_done() -> None:
        with lock:
            pending["count"] -= 1
            if pending["count"] == 0:
                done.set()

    try:
        for i in range(MESSAGE_COUNT):
            tag = TAGS[i % len(TAGS)]
            msg = build_message(
                TOPIC_TAG,
                f"Async message with {tag} #{i}",
                tag=tag,
                keys=f"async-{i}",
            )

            def on_success(result, index=i, current_tag=tag):
                print(
                    f"[async-{current_tag}] #{index} status={result.status} "
                    f"msg_id={result.msg_id} offset={result.offset}"
                )
                on_done()

            def on_exception(exc, index=i):
                print(f"[async] #{index} exception: {exc}")
                on_done()

            send_async_with_callback(producer, msg, on_success, on_exception)

        if not done.wait(timeout=30):
            print("Warning: not all async sends finished within 30 seconds.")
    finally:
        producer.shutdown()
        print("Tag async producer shutdown.")


if __name__ == "__main__":
    main()
