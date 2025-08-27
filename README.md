# PyCalc-SSE

PyCalc-SSE 是一个基于 FastMCP 框架的简单计算器服务，通过 Server-Sent Events (SSE) 方式暴露 HTTP 服务。该服务提供了一个安全的算术表达式计算功能，支持基本的数学运算符，包括加法、减法、乘法、除法、整除、取模和幂运算。

## 服务配置

```json
{
  "command": "uvx",
  "args": ["pycalc-sse@latest", "--transport", "sse", "--host", "0.0.0.0", "--port", "18000"]
}
```

## 功能

- 提供安全的算术表达式计算功能
- 支持的运算符：
  - 基本运算：`+`, `-`, `*`, `/`, `//`, `%`, `**`
  - 括号：`()`
  - 一元运算符：`+`, `-`
- 仅接受数字常量，不支持变量或其他 Python 语法
- 通过 SSE 方式提供 HTTP 服务

## 使用方法

1. 安装依赖：
   ```bash
   pip install fastmcp
   ```

2. 运行服务：
   ```bash
   python server_sse.py
   ```
   服务将在 `http://0.0.0.0:18000/sse` 上启动

3. 连接服务并调用工具：
   - 使用支持 SSE 的客户端连接到 `/sse` 端点
   - 调用 `calc` 工具，传入 `expr` 参数进行计算
   - 示例表达式：`"789798*6786786/321321"`

## 安全特性

- 使用 Python `ast` 模块解析表达式，避免 `eval` 的安全风险
- 限制只允许特定的二元运算符和一元运算符
- 只接受数字常量，拒绝其他类型的表达式节点
- 对不支持的表达式或语法抛出明确的错误

## 代码结构

- `server_sse.py`: 主服务文件
  - `_ALLOWED_BINOPS`: 允许的二元运算符映射
  - `_ALLOWED_UNARYOPS`: 允许的一元运算符映射
  - `_eval_node()`: 递归计算 AST 节点
  - `safe_eval()`: 安全的表达式求值函数
  - `calc()`: 作为 MCP 工具暴露的计算函数