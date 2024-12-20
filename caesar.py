def alpcezar(text, shift):
    result = []

    for bukva in text:
        if 'А' <= bukva <= 'Я':  # Обрабатываем заглавные буквы русского алфавита
            result.append(chr((ord(bukva) - ord('А') + shift) % 32 + ord('А')))
        elif 'а' <= bukva <= 'я':  # Обрабатываем строчные буквы русского алфавита
            result.append(chr((ord(bukva) - ord('а') + shift) % 32 + ord('а')))
        elif 'A' <= bukva <= 'Z':  # Обрабатываем заглавные буквы латинского алфавита
            result.append(chr((ord(bukva) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= bukva <= 'z':  # Обрабатываем строчные буквы латинского алфавита
            result.append(chr((ord(bukva) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(bukva)  # Не меняем пробелы, знаки препинания и другие символы

    return ''.join(result)  # Возвращаем строку, собрав её из списка

if __name__ == "__main__":
    text = input("Введите текст для шифрования: ")
    shift = int(input("Введите сдвиг (можно использовать отрицательные значения): "))
    encrypted_text = alpcezar(text, shift)
    print(f"Результат шифрования: {encrypted_text}")
