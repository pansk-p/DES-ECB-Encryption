# DES Encryption Algorithm in Python

This Python program implements the Data Encryption Standard (DES) algorithm, a symmetric key block cipher. DES operates on 64-bit blocks of data and involves various permutation and substitution operations.
Here's an overview of the main components and functionalities of the program:

 1. **Permutation Tables**: The program defines several permutation tables (e.g., initial permutation ip, key permutation pc1, pc2, expansion expansion_table, final permutation finalp, etc.) used in the DES algorithm.

 2. **S-boxes**: The S-boxes (substitution boxes) are defined using a 2D list (sbox). These S-boxes are used for the substitution operation during the DES encryption process.

 3. **Key Generation**: The subKeyGenerator function generates 16 subkeys for each round of DES encryption based on the initial key and the left rotation values specified by the left_rotations table.

 4. **DES Encryption**: The desCrypt function performs the core DES encryption. It includes the initial permutation, key generation, 16 rounds of substitution and permutation operations, and the final permutation.

 5. **String and Hexadecimal Input Handling**: The program allows the user to input the plaintext either as a binary string or a hexadecimal string. It includes functions (stringToBinary, hexToList, bitsToString) for converting between these formats.

 6. **Padding**: The pad function is used to pad the input data with '0's to create 64-bit blocks if needed.

 7. **Output and Logging**: The program outputs the encryption results to the console and also writes the results to a text file (EncryptionResult.txt). The output includes details of each encryption round, such as the input block, subkeys, and the final output.


The program performs DES encryption on the input data, and the final encrypted output is printed to the console and saved in the EncryptionResult.txt file. 

## Features
- Key generation with subkeys for each round.
- Initial and final permutations.
- Expansion, substitution, and permutation operations.
- S-boxes for substitution.
- Support for binary string and hexadecimal input formats.
- Padding to create 64-bit blocks if necessary.
- Output details of each encryption round.
- Results printed to the console and saved in `EncryptionResult.txt` file.

## How to Use

1. Run the program and input the plaintext.
2. Choose the input format (binary or hexadecimal).
3. Enter the 64-bit key.
4. View the console output and find the final encrypted result in `EncryptionResult.txt`.

## Example

```bash
python des_encryption.py
