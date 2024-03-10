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
pt = 'AABB11223344CCDD'

des = DES(pt)
des.encrypt()
```

Output:
```powershell
Round=1  C1D1=87C037337C186C  Round key=00195C5C30C8CD
Round=2  C2D2=0F806E76F830D8  Round key=00056CD8722CCC
Round=3  C3D3=3E01B9CBE0C361  Round key=005665B4A8B19B
Round=4  C4D4=F806E70F830D86  Round key=00DE8D01277623
Round=5  C5D5=E01B9C3E0C361B  Round key=004BA22F7E0962
Round=6  C6D6=806E70F830D86F  Round key=00A9948E84C95E
Round=7  C7D7=01B9C3E0C361BE  Round key=00700AEA45B6D0
Round=8  C8D8=06E70F830D86F8  Round key=00B0F830F98469
Round=9  C9D9=0DCE1F061B0DF0  Round key=0094F84673D62C
Round=10  C10D10=37387C086C37C1  Round key=00226756181DAA
Round=11  C11D11=DCE1F001B0DF06  Round key=006C55258C7835
Round=12  C12D12=7387C036C37C18  Round key=00C38179636AF0
Round=13  C13D13=CE1F00DB0DF061  Round key=008DC2B3B1891B
Round=14  C14D14=387C037C37C186  Round key=00B71B8A871616
Round=15  C15D15=E1F00DC0DF061B  Round key=003A32C15D23E4
Round=16  C16D16=C3E01B91BE0C36  Round key=0039385554E225
```

## Sources
[1] https://bit.nmu.org.ua/ua/student/metod/cryptology/%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%206.pdf



