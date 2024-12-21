from collections import Counter

# Генерация квадрата Виженера
def generate_vigenere_square(alphabet):
    length = len(alphabet)
    return [alphabet[i:] + alphabet[:i] for i in range(length)]

# Шифрование текста
def vigenere_cipher_encrypt(text, key, alphabet):
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

# Расшифровка текста
def vigenere_cipher_decrypt(text, key, alphabet):
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

# Определение алфавита
def detect_alphabet(text):
    if any('А' <= char <= 'Я' or 'а' <= char <= 'я' for char in text):
        return "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Вычисление индекса совпадений
def calculate_index_of_coincidence(text, alphabet):
    frequencies = Counter([char for char in text if char in alphabet])
    text_length = sum(frequencies.values())
    index = sum(f * (f - 1) for f in frequencies.values()) / (text_length * (text_length - 1)) if text_length > 1 else 0
    return index

# Предсказание длины ключа
def guess_key_length(text, max_key_length, alphabet):
    likely_lengths = []
    for key_length in range(1, max_key_length + 1):
        segments = [''.join(text[i::key_length]) for i in range(key_length)]
        average_ic = sum(calculate_index_of_coincidence(segment, alphabet) for segment in segments) / key_length
        likely_lengths.append((key_length, average_ic))
    likely_lengths.sort(key=lambda x: x[1], reverse=True)
    return likely_lengths[0][0]

# Функция взлома
def break_vigenere_cipher(text, max_key_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    text = ''.join([char for char in text.upper() if char in alphabet])
    key_length = guess_key_length(text, max_key_length, alphabet)
    print(f"Предполагаемая длина ключа: {key_length}")

    key = []
    for i in range(key_length):
        segment = ''.join(text[j] for j in range(i, len(text), key_length))
        frequencies = Counter(segment)
        most_common_char = frequencies.most_common(1)[0][0]
        common_letter = 'E' if alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ" else 'О'
        shift = (alphabet.index(most_common_char) - alphabet.index(common_letter)) % len(alphabet)
        key.append(alphabet[shift])

    key = ''.join(key)
    print(f"Предполагаемый ключ: {key}")
    decrypted_text = vigenere_cipher_decrypt(text, key, alphabet)
    return decrypted_text, key

# Основное меню программы
if __name__ == "__main__":
    print("Добро пожаловать в шифратор Виженера!")
    action = input("Выберите действие (зашифровать, расшифровать, взломать): ").strip().lower()

    if action in {"зашифровать", "расшифровать", "взломать"}:
        text = input("Введите текст: ").strip()
        alphabet = detect_alphabet(text)

        if action == "зашифровать":
            key = input("Введите ключ для шифрования: ").strip()
            encrypted_text = vigenere_cipher_encrypt(text, key, alphabet)
            print("Зашифрованный текст:", encrypted_text)

        elif action == "расшифровать":
            key = input("Введите ключ для расшифровки: ").strip()
            decrypted_text = vigenere_cipher_decrypt(text, key, alphabet)
            print("Расшифрованный текст:", decrypted_text)

        elif action == "взломать":
            print("Попытка взлома текста...")
            decrypted_text, guessed_key = break_vigenere_cipher(text, max_key_length=10, alphabet=alphabet)
            print("Предполагаемый ключ:", guessed_key)
            print("Расшифрованный текст:", decrypted_text)

    else:
        print("Неизвестная команда. Попробуйте снова.")
