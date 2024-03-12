# DES (Data Encryption Standard)
![made-with-python](https://img.shields.io/badge/Made%20with-Python%203-1f425f.svg)
## What DES is it?
DES - Data Encryption Standard (DES) is a block cipher algorithm that takes plaintext in blocks of 64 bits and converts them into ciphertext using keys of 48 bits.
It is a symmetric key algorithm, which means that the same key is used to encrypt and decrypt the data.
The DES algorithm (Data Encryption Standard) is the most widely used encryption algorithm in the world.
For many years and among many people, "creating a secret code" and DES were synonymous.
And despite the recent coup by the Electronic Frontier Foundation to create a $220,000 machine to crack messages encrypted with DES, DES will live on in government and banking for years to come with a life-extending version called "triple-DES."

## How you can use this one?

Step 1: How to install and run your code.
Clone this repository on your machine and enter directory. 
```powershell
git clone https://github.com/gilspi/DES-algorithm.git
cd DES-algorithm
```

Step 2: Example of code usage.
The use of my code is very simple. Look:

```python
pt = "123456ABCD132536"
key = "AABB09182736CCDD"

des = DES(key)
des.encrypt(pt)
```

Output:
```powershell
L0R0=14A7D67818CA18AD
Round=1  C1D1=878067567E19F4  Round key=194CD072DE8C
CP1=8F16540F155A
right expanded=[1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
round_binary_keys[0]=[0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0]
CP2(xor_x)=965A847DCBD6
S1   row=3   col=2   val=8   output=1000
S1   row=3   col=2   val=10   output=1010
S1   row=2   col=5   val=15   output=1111
S1   row=0   col=2   val=14   output=1110
S1   row=1   col=15   val=6   output=0110
S1   row=0   col=14   val=5   output=0101
S1   row=3   col=7   val=7   output=0111
S1   row=0   col=11   val=14   output=1110
CP3=S1S2S3S4S5S6S7S8=10001010111111100110010101111110=8AFE657E
CP4=01001110110111110011010111101100=4EDF35EC
L0=00010100101001111101011001111000   CP4=01001110110111110011010111101100   result=00011000110010100001100010101101=18CA18AD
L1=01011010011110001110001110010100=5A78E394
...
L16R16=19BA9212CF26B472
Cipher text=C0B7A8D05F3A829C
```

## Sources
[1] https://bit.nmu.org.ua/ua/student/metod/cryptology/%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%206.pdf



