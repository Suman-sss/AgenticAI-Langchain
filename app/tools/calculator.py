import ast
import operator

from langchain_core.tools import tool


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


class CalculatorError(Exception):
    pass


def calculate(expression: str) -> float:
    try:
        parsed = ast.parse(expression, mode="eval")
        return float(_evaluate_node(parsed.body))
    except Exception as exc:
        raise CalculatorError(f"Invalid calculation: {expression}") from exc


@tool
def calculator_tool(expression: str) -> str:
    """
    Safely evaluate a mathematical expression and return the result.
    Use this tool for arithmetic calculations such as addition,
    subtraction, multiplication, division, modulus, and powers.
    """
    try:
        result = calculate(expression)
        return str(result)
    except CalculatorError as exc:
        return str(exc)


def _evaluate_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise CalculatorError("Unsupported operator")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_node(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise CalculatorError("Unsupported unary operator")
        return operator_func(operand)

    raise CalculatorError("Unsupported expression")
