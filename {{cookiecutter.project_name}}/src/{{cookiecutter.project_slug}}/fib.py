import argparse

from . import __version__ as VERSION


def fib(n: int) -> int:
    """计算斐波那契数列

    Args:
        n ([int]): [次数]

    Returns:
        [int]: [计算结果]
    """
    if n < 2:
        return n

    return fib(n - 1) + fib(n - 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s Version: {VERSION}",
        help="Show program's version number and exit.",
    )
    parser.add_argument(
        "n",
        type=int,
        help="The number of Fibonacci sequence to calculate.",
    )
    args = parser.parse_args()
    result = fib(args.n)
    print(f"The {args.n}th Fibonacci number is: {result}")
