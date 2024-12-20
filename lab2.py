def generate_vigenere_square(alphabet):
    length = len(alphabet)
    return [alphabet[i:] + alphabet[:i] for i in range(length)]

def vigenere_cipher_encrypt(text, key, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    text = text.upper()
    key = key.upper()
    vigenere_square = generate_vigenere_square(alphabet)
    encrypted_text = []
    key_index = 0
    
    for char in text:
        if char in alphabet:
            row = alphabet.index(key[key_index % len(key)])
            col = alphabet.index(char)
            encrypted_text.append(vigenere_square[row][col])
            key_index += 1
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)

def vigenere_cipher_decrypt(text, key, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    text = text.upper()
    key = key.upper()
    vigenere_square = generate_vigenere_square(alphabet)
    decrypted_text = []
    key_index = 0
    
    for char in text:
        if char in alphabet:
            row = alphabet.index(key[key_index % len(key)])
            col = vigenere_square[row].index(char)
            decrypted_text.append(alphabet[col])
            key_index += 1
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

# Определение алфавита по входному тексту
def detect_alphabet(text):
    if any('А' <= char <= 'Я' or 'а' <= char <= 'я' for char in text):
        return "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Пример использования
plain_text = "СОБАКА"
key = "КЛЮЧ"

alphabet = detect_alphabet(plain_text)
encrypted_text = vigenere_cipher_encrypt(plain_text, key, alphabet)
print("Зашифрованный текст:", encrypted_text)

decrypted_text = vigenere_cipher_decrypt(encrypted_text, key, alphabet)
print("Расшифрованный текст:", decrypted_text)
