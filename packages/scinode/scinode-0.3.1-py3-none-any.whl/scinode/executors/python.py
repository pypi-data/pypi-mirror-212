def operator(x, y, operator="+"):
    """Check all python operators, and apply to x and y. Return a tuple of results."""
    if operator == "+":
        results = (x + y,)
    elif operator == "-":
        results = (x - y,)
    elif operator == "*":
        results = (x * y,)
    elif operator == "/":
        results = (x / y,)
    elif operator == "//":
        results = (x // y,)
    elif operator == "%":
        results = (x % y,)
    elif operator == "**":
        results = (x**y,)
    elif operator == "==":
        results = (x == y,)
    elif operator == "!=":
        results = (x != y,)
    elif operator == ">":
        results = (x > y,)
    elif operator == "<":
        results = (x < y,)
    elif operator == ">=":
        results = (x >= y,)
    elif operator == "<=":
        results = (x <= y,)
    elif operator == "and":
        results = (x and y,)
    elif operator == "or":
        results = (x or y,)
    else:
        raise ValueError("Operator not supported: %s" % operator)
    return results


def setattr(source, name, value):
    """set attribute."""
    import builtins

    builtins.setattr(source, name, value)
    return source


def getitem(source, index):
    """Get items from a array."""

    if isinstance(source, dict):
        result = source[index]
    else:
        # list or array
        if type(index) in (int, float):
            index = [index]
        result = [source[i] for i in index]
        if len(result) == 1:
            result = result[0]
    results = (result,)
    return results


def setitem(source, index, value):
    """Set items value for a array."""
    if type(index) in (int, float):
        index = [index]
    index = [int(i) for i in index]
    if isinstance(source, list):
        for i in index:
            source[i] = value[i]
    else:
        source[index] = value
    return source
