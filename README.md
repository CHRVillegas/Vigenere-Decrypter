# Vigenere Decryption Program
Program that takes a ciphertext encrypted using a Vigenere Cipher in hex and returns the key in hex as well as the decrypted message. Uses english letter frequencies to accurately identify the key length used to encrypt the message and discover the key itself.

## Usage
Run the program with  
__python3 VigenereDecryption.py__  
and it will decrypt the ciphertext stored in __cipher.txt__
### Notes
Will not work with a key length equal to the message length (One-Time Pad) <br />
The longer the length of the message the more accurate the decryption will be.
