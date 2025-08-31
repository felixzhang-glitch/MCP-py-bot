# PyCalc-SSE

一个基于 FastMCP 的极简计算器服务，通过 SSE 暴露 HTTP 接口。提供安全的算术表达式求值（白名单 AST），功能不变但项目已重构为标准工程布局（src layout）。需要 Python 3.10+。

## 功能
- 支持运算：`+` `-` `*` `/` `//` `%` `**`、括号、以及一元 `+/-`
- 仅接受数字常量；拒绝变量与任意 Python 语法
- 通过 SSE 暴露为 HTTP 服务（默认 `/sse`）

## 安装与运行
```bash
# 推荐使用虚拟环境
python -m venv .venv && source .venv/bin/activate

# 开发安装（可编辑）
pip install -e .

# 以 CLI 方式运行
pycalc-sse --host 0.0.0.0 --port 18000

# 或以模块方式运行
python -m pycalc_sse.server --host 0.0.0.0 --port 18000
```
服务默认在 `http://0.0.0.0:18000/sse` 暴露。

## 客户端使用（示意）
- 连接到 `/sse` 端点
- 调用工具 `calc(expr: str)`，例如：`"789798*6786786/321321"`

## 安全性
- 使用 `ast` 解析并严格限定节点与运算符，避免 `eval` 风险
- 对非数字常量或不支持的语法抛出明确错误

## 代码结构
- `src/pycalc_sse/server.py`: 入口与服务定义
- `src/pycalc_sse/__init__.py`: 包元数据与导出
- `pyproject.toml`: 打包与依赖配置（入口：`pycalc-sse`）

## 开发
- 代码风格：PEP8、4 空格缩进、适度类型标注
- 打包：`python -m build`（需先 `pip install build`）

## 提交前检查（pre-commit）
```bash
pip install pre-commit
pre-commit install

# 手动检查全部文件
pre-commit run --all-files
```
已配置的钩子：Ruff 格式化/检查、pytest（快速回归）。
