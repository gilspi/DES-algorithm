from PBox import PBox

from utils import bin2hex, hex2bin, bin2dec, dec2bin, left_shift, xor, right_shift


class DES:
    # Метод для разделения блока и выполнения циклического сдвига влево
    def __init__(self, key: str):
        self.key = hex2bin(key)
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

    def encrypt(self):
        data = self.permute(self.key, self.PC_I, 64, 'after initial')
        # getting 56 bit key from 64 bit using the parity bits
        round_binary_keys, round_keys, cd_blocks = self.generate_rounds()
        # Splitting
        left = data[0:32]
        right = data[32:64]

        for i in range(16):
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = self.permute(right, self.P_EXPAND, 48)
            # XOR RoundKey[i] and right_expanded

            xor_x = xor(right_expanded, round_binary_keys[i])

            # S-boxes: substituting the value from s-box table by calculating row and column
            sbox = []
            sbox_table = self.SBOX_TABLES
            for j in range(8):
                row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
                col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
                val = sbox_table[j][row][col]
                sbox.append(dec2bin(val))

            # Straight D-box: After substituting, rearranging the bits
            sbox_new = []
            for box in sbox:
                for elem in box:
                    sbox_new.append(int(elem))

            sbox_arr = self.permute(sbox_new, self.STRAIGHT_ROUND, 32)
            # XOR left and sbox_str
            result = xor(left, sbox_arr)
            left = result

            # Swapper
            if i != 15:
                left, right = right, left

            print(f"Round={i+1}  C{i+1}D{i+1}={cd_blocks[i]}  Round key={round_keys[i]}")

        # Combination
        combine = left + right

        # Final permutation: final rearranging of bits to get cipher text
        cipher_text = self.permute(combine, self.PC_F, 64, 'finish')
        return cipher_text

    def generate_rounds(self, msg: str = 'right'):
        round_binary_keys, round_keys, cd_blocks = [], [], []
        self.key = self.permute(self.key, self.PC_1, 56, 'round keys')
        ci, di = self.key[0: 28], self.key[28: 56]

        for i in range(1, 17):
            if msg == 'left':
                shift = 1 if i in [1, 2, 9, 16] else 2
                ci, di = left_shift(ci, shift), left_shift(di, shift)
            if msg == 'right':
                if i == 1:
                    shift = 0
                elif i in [2, 9, 16]:
                    shift = 1
                else:
                    shift = 2
                ci, di = right_shift(ci, shift), right_shift(di, shift)

            cd_block = ci + di
            cd_blocks.append(bin2hex(cd_block))
            k = self.permute(cd_block, self.PC_2, 48)
            round_binary_keys.append(k)
            round_keys.append(bin2hex(k))

        return round_binary_keys, round_keys, cd_blocks


pt = 'AAbb09182736ccdd'

des = DES(pt)
des.encrypt()

# CoDo  = 2E8CCE30C815C5
# C1D1 = 5D199C61902B8A
# k1 = 4463EF0C7445
# C2D2 = BA3338C3205714
