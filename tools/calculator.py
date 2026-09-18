import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        return evaluate(tree.body)

    except Exception:
        raise ValueError("Invalid mathematical expression.")


def evaluate(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):

        if type(node.op) not in OPERATORS:
            raise ValueError("Unsupported mathematical operator.")

        left = evaluate(node.left)
        right = evaluate(node.right)

        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):

        if type(node.op) not in OPERATORS:
            raise ValueError("Unsupported mathematical operator.")

        operand = evaluate(node.operand)

        return OPERATORS[type(node.op)](operand)

    raise ValueError("Invalid mathematical expression.")