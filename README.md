## About

使用 Jenkins 自动化评估 OpenCV 在启用/禁用 RISC-V Vector 扩展时的性能差异

## 目录结构

- `./jenkins-docker` : dockerfile / docker compose 配置文件
- `output_sample` : 用于调试 python 脚本的样本数据
- `Jenkinsfile` : Jenkins pipeline 文件
- `test_report.py` : 自动处理测试结果生成测试报告的代码
- `test.md` : 前期手测的数据集（没啥用）
- `toolchain-riscv64.cmake` : cmake 交叉编译工具链配置文件

## 使用条件

- 安装 `riscv-gnu-toolchain` 工具链，[参考这里](https://leetfs.com/tips/riscv-gnu-toolchain)。
- 安装 `python` 。
- 已经添加了支持 Vector 扩展的 RISC-V 节点。

## 使用方法

### 配置所需环境

本仓库 dockerfile 已经配好了所需环境，可以直接使用。

- 在 /etc/docker/下新建文件夹 jenkins。
- 将 `jenkins-docker` 内的文件放入 jenkins 文件夹中。
- 在 `jenkins` 文件夹下执行 `sudo docker compose up`。

### 使用 Jenkinsfile

1. Jenkins 面板 / 新建任务 / 流水线
1. 流水线定义选择 Pipeline script from SCM
1. SCM 选项选择 Git
1. Repository URL 填写本仓库 URL 或 fork 出的 url
1. 点击立即构建
