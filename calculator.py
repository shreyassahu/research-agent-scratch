from simpleeval import simple_eval

def calculate_expression(expression):
    try:
        return simple_eval(expression)
    except Exception as e:
        return "Calculator didn't work, pls try again."