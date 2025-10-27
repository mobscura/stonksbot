def get_signal(message):
    signal = False
    msg = message.text.strip().split(' >>>>> ')
    if len(msg) > 3:
        signal = True
    return signal

def get_parameter(message):
    signal = message.text.strip().split(' >>>>> ')
    coin_name = signal[2]
    coin_flag = signal[3]
    symbol = coin_name + 'USDT'
    return coin_name, coin_flag, symbol

def abbre_numbers(num: float) -> str:
    if 1000 <= num < 1_000_000:
        return f"{round(num / 1_000, 2)}K"
    elif 1_000_000 <= num < 1_000_000_000:
        return f"{round(num / 1_000_000, 2)}M"
    elif 1_000_000_000 <= num < 1_000_000_000_000:
        return f"{round(num / 1_000_000_000, 2)}B"
    elif num >= 1_000_000_000_000:
        return f"{round(num / 1_000_000_000_000, 2)}T"
    return str(num)

def commas(number: float) -> str:
    number_string = str(number)
    parts = number_string.split(".")
    integer_part = parts[0]
    decimal_part = "." + parts[1] if len(parts) > 1 else ""
    formatted_integer_part = "{:,}".format(int(integer_part))
    return formatted_integer_part + decimal_part

def format_decimal(value: float, max_decimals: int = 8) -> str:
    trimmed = f"{value:.{max_decimals}f}"

    if '.' in trimmed:
        trimmed = trimmed.rstrip('0').rstrip('.')

    parts = trimmed.split(".")
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else ""

    formatted_integer = "{:,}".format(int(integer_part))

    return f"{formatted_integer}.{decimal_part}" if decimal_part else formatted_integer