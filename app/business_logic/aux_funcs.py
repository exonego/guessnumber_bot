def num_check(text: str):
    num = int(text)
    if not 1 <= num <= 100:
        raise ValueError

    return num
