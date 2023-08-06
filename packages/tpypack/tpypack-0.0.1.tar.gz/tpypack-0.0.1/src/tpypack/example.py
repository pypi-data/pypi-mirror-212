import numpy as np

def logger(func):
    func_calls = 0
    def wrapper(*args, **kwargs):
        nonlocal func_calls
        print(f"Function calls is {func_calls}")
        print(f"Function name is {func.__name__}")
        out = func(*args, **kwargs)
        print(out)
        return out

    return wrapper

@logger
def sum(a, b):
    return a + b

if __name__ == "__main__":
    sum(12, 5)
