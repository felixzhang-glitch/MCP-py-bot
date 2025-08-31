from __future__ import annotations

import argparse
import ast
import operator as op
from typing import Union

from fastmcp import FastMCP


# Public MCP app instance
mcp = FastMCP(name="PyCalc-SSE")

# Allowed operators for safe evaluation
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


def _eval_node(node: ast.AST) -> Union[int, float]:
    """Evaluate a restricted AST node consisting of numeric constants and
    allowed unary/binary operations. Raises ValueError for disallowed syntax.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    raise ValueError("Unsupported expression or syntax")


def safe_eval(expr: str) -> Union[int, float]:
    """Safely evaluate a Python-style arithmetic expression.

    Supported: +, -, *, /, //, %, **, parentheses, unary +/-; numeric constants only.
    """
    tree = ast.parse(expr, mode="eval")
    result = _eval_node(tree.body)
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


@mcp.tool
def calc(expr: str) -> Union[int, float]:
    """Compute an arithmetic expression (safe subset).

    Example: "789798*6786786/321321"
    """
    return safe_eval(expr)


def main() -> None:
    parser = argparse.ArgumentParser(description="PyCalc-SSE server")
    parser.add_argument("--transport", default="sse", help="Transport (sse)")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=18000, help="Bind port")
    args = parser.parse_args()

    mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

