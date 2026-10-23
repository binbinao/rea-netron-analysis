# rea-netron-analysis

逆向本机 `/Applications/Netron.app`，目的不是存档，是**给 Rust 版 `ai-model-viewer` 抄架构**。

Netron 是目前最通用的模型查看器，支持 67 种模型格式。它的架构决定了「支持一个新格式要写多少代码」这件事的量级——这篇拆解给出的就是那个量级，以及哪些设计值得抄、哪些是 Electron 时代的包袱。

## 读什么

**[`reports/netron-architecture.md`](reports/netron-architecture.md)** —— 主文章。六节，每节一个可复核的事实 + 一条「抄 / 不抄」的判断。

## 目录

| 路径 | 说明 |
|---|---|
| `reports/netron-architecture.md` | 架构拆解文章 |
| `evidence/netron-9.3.2-analyze-javascript-application.json` | REA 静态分析完整证据，60MB |
| `scripts/analyze.sh` | 复现静态分析 |
| `scripts/summarize.py` | 把 60MB JSON 压成人读摘要 |

## 复现

```bash
python3 scripts/summarize.py                 # 读证据，1 秒
./scripts/analyze.sh                         # 重跑静态分析，约 70 秒
```

需要 Node.js >=22.19 和 npm。REA 通过 npx 调用，无需全局安装。

## 目标版本

Netron **9.3.2**，目录 sha256 `013c98310baaaa9e485eb760aeae6d3abb06b824156d73e1167bab61c79b6547`。

分析途中 Netron 自动更新过一次（9.3.1 → 9.3.2）。文章里的所有数字都以 9.3.2 为准。

源码级证据来自解包 `app.asar` 后的 `source/*.js`（179 个文件）。文章引用的每段代码都能在其中定位。

## 边界

全部结论基于**静态**分析。行数、字节数、注册表条数、IPC 通道名是可直接复核的计数；「为什么这么设计」是从代码结构反推的判断，不是作者的说明。

未做运行时观察，未做逐条 IPC 流量抓取。

## 相关

- 目标项目：[ai-model-viewer](../ai-model-viewer) —— Rust 写的多格式模型图查看器
- REA：https://github.com/morluto/rea
