from PBox import PBox
from SBox import SBox

from utils import bin2hex, hex2bin, bin2dec, dec2bin, shift_func, xor


class DES:
    def __init__(self, main_key: str):
        self.main_key = hex2bin(main_key)
        self.PC_1 = PBox.get_key_initial_permutation()
        self.PC_2 = PBox.get_key_finish_permutation()
        self.PC_I = PBox.get_initial_permutation()
        self.PC_F = PBox.get_finish_permutation()
        self.P_EXPAND = PBox.get_single_expand_permutation()
        self.STRAIGHT_ROUND = PBox.get_straight_round_permutation()
        self.round_binary_keys, self.cd_blocks = self.generate_rounds()  # getting 56 bit key from 64 bit using the parity bits
        self.output_sbox = SBox().get_sbox_substitution
        self.left, self.right = None, None

    @staticmethod
    def get_matrix(data: list):
        for ind, el in enumerate(data, start=1):
            print(f'{ind}={el} ', end='')
            if ind % 8 == 0 and ind != len(data):
                print()
        print()

    def generate_rounds(self) -> tuple[list, list]:
        round_binary_keys, cd_blocks = [], []
        self.main_key = self.permute(self.main_key, self.PC_1, 56, 'round keys')
        ci, di = self.main_key[0: 28], self.main_key[28: 56]

        for i in range(1, 17):
            shift = 1 if i in [1, 2, 9, 16] else 2
            ci, di = shift_func(ci, shift), shift_func(di, shift)
            cd_block = ci + di

            cd_blocks.append(bin2hex(cd_block, is_needed=True))
            k = self.permute(cd_block, self.PC_2, 48)
            round_binary_keys.append(k)

        return round_binary_keys, cd_blocks

    def permute(self, data: list, arr: list, n: int, permute_text: str = '') -> list:
        permutation = []
        for i in range(0, n):
            permutation.append(data[arr[i] - 1])
        # print(f'{permute_text} permutation = {"".join(map(str, permutation))}'.strip().capitalize())
        return permutation

    def encrypt(self, pt: str):
        text = self.main_key if not len(pt) else hex2bin(pt)
        data = self.permute(text, self.PC_I, 64, 'after initial')
        print(f'L0R0={bin2hex(data, is_needed=True, n=16)}')

        # Splitting
        self.left, self.right = data[0:32], data[32:64]

        for i in range(1, 17):
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = self.permute(self.right, self.P_EXPAND, 48)
            # XOR RoundKey[i] and right_expanded
            print(f"Round={i}  C{i}D{i}={self.cd_blocks[i-1]}  Round key={bin2hex(self.round_binary_keys[i-1], is_needed=True, n=12)}")
            print(f'CP1={bin2hex(right_expanded, is_needed=True, n=12)}')
            xor_x = xor(right_expanded, self.round_binary_keys[i-1])
            print(f'CP2(xor_x)={bin2hex(xor_x, is_needed=True, n=12)}')
            print(f'CP3={self.output_sbox(xor_x=xor_x)}={bin2hex(list(map(int, self.output_sbox(xor_x=xor_x))), is_needed=True, n=8)}')
            # Straight D-box: After substituting rearranging the bits
            output_pbox = self.permute(list(map(int, self.output_sbox(xor_x=xor_x))), self.STRAIGHT_ROUND, 32)
            print(f'CP4={"".join(map(str, output_pbox))}={bin2hex(output_pbox, is_needed=True, n=8)}')

            # XOR left and SBox
            result = xor(output_pbox, self.left)
            self.left = result
            print(f'L{i}R{i}={bin2hex(self.right, is_needed=True, n=8)}{bin2hex(self.left, is_needed=True, n=9)}')
            print()
            # Swapper
            if i < 16:
                self.left, self.right = self.right, self.left

        # Combination
        output = self.left + self.right
        # Final permutation: final rearranging of bits to get cipher text
        cipher_text = self.permute(output, self.PC_F, 64, 'finish')
        print(f'Cipher text={bin2hex(cipher_text)}')

    def decrypt(self, ct: str):
        print("Decryption")
        text = self.main_key if not len(ct) else hex2bin(ct)
        data = self.permute(text, self.PC_I, 64, 'after initial')
        print(f'L16R16={bin2hex(data, is_needed=True, n=16)}')
        # getting 56 bit key from 64 bit using the parity bits

        # Splitting
        self.left, self.right = data[0:32], data[32:64]

        for i in range(17, 1, -1):
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = self.permute(self.right, self.P_EXPAND, 48)
            # XOR RoundKey[i] and right_expanded
            print(f"Round={i-1}  C{i-1}D{i-1}={self.cd_blocks[i-2]}  Round key={bin2hex(self.round_binary_keys[i-2], is_needed=True, n=12)}")
            print(f'CP1={bin2hex(right_expanded, is_needed=True, n=12)}')
            xor_x = xor(right_expanded, self.round_binary_keys[i-2])
            print(f'CP2(xor_x)={bin2hex(xor_x, is_needed=True, n=12)}')
            # S-boxes: substituting the value from s-box table by calculating row and column
            print(f'CP3={self.output_sbox(xor_x=xor_x)}={bin2hex(list(map(int, self.output_sbox(xor_x=xor_x))), is_needed=True, n=8)}')
            # Straight D-box: After substituting rearranging the bits
            output_pbox = self.permute(list(map(int, self.output_sbox(xor_x=xor_x))), self.STRAIGHT_ROUND, 32)
            print(f'CP4={"".join(map(str, output_pbox))}={bin2hex(output_pbox, is_needed=True, n=8)}')

            # XOR left and SBox
            result = xor(output_pbox, self.left)
            self.left = self.right
            self.right = result

            print(f'L{i-2}R{i-2}={bin2hex(self.left, is_needed=True, n=8)}{bin2hex(self.right, is_needed=True, n=8)}')
            print()

        # Combination
        output = self.left + self.right
        # Final permutation: final rearranging of bits to get cipher text
        plain_text = self.permute(output, self.PC_F, 64, 'finish')

        print(f"Plain Text : {bin2hex(plain_text)}")


PT = "18C7B8E55EF4317C"
KEY = "3900A6B48811783C"
CT = '18C7B8E55EF4317C'


des = DES(KEY)
des.encrypt(PT)
# des.decrypt(CT)


input_text = '80EE7EE0474A74BF987C314AB0BB86B'
open_text = 'D2F8F63A57F54020'

