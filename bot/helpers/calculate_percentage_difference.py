from typing import Union


def calculate_percentage_difference(is_all_time: bool, current: Union[int, float], before: Union[int, float]):
    if is_all_time:
        return ""
    if before == 0:
        return f"(+{current}%)"

    percentage_diff = round(((current - before) / before) * 100, 2)
    sign = "+" if percentage_diff >= 0 else ""
    return f"({sign}{percentage_diff}%)"
