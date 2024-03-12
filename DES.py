from PBox import PBox

from utils import bin2hex, hex2bin, bin2dec, dec2bin, shift_func, xor


class DES:
    def __init__(self, main_key: str):
        self.main_key = hex2bin(main_key)
        self.PC_1 = PBox.get_key_initial_permutation()
        self.PC_2 = PBox.get_key_finish_permutation()
        self.PC_I = PBox.get_initial_permutation()
        self.PC_F = PBox.get_finish_permutation()
        self.P_EXPAND = PBox.get_single_expand_permutation()
        self.SBOX_TABLES = PBox.get_sbox_tables()
        self.STRAIGHT_ROUND = PBox.get_straight_round_permutation()

    @staticmethod
    def get_matrix(data: list):
        for ind, el in enumerate(data, start=1):
            print(f'{ind}={el} ', end='')
            if ind % 8 == 0 and ind != len(data):
                print()
        print()

    def permute(self, data: list, arr: list, n: int, permute_text: str = ''):
        permutation = []
        for i in range(0, n):
            permutation.append(data[arr[i] - 1])
        # print(f'{permute_text} permutation = {"".join(map(str, permutation))}'.strip().capitalize())
        return permutation

    def encrypt(self, pt: str = ''):
        text = self.main_key if not len(pt) else hex2bin(pt)
        data = self.permute(text, self.PC_I, 64, 'after initial')
        print(f'L0R0={bin2hex(data)}')
        # getting 56 bit key from 64 bit using the parity bits
        round_binary_keys, round_keys, cd_blocks = self.generate_rounds()
        # Splitting
        left = data[0:32]
        right = data[32:64]

        for i in range(16):  # TODO n=16
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = self.permute(right, self.P_EXPAND, 48)
            # XOR RoundKey[i] and right_expanded
            print(f"Round={i+1}  C{i+1}D{i+1}={cd_blocks[i]}  Round key={round_keys[i]}")
            print(f'CP{i+1}={bin2hex(right_expanded)}')
            print(f'right expanded={right_expanded}')
            print(f'round_binary_keys[{i}]={round_binary_keys[i]}')
            xor_x = xor(right_expanded, round_binary_keys[i])
            print(f'CP{i+2}(xor_x)={bin2hex(xor_x)}')
            # S-boxes: substituting the value from s-box table by calculating row and column
            output_sbox = ""
            for j in range(0, 8):
                row = bin2dec(int(f'{xor_x[j * 6]}{xor_x[j * 6 + 5]}'))
                col = bin2dec(int(f'{xor_x[j * 6 + 1]}{xor_x[j * 6 + 2]}{xor_x[j * 6 + 3]}{xor_x[j * 6 + 4]}'))
                val = self.SBOX_TABLES[j][row][col]
                output_sbox += dec2bin(val)
                print(f'S{i+1}   row={row}   col={col}   val={val}   output={dec2bin(val)}')

            print(f'CP{i+3}=S1S2S3S4S5S6S7S8={output_sbox}={bin2hex(list(map(int, output_sbox)))}')
            # Straight D-box: After substituting rearranging the bits
            output_pbox = self.permute(list(map(int, output_sbox)), self.STRAIGHT_ROUND, 32)
            print(f'CP{i+4}={"".join(map(str, output_pbox))}={bin2hex(output_pbox)}')

            # XOR left and SBox
            result = xor(output_pbox, left)
            print(f'L0={"".join(map(str, left))}   CP{i+4}={"".join(map(str, output_pbox))}   result={"".join(map(str, right))}={bin2hex(right)}')
            left = result
            print(f'L1={"".join(map(str, left))}={bin2hex(left)}')
            # Swapper
            if i != 15:
                left, right = right, left

        # Combination
        output = left + right
        print(f'L16R16={bin2hex(output)}')

        # Final permutation: final rearranging of bits to get cipher text
        cipher_text = self.permute(output, self.PC_F, 64, 'finish')
        print(f'Cipher text={bin2hex(cipher_text)}')
        return cipher_text

    def generate_rounds(self, msg: str = 'right'):
        round_binary_keys, round_keys, cd_blocks = [], [], []
        self.main_key = self.permute(self.main_key, self.PC_1, 56, 'round keys')
        ci, di = self.main_key[0: 28], self.main_key[28: 56]

        for i in range(1, 17):
            shift = 1 if i in [1, 2, 9, 16] else 2
            ci, di = shift_func(ci, shift), shift_func(di, shift)
            cd_block = ci + di
            cd_blocks.append(bin2hex(cd_block, is_needed=True))
            k = self.permute(cd_block, self.PC_2, 48)
            round_binary_keys.append(k)
            round_keys.append(bin2hex(k))

        return round_binary_keys, round_keys, cd_blocks


pt = "123456ABCD132536"
key = "AABB09182736CCDD"

des = DES(key)
des.encrypt(pt)

# CoDo  = 2E8CCE30C815C5
# C1D1 = 5D199C61902B8A
# k1 = 4463EF0C7445
# C2D2 = BA3338C3205714


# TODO у меня есть правильные ответы и там c8d8=0CEB0F033E8CFC c9d9=19D61E067D19F8 а у меня вот такой вот ответ
# Round=1  C1D1=C3C033A33F0CFA  Round key=181C5D75C66D
# Round=2  C2D2=61E019D19F867D  Round key=3330C5D9A36D
# Round=3  C3D3=5878067467E19F  Round key=251B8BC717D0
# Round=4  C4D4=D61E019D19F867  Round key=99C31397C91F
# Round=5  C5D5=7587806F467E19  Round key=C2C1E96A4BF3
# Round=6  C6D6=9D61E017D19F86  Round key=6D5560AF7CA5
# Round=7  C7D7=67587809F467E1  Round key=2765708B5BF
# Round=8  C8D8=19D61E067D19F8  Round key=84BB4473DCCC
# Round=9  C9D9=0CEB0F033E8CFC  Round key=34F822F0C66D
# Round=10  C10D10=033AC3C0CFA33F  Round key=708AD2DDB3C0
# Round=11  C11D11=00CEB0FC33E8CF  Round key=C1948E87475E
# Round=12  C12D12=C033AC3F0CFA33  Round key=69A629FEC913
# Round=13  C13D13=F00CEB0FC33E8C  Round key=DA2D032B6EE3
# Round=14  C14D14=3C033AC3F0CFA3  Round key=6EDA4ACF5B5
# Round=15  C15D15=0F00CEBCFC33E8  Round key=4568581ABCCE
# Round=16  C16D16=878067567E19F4  Round key=194CD072DE8C
# как это исправить

