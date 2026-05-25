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
