## Apache RocketMQ 本地快速上手（Windows 从源码开始）

本文档面向 **Windows 开发环境**，从零开始指导你在本机编译、启动 Apache RocketMQ，并完成最基础的发送 / 接收消息功能。所有命令默认在 **Windows（PowerShell 或 CMD）** 中执行。

---

## 一、环境准备

- **操作系统**
  - Windows 10 或更高版本（64 位）。

- **JDK**
  - 版本：JDK 8 或以上（推荐 8/11 LTS）。
  - 安装后，确保 `JAVA_HOME` 已配置，并且命令行能执行：

```powershell
java -version
```

- **Maven**
  - 版本：建议 Maven 3.6+。
  - 安装后，确保命令行能执行：

```powershell
mvn -version
```

- **Git（可选，但推荐）**
  - 用于从 Git 仓库获取和更新代码。

- **IDE（可选）**
  - 如 IntelliJ IDEA / VS Code / Eclipse，用于查看和开发代码。

---

## 二、获取源码

如果你已经从 Git 克隆了本仓库，可以跳过本节。

```powershell
cd D:\code
git clone https://github.com/apache/rocketmq.git
cd .\rocketmq
```

> 说明：上面的 `D:\code\rocketmq` 路径仅为示例，请根据你本地实际路径调整。

---

## 三、在 Windows 上从源码编译

在项目根目录（即 `pom.xml` 所在目录）执行 Maven 打包命令：

```powershell
cd D:\code\rocketmq
mvn -Prelease-all -DskipTests clean install -U
```

- **常见耗时**：第一次编译会下载大量依赖，耗时可能在 5–20 分钟。
- **编译成功标志**：命令结尾出现 `BUILD SUCCESS`。

编译完成后，会在 `distribution\target` 目录生成类似下面的二进制包（版本号可能略有不同）：

- `distribution\target\rocketmq-5.4.0\rocketmq-5.4.0`

后续所有运行命令都以该目录为基础。

---

## 四、配置环境变量（ROCKETMQ_HOME）

为了方便脚本运行，建议配置 `ROCKETMQ_HOME` 环境变量，指向刚刚生成的二进制目录。

假设你的项目路径为：

- `D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0`

### 1. 临时设置（当前窗口有效）

在 PowerShell 中：

```powershell
$env:ROCKETMQ_HOME = "D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0"
cd $env:ROCKETMQ_HOME\bin
```

在 CMD 中：

```cmd
set ROCKETMQ_HOME=D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0
cd /d %ROCKETMQ_HOME%\bin
```

### 2. 永久设置（系统环境变量）

在 Windows 桌面上：

1. 右键点击 “此电脑” / “我的电脑” → 选择 “属性”。
2. 点击左侧 “高级系统设置”。
3. 点击 “环境变量(N)...”。
4. 在 “系统变量” 中点击 “新建”：
   - 变量名：`ROCKETMQ_HOME`
   - 变量值：`D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0`
5. 确认后，重新打开一个新的终端窗口使配置生效。

---

## 五、启动核心组件（NameServer + Broker）

以下步骤假设你已经进入 `bin` 目录：

```powershell
cd D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0\bin
```

### 1. 启动 NameServer

在一个新的终端窗口（PowerShell 或 CMD 均可）中执行：

```powershell
cd D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0\bin
mqnamesrv.cmd
```

- 若启动成功，终端中会出现类似：
  - `The Name Server boot success...`
- 服务默认监听地址：`0.0.0.0:9876`
- 请保持该窗口 **不要关闭**。

### 2. 启动 Broker

再打开一个新的终端窗口，执行：

```powershell
cd D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0\bin
mqbroker.cmd -n 127.0.0.1:9876 autoCreateTopicEnable=true
```

- 若启动成功，终端中会出现类似：
  - `The broker[broker-a, 192.168.x.x:10911] boot success...`
- 同样请保持该窗口 **不要关闭**。

> 提示：`autoCreateTopicEnable=true` 仅适合本地开发测试，生产环境不建议开启。

---

## 六、发送与接收测试消息（最基础功能）

在 NameServer 与 Broker 都正常运行的前提下，可以使用自带的 `tools.cmd` 工具脚本进行简单的发送 / 接收验证。

### 1. 发送消息

在新的终端窗口中执行：

```powershell
cd D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0\bin

# 设置 NameServer 地址（临时环境变量）
set ROCKETMQ_HOME=%cd%\..
set NAMESRV_ADDR=127.0.0.1:9876

# 发送示例消息（Java 示例 Producer）
./tools.cmd org.apache.rocketmq.example.quickstart.Producer
```

- 执行后，终端会输出发送消息的日志，若无报错即代表发送成功。

### 2. 接收消息

继续在同一个（或新的）终端中执行：

```powershell
cd D:\code\rocketmq\distribution\target\rocketmq-5.4.0\rocketmq-5.4.0\bin

set ROCKETMQ_HOME=%cd%\..
set NAMESRV_ADDR=127.0.0.1:9876

# 接收消息（Java 示例 Consumer）
./tools.cmd org.apache.rocketmq.example.quickstart.Consumer
```

- 能在终端看到消费日志（打印收到的消息内容），说明最基础的发送 / 接收链路已正常工作。

> 说明：示例 Producer / Consumer 属于简单的 Java 样例，适合用于本地功能验证。

---

## 七、常见问题排查

- **问题 1：`java` 或 `mvn` 不是内部或外部命令**
  - 检查是否已安装 JDK / Maven。
  - 确认 `JAVA_HOME`、`MAVEN_HOME` 和 `Path` 环境变量中包含对应的 `bin` 目录。

- **问题 2：端口 9876 或 10911 被占用**
  - 使用下面命令查看占用端口的进程：

```powershell
netstat -ano | findstr "9876"
netstat -ano | findstr "10911"
```

  - 若被其他程序占用，可结束该进程后重试，或修改 Broker 启动参数使用其他端口。

- **问题 3：Broker 启动后立刻退出**
  - 检查是否已经正确启动 NameServer。
  - 确认 `-n 127.0.0.1:9876` 地址与实际 NameServer 地址一致。

- **问题 4：示例 Producer / Consumer 无法连接**
  - 确认 `NAMESRV_ADDR` 环境变量设置正确。
  - 确认防火墙未阻止本机端口访问。

---

## 八、下一步

当你完成上述步骤后，说明你已经能够在 Windows 上：

1. 从源码编译 Apache RocketMQ；
2. 启动本地的 NameServer 和 Broker；
3. 使用示例程序完成最基础的发送 / 接收消息。

接下来，你可以进一步：

- 阅读本仓库根目录下的英文 `README.md` 和官方文档；
- 学习如何创建主题、消费组以及各种高级特性（顺序消息、事务消息、延时消息等）；
- 配合 `rocketmq-dashboard` 进行可视化管理与监控。

