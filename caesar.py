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

def break_cezar(text):
    print("\nПопытки взлома:")
    
    # Определяем, какой алфавит используется (русский или английский)
    is_russian = any('А' <= bukva <= 'я' for bukva in text)
    alphabet_size = 32 if is_russian else 26  # Русский алфавит — 32 буквы, английский — 26

    # Проверяем все сдвиги от -alphabet_size до +alphabet_size
    for possible_shift in range(-alphabet_size, alphabet_size + 1):
        decrypted_text = alpcezar(text, possible_shift)
        print(f"Сдвиг {possible_shift}: {decrypted_text}")

if __name__ == "__main__":
    print("Добро пожаловать в программу шифрования и расшифровки Цезаря!")
    action = input("Выберите действие (зашифровать, расшифровать, взломать): ").strip().lower()

    if action in {"зашифровать", "расшифровать"}:
        text = input("Введите текст: ").strip()
        shift = int(input("Введите сдвиг (положительное число для шифрования, отрицательное для расшифровки): "))
        result = alpcezar(text, shift)
        print(f"Результат: {result}")
    
    elif action == "взломать":
        text = input("Введите зашифрованный текст: ").strip()
        break_cezar(text)
    
    else:
        print("Неизвестная команда. Попробуйте снова.")
