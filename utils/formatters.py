def inr(value):
    """
    Formats a number using the Indian numbering system.

    Examples
    --------
    980 -> ₹980
    8450 -> ₹8,450
    98450 -> ₹98,450
    123456 -> ₹1,23,456
    1234567 -> ₹12,34,567
    12345678 -> ₹1,23,45,678
    """

    if value is None:
        return "₹0"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return "₹0"

    negative = value < 0
    value = abs(value)

    integer = int(value)
    decimal = value - integer

    s = str(integer)

    if len(s) > 3:
        last3 = s[-3:]
        remaining = s[:-3]

        groups = []

        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            groups.insert(0, remaining)

        formatted = ",".join(groups) + "," + last3
    else:
        formatted = s

    if decimal:
        formatted += f"{decimal:.2f}"[1:]

    if negative:
        formatted = "-" + formatted

    return f"₹{formatted}"