"""
Calc function used for unit testing
"""

def add(x:int, y:int) -> int:
    """
    returns sum of two numbers, throws exception if their types are not integer
    """
    try:
        return x+y
    except TypeError:
        return "Invalid inputs passed"

def subtract(x:int, y:int) -> int:
    """
    returns difference of two numbers, throws exception if their types are not integer
    """
    try:
        return x-y
    except TypeError:
        return "Invalid inputs passed"


if __name__ == "__main__":
    print(add(4,6))
    print(add('a',4))

