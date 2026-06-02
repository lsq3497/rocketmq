# RocketMQ Python 作业 Demo

基于 [apache/rocketmq-client-python](https://github.com/apache/rocketmq-client-python) 的基础实践脚本，对应课程任务 4–9。

> **平台说明**：Python 客户端依赖 `librocketmq`（C++ 动态库），**支持 macOS / Linux，不支持 Windows**。以下命令均按 **macOS** 可直接复制执行编写。

## 目录结构

| 脚本 | 任务 |
|------|------|
| `producer_04_normal.py` | 4. 普通消息发送 |
| `producer_05_orderly.py` | 5. 顺序消息发送 |
| `producer_06_delay.py` | 6.1 延时消息发送 |
| `producer_06_transaction.py` | 6.2 事务消息发送 |
| `producer_07_tag_sync.py` | 7.1 Tag 同步发送 |
| `producer_07_tag_async.py` | 7.2 Tag 异步发送 |
| `producer_07_tag_oneway.py` | 7.3 Tag OneWay 发送 |
| `consumer_08_push.py` | 8. Push 模式消费 |
| `producer_08_push_feed.py` | 8. 辅助：向 Push 消费 Topic 发消息 |
| `consumer_09_tag_filter.py` | 9.1 Tag 过滤消费 |
| `producer_09_tag_filter_feed.py` | 9.1 辅助：发送 TagA/B/C 测试消息 |
| `consumer_09_idempotent.py` | 9.2 消息幂等消费 |
| `producer_09_idempotent_feed.py` | 9.2 辅助：发送重复 business key 消息 |

## 0. 前置条件（macOS 一次性准备）

```bash
# 进入仓库根目录（按实际路径修改）
cd /path/to/rocketmq

# 安装 librocketmq（macOS 官方二进制）
wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0-bin-release.darwin.tar.gz
tar -xzf rocketmq-client-cpp-2.0.0-bin-release.darwin.tar.gz
cd rocketmq-client-cpp
sudo mkdir -p /usr/local/include/rocketmq /usr/local/lib
sudo cp include/* /usr/local/include/rocketmq/
sudo cp lib/* /usr/local/lib/
sudo install_name_tool -id "@rpath/librocketmq.dylib" /usr/local/lib/librocketmq.dylib
cd ..

# Python 虚拟环境与依赖
cd rocketmq-python-demos
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# 启动 RocketMQ 集群（另开终端，需先完成源码编译）
export ROCKETMQ_HOME=/path/to/rocketmq/distribution/target/rocketmq-5.4.0
sh $ROCKETMQ_HOME/bin/mqnamesrv
# 再开终端
export ROCKETMQ_HOME=/path/to/rocketmq/distribution/target/rocketmq-5.4.0
sh $ROCKETMQ_HOME/bin/mqbroker -n localhost:9876

# 创建 Demo 所需 Topic
export ROCKETMQ_HOME=/path/to/rocketmq/distribution/target/rocketmq-5.4.0
for t in HomeworkTopicNormal HomeworkTopicOrder HomeworkTopicDelay HomeworkTopicTransaction HomeworkTopicTag HomeworkTopicPush HomeworkTopicTagFilter HomeworkTopicIdempotent; do
  sh $ROCKETMQ_HOME/bin/mqadmin updateTopic -n localhost:9876 -t $t -c DefaultCluster
done

# 可选：自定义 NameServer 地址
export ROCKETMQ_NAMESRV=127.0.0.1:9876
```

## 1. 任务 4：普通消息

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_04_normal.py
```

## 2. 任务 5：顺序消息

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_05_orderly.py
```

## 3. 任务 6：延时消息 & 事务消息

### 6.1 延时消息（默认 delay level=3，约 10 秒后投递）

终端 1 — 启动消费者（监听延时 Topic）：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
export ROCKETMQ_TOPIC=HomeworkTopicDelay
python3 consumer_08_push.py
```

终端 2 — 发送延时消息：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_06_delay.py
```

### 6.2 事务消息

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_06_transaction.py
```

偶数序号消息本地提交（COMMIT），奇数序号回滚（ROLLBACK），并触发 Broker 事务回查。

## 4. 任务 7：Tag 同步 / 异步 / OneWay

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate

# 7.1 同步
python3 producer_07_tag_sync.py

# 7.2 异步（Python 客户端无原生 async API，使用回调 + 后台线程模拟）
python3 producer_07_tag_async.py

# 7.3 OneWay
python3 producer_07_tag_oneway.py
```

## 5. 任务 8：Push 模式消费

终端 1 — 启动 Push 消费者：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 consumer_08_push.py
```

终端 2 — 发送测试消息：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_08_push_feed.py
```

## 6. 任务 9：Tag 过滤 & 消息幂等

### 9.1 Tag 过滤（订阅 `TagA || TagC`）

终端 1：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 consumer_09_tag_filter.py
```

终端 2：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_09_tag_filter_feed.py
```

预期：消费者只打印 TagA、TagC 消息，TagB 被过滤。

### 9.2 消息幂等（按 business key 去重）

终端 1 — 首次运行前可重置状态：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
export RESET_IDEMPOTENT_STATE=1
python3 consumer_09_idempotent.py
```

终端 2：

```bash
cd /path/to/rocketmq/rocketmq-python-demos
source .venv/bin/activate
python3 producer_09_idempotent_feed.py
```

预期：`biz-1001`、`biz-1002` 等重复 key 第二次出现时输出 `SKIP duplicate`。

幂等状态持久化在 `.idempotent_state.json`（已加入 `.gitignore`）。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ROCKETMQ_NAMESRV` | `127.0.0.1:9876` | NameServer 地址 |
| `ROCKETMQ_TOPIC` | `HomeworkTopicPush` | `consumer_08_push.py` 监听的 Topic |
| `RESET_IDEMPOTENT_STATE` | 未设置 | 设为 `1` 时清空幂等状态文件 |

## 常见问题

1. **`ImportError: rocketmq dynamic library not found`**  
   按上文安装 `librocketmq` 并确认 `/usr/local/lib/librocketmq.dylib` 存在。

2. **发送失败 / No route info**  
   确认 NameServer、Broker 已启动，且对应 Topic 已通过 `mqadmin updateTopic` 创建。

3. **消费者无输出**  
   先启动消费者，再运行对应的 `producer_*_feed.py` 辅助脚本。
