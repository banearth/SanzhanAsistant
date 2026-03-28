# SanzhanAssistant

基于 MaaFramework 的《三国志·战略版》助手项目。

当前阶段目标：

- 先做稳定的日常自动化 MVP
- 再引入 AI 做任务排序与状态解释
- 最后再推进到低风险作战建议与半自动执行

## 当前仓库状态

当前仓库已经具备：

- 路线规划文档
- MVP 功能清单
- 项目初始化与任务拆解文档
- 第一版项目目录骨架
- 第一版 `interface.json` 草案
- 第一版 Python 入口骨架
- MuMu ADB 直连与真实截图采集能力

当前仓库还没有完成：

- 实际的 MAA 识别素材
- 实际可用的 pipeline 节点链路
- 自定义识别/动作实现
- 模拟器接入与真机验证

## 三战领域说明

这个项目的日常定义并不是“像单机手游那样把通用奖励领一遍就结束”。

当前已经确认的一条关键业务认知是：

- 三战是强社交协作玩法
- `同盟` 页签下的任务/目标，才是更有意义的核心日常
- 真正重要的循环通常是“查看同盟目标 -> 派兵 -> 战斗 -> 回看结果 -> 再次派兵”

因此，项目后续的核心自动化方向会优先围绕 `ALLIANCE_TASK_CENTER` 和派兵作战循环来设计，而不是只做普通领奖脚本。

## 文档

- [路线规划](docs/sanzhan-assistant-roadmap.md)
- [MVP 功能清单](docs/mvp-feature-checklist.md)
- [初始化与任务拆解](docs/bootstrap-task-breakdown.md)

## 推荐开发顺序

1. 安装 Python 3.11+ 并确认 `python` 在 PATH 中可用
2. 安装 MaaFramework 运行环境与目标控制方式
3. 采集第一批页面截图素材
4. 先实现主页面识别和导航回正
5. 再实现邮件/任务/奖励/征兵等日常链路

## Python 入口

当前预留了一个轻量入口：

```powershell
python -m src.app.main check-env
python -m src.app.main probe-device
python -m src.app.main run-daily
python -m src.app.main debug-capture
python -m src.app.main inspect-fixtures
python -m src.app.main capture-screen --name home_city --fixture
python -m src.app.main capture-screen --name battle-report --fixture
```

说明：

- 这几个命令当前还是骨架状态
- 它们已经能读配置、生成基础报告
- 还没有真正接入 MAA 控制链路

## 配置

配置文件位于：

- `config/default.toml`
- `config/tasks.toml`
- `config/safety.toml`

## 说明

`interface.json` 当前是按 MaaFramework Project Interface V2 文档整理出的第一版草案，目的是先固定项目入口结构。后续等我们选定具体控制方式、资源包和 agent 运行方式后，再补齐任务节点、选项配置和实际识别链路。
