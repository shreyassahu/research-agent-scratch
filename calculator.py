def calculate_expression(expression):
    try:
        return eval(expression)
    except Exception as e:
        return "Calculator didn't work, pls try again."