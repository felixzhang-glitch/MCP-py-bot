from __future__ import annotations
from fastmcp import FastMCP
from typing import Union
import ast
import operator as op

mcp = FastMCP(name="PyCalc-SSE")

_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}
_ALLOWED_UNARYOPS = {ast.UAdd: op.pos, ast.USub: op.neg}

def _eval_node(node) -> Union[int, float]:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("只接受数字常量")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    raise ValueError("不支持的表达式或语法")

def safe_eval(expr: str) -> Union[int, float]:
    tree = ast.parse(expr, mode="eval")
    result = _eval_node(tree.body)
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result

@mcp.tool
def calc(expr: str) -> Union[int, float]:
    """
    计算一个 Python 风格的算术表达式（安全子集）。
    支持: +, -, *, /, //, %, **, 括号, 一元+/-；仅数字常量。
    示例: "789798*6786786/321321"
    """
    return safe_eval(expr)

if __name__ == "__main__":
    # 以 SSE 方式暴露为 HTTP 服务（默认 /sse 路由）
    # 可按需改 host/port
    mcp.run(transport="sse", host="0.0.0.0", port=18000)
