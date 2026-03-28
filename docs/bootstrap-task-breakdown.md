# 三战助手项目初始化与首批任务拆解

> 目标
>
> 这份文档解决两个问题：
>
> - 项目应该怎么搭骨架
> - 第一批任务具体先做什么

## 1. 初始化目标

初始化阶段的目标不是“功能多”，而是建立一套后面不会频繁推倒重来的结构。

初始化完成后，项目应该具备：

- 清晰的资源目录
- 清晰的代码目录
- 最小可运行入口
- 最小可执行 pipeline
- 最小日志链路
- 最小配置体系

## 2. 推荐目录结构

建议直接按下面的结构创建：

```text
SanzhanAssistant/
├── interface.json
├── README.md
├── docs/
│   ├── sanzhan-assistant-roadmap.md
│   ├── mvp-feature-checklist.md
│   └── bootstrap-task-breakdown.md
├── config/
│   ├── default.toml
│   ├── tasks.toml
│   └── safety.toml
├── resource/
│   ├── image/
│   │   ├── anchors/
│   │   ├── buttons/
│   │   ├── popups/
│   │   └── states/
│   ├── model/
│   │   └── ocr/
│   └── pipeline/
│       ├── startup/
│       ├── navigation/
│       ├── daily/
│       ├── recovery/
│       └── debug/
├── src/
│   ├── app/
│   ├── core/
│   ├── agent/
│   ├── planner/
│   ├── recognizers/
│   ├── actions/
│   ├── pipelines/
│   ├── safety/
│   ├── state/
│   ├── report/
│   └── utils/
├── reports/
│   ├── screenshots/
│   └── daily/
└── tests/
    ├── fixtures/
    └── smoke/
```

## 3. 目录职责说明

### 3.1 顶层文件

- `interface.json`
  - MAA 项目入口
  - 描述项目基础信息、资源入口和标准接口信息
- `README.md`
  - 项目简介
  - 启动方式
  - 环境要求

### 3.2 `config/`

- `default.toml`
  - 模拟器连接、分辨率、日志路径、运行开关
- `tasks.toml`
  - 开启哪些日常任务
- `safety.toml`
  - 风险等级、失败阈值、自动停止策略

### 3.3 `resource/`

- `resource/image/anchors/`
  - 页面定位锚点图
- `resource/image/buttons/`
  - 通用按钮素材
- `resource/image/popups/`
  - 常见弹窗素材
- `resource/image/states/`
  - 页面状态识别素材
- `resource/pipeline/`
  - MAA pipeline JSON

### 3.4 `src/`

- `src/app/`
  - 程序入口与启动流程
- `src/core/`
  - 运行时上下文、配置加载、任务注册
- `src/agent/`
  - 与 MAA 或外部能力交互的封装
- `src/planner/`
  - AI 规划层，第一版先做空骨架或轻量排序逻辑
- `src/recognizers/`
  - 状态识别、弹窗识别、区域识别
- `src/actions/`
  - 动态动作和异常恢复动作
- `src/pipelines/`
  - 任务编排层，把多个动作/识别组合成任务
- `src/safety/`
  - 风控、白名单、停止条件
- `src/state/`
  - 状态模型、状态快照、运行结果模型
- `src/report/`
  - 日志、截图、执行报告
- `src/utils/`
  - 通用工具函数

### 3.5 `reports/`

- `reports/screenshots/`
  - 失败截图
- `reports/daily/`
  - 每日执行摘要

### 3.6 `tests/`

- `tests/fixtures/`
  - 截图样本
- `tests/smoke/`
  - 冒烟测试

## 4. 第一版建议模块

第一版建议只建立下面这些核心模块。

### 4.1 运行入口

建议目标：

- 支持 `run_daily`
- 支持 `check_env`
- 支持 `debug_capture`

这样能快速区分：

- 环境是否正常
- 截图是否正常
- 日常主流程是否正常

### 4.2 状态模块

建议先定义：

- `PageState`
- `PopupState`
- `TaskResult`
- `RuntimeSnapshot`

核心原则：

- 状态命名统一
- 结果枚举统一
- 每个任务都能留下结构化结果

### 4.3 识别模块

建议第一版拆成 3 类识别器：

- `anchor_recognizer`
  - 判断是否处于某个页面
- `popup_recognizer`
  - 判断是否有常见弹窗
- `status_recognizer`
  - 读取一些关键状态，比如队列是否已满、是否可领取

### 4.4 动作模块

建议第一版拆成 3 类动作：

- `navigation_actions`
  - 返回主页、切换页面、进入子页面
- `daily_actions`
  - 领奖、收邮件、补征兵
- `recovery_actions`
  - 关闭弹窗、重试、回正

### 4.5 报告模块

建议第一版至少产出：

- 运行日志
- 失败截图
- 一份文本日报

## 5. 推荐初始化顺序

建议严格按下面顺序做，不要跳步。

### Step 1：建立空目录和配置骨架

产物：

- 目录结构创建完成
- `config/` 下 3 个基础配置文件
- `README.md`
- `interface.json`

完成标准：

- 项目结构清晰可读
- 运行参数有地方可放

### Step 2：打通最小运行入口

产物：

- 程序启动入口
- 环境检查命令
- 截图测试命令

完成标准：

- 能执行“检查环境”
- 能执行“截图调试”

### Step 3：实现主页面识别

产物：

- 主城识别
- 地图识别
- 邮件页识别
- 任务页识别

完成标准：

- 给定截图能返回结构化页面状态

### Step 4：实现导航与回正

产物：

- 从任意已知页面返回主城或主链路入口
- 常见弹窗关闭
- 未知状态停止

完成标准：

- 主流程不会轻易因为偏页而卡死

### Step 5：实现第一批日常任务

产物：

- 邮件领取
- 任务领取
- 奖励领取
- 一项资源补充任务

完成标准：

- 能跑通一轮最小日常

### Step 6：接入报告能力

产物：

- 结构化日志
- 失败截图
- 执行摘要

完成标准：

- 任何失败都能回看

## 6. 首批开发任务拆解

下面按“可以直接建 issue”的粒度来拆。

### A 组：项目骨架

- `A1` 创建基础目录结构
- `A2` 初始化 `interface.json`
- `A3` 编写 `README.md` 基础说明
- `A4` 创建默认配置文件
- `A5` 建立日志输出目录规则

### B 组：运行时基础

- `B1` 实现配置加载器
- `B2` 实现运行上下文对象
- `B3` 实现命令入口
- `B4` 实现环境检查逻辑
- `B5` 实现截图调试逻辑

### C 组：状态与识别

- `C1` 定义页面状态枚举
- `C2` 定义任务结果枚举
- `C3` 实现主城识别器
- `C4` 实现地图识别器
- `C5` 实现任务页识别器
- `C6` 实现邮件页识别器
- `C7` 实现通用弹窗识别器

### D 组：动作与导航

- `D1` 实现返回主页动作
- `D2` 实现打开任务页动作
- `D3` 实现打开邮件页动作
- `D4` 实现关闭奖励弹窗动作
- `D5` 实现未知状态停止逻辑

### E 组：首批日常

- `E1` 实现邮件奖励领取任务
- `E2` 实现任务奖励领取任务
- `E3` 实现通用奖励领取任务
- `E4` 实现资源/征兵补充任务
- `E5` 实现日常主流程编排

### F 组：可观测性

- `F1` 实现任务级日志
- `F2` 实现失败截图保存
- `F3` 实现运行摘要生成
- `F4` 实现日报文本输出

### G 组：安全与恢复

- `G1` 实现动作白名单
- `G2` 实现失败重试阈值
- `G3` 实现未知状态停止
- `G4` 实现常见网络异常恢复

## 7. 首批截图采集清单

这件事非常重要，建议尽早做，因为很多开发工作会被素材采集卡住。

第一批必须采的截图：

- 主城首页
- 世界地图
- 任务页
- 邮件页
- 征兵页
- 奖励弹窗
- 确认弹窗
- 网络异常弹窗
- 任意未知弹窗示例

采集要求：

- 同一分辨率
- 同一缩放
- 避免过多遮挡
- 尽量覆盖白天/夜间场景差异

## 8. 第一批配置项建议

建议第一版就显式配置这些参数：

```yaml
device:
  type: adb
  serial: emulator-5554

game:
  package_name: your.game.package
  channel: default
  language: zh-CN

runtime:
  profile: single-account
  save_screenshots_on_fail: true
  max_retry_per_task: 2

features:
  collect_mail: true
  collect_tasks: true
  collect_rewards: true
  recruit_safe_mode: true
  battle_auto_execute: false

safety:
  allow_only_low_risk_actions: true
  stop_on_unknown_popup: true
  stop_after_consecutive_failures: 3
```

## 9. 第一阶段完成定义

项目初始化阶段完成，建议以这几条为准：

- 项目目录建立完成
- 最小入口能运行
- 主页面识别跑通
- 至少 3 个日常动作能执行
- 失败日志和截图可回看

如果这些都达成，我们就已经不是“在想项目”，而是在“做产品第一版”。

## 10. 我建议的下一步执行顺序

如果按实际开工节奏排，我建议这样推进：

1. 先建目录和配置骨架
2. 先把 `interface.json` 和运行入口立住
3. 先做截图与页面识别
4. 再做导航与异常恢复
5. 再做日常主流程
6. 最后补日志、日报和 AI 轻量调度

## 11. 现在就可以继续做的事

如果你要我继续往下推进，最适合下一步直接开干的是下面三项中的任意一个：

1. 帮你把项目骨架文件直接创建出来
2. 帮你先写 `README.md`、`interface.json` 和基础配置模板
3. 帮你把 Python 侧的最小运行入口搭出来

从落地效率看，我最推荐第 `1 + 2 + 3` 一起做，直接把仓库从“只有文档”推进到“可开始写功能”的状态。
