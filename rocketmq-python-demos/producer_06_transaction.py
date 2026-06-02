# -*- coding: utf-8 -*-
"""Task 6.2: send transaction messages with local execute and check callbacks."""

import time

from rocketmq.client import TransactionMQProducer, TransactionStatus

from common import GROUP_PRODUCER_TRANSACTION, NAMESRV_ADDR, TOPIC_TRANSACTION, build_message, print_send_result

MESSAGE_COUNT = 5


def transaction_checker(msg) -> TransactionStatus:
    body = msg.body.decode("utf-8")
    print(f"[transaction-check] msg_id={msg.id} body={body}")
    if "rollback" in body.lower():
        return TransactionStatus.ROLLBACK
    return TransactionStatus.COMMIT


def local_transaction_execute(msg, _user_args) -> TransactionStatus:
    body = msg.body.decode("utf-8")
    print(f"[transaction-local] executing local branch for: {body}")
    if "rollback" in body.lower():
        print("[transaction-local] local logic failed -> ROLLBACK")
        return TransactionStatus.ROLLBACK
    print("[transaction-local] local logic success -> COMMIT")
    return TransactionStatus.COMMIT


def main() -> None:
    producer = TransactionMQProducer(GROUP_PRODUCER_TRANSACTION, transaction_checker)
    producer.set_name_server_address(NAMESRV_ADDR)
    producer.start()
    print("Transaction producer started.")

    try:
        for i in range(MESSAGE_COUNT):
            action = "commit" if i % 2 == 0 else "rollback"
            msg = build_message(
                TOPIC_TRANSACTION,
                f"Transaction message {i} action={action}",
                tag="TagTransaction",
                keys=f"tx-{i}",
            )
            result = producer.send_message_in_transaction(msg, local_transaction_execute, None)
            print_send_result(f"transaction-{action}", i, result)
            time.sleep(1)

        print("Waiting 15s for transaction check callbacks...")
        time.sleep(15)
    finally:
        producer.shutdown()
        print("Transaction producer shutdown.")


if __name__ == "__main__":
    main()
