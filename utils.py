def left_shift(binary: list, shift_amount: int):
    shift_amount = shift_amount % len(binary)
    return binary[shift_amount:] + binary[0: shift_amount]


def right_shift(lst: list, steps: int):
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            lst.append(lst.pop(0))
    else:
        for i in range(steps):
            lst.insert(0, lst.pop())
    return lst


# Binary to decimal conversion
def bin2dec(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal


# Decimal to binary conversion
def dec2bin(num):
    res = bin(num).replace("0b", "")
    if len(res) % 4 != 0:
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res


def xor(data_expanded: list, round_binary_keys: list):
    xor_values = []

    for i in range(len(data_expanded)):
        if data_expanded[i] == round_binary_keys[i]:
            xor_values.append(0)
        else:
            xor_values.append(1)

    return xor_values


# Метод для преобразования блока из бинарного представления в шестнадцатеричное представление
def bin2hex(binary_data: list, scale: int = 2):
    binary_str = ''.join(map(str, binary_data))
    hex_representation = hex(int(binary_str, scale))[2:].upper()  # Преобразование в шестнадцатеричное представление

    # Добавление нулей в начало, если строка короче 14 символов
    if len(hex_representation) < 14:
        hex_representation = '0' * (14 - len(hex_representation)) + hex_representation

    return hex_representation


def hex2bin(hex_data: str, scale: int = 16, num_of_bits: int = 64):
    binary_representation = bin(int(hex_data, scale))[2:].zfill(num_of_bits)  # Преобразование в двоичное представление
    return [int(bit) for bit in binary_representation]  # Преобразование строки в список целых чисел
