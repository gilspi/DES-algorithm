def shift_func(binary: list, shift_amount: int):
    shift_amount = shift_amount % len(binary)
    return binary[shift_amount:] + binary[:shift_amount]


# Binary to decimal conversion
def bin2dec(binary_number: str):
    if not isinstance(binary_number, str):
        raise TypeError("Входной аргумент должен быть строкой")

    decimal_representation = int(binary_number, 2)

    return decimal_representation


def dec2bin(decimal_number: int, n=4):
    if not isinstance(decimal_number, int):
        raise TypeError("Входной аргумент должен быть целым числом")

    binary_representation = bin(decimal_number)[2:].zfill(n)
    return binary_representation


def xor(data_expanded: list, round_binary_keys: list):
    xor_values = []

    for i in range(len(data_expanded)):
        if data_expanded[i] == round_binary_keys[i]:
            xor_values.append(0)
        else:
            xor_values.append(1)
    return xor_values


# Метод для преобразования блока из бинарного представления в шестнадцатеричное представление
def bin2hex(data, scale: int = 2, is_needed: bool = False, n: int = 14):
    if isinstance(data, list):
        binary_str = ''.join(map(str, data))
    elif isinstance(data, str):
        binary_str = data
    else:
        raise TypeError("Данные должны быть либо списком, либо строкой")

    hex_representation = hex(int(binary_str, scale))[2:].upper()  # Преобразование в шестнадцатеричное представление

    # Добавление нулей в начало
    if len(hex_representation) < n and is_needed:
        hex_representation = '0' * (n - len(hex_representation)) + hex_representation

    return hex_representation


def hex2bin(hex_data: str, scale: int = 16, num_of_bits: int = 64):
    binary_representation = bin(int(hex_data, scale))[2:].zfill(num_of_bits)  # Преобразование в двоичное представление
    return [int(bit) for bit in binary_representation]  # Преобразование строки в список целых чисел
