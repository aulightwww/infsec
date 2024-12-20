import struct

class RC5:
    def __init__(self, key, rounds=12, word_size=32):
        self.rounds = rounds
        self.word_size = word_size
        self.block_size = 2 * (word_size // 8)  # Размер блока = 2 слова
        self.key = key
        self.mod = 2 ** word_size
        self.S = self.key_schedule()

    def key_schedule(self):
        """
        Генерация ключей для каждого раунда.
        """
        P = 0xB7E15163
        Q = 0x9E3779B9
        u = self.word_size // 8  # Размер слова в байтах
        c = max(1, (len(self.key) + u - 1) // u)  # Количество слов в ключе (округляем вверх)
        padded_key = self.key.ljust(c * u, b'\x00')  # Дополнение ключа до длины, кратной размеру слова
        L = list(struct.unpack(f"{c}I", padded_key))  # Распаковываем дополненный ключ
        S = [(P + i * Q) % self.mod for i in range(2 * (self.rounds + 1))]

        A = B = i = j = 0
        for _ in range(3 * max(c, len(S))):
            A = S[i] = self._rotl((S[i] + A + B) % self.mod, 3)
            B = L[j] = self._rotl((L[j] + A + B) % self.mod, (A + B) % self.word_size)
            i = (i + 1) % len(S)
            j = (j + 1) % len(L)

        return S

    def encrypt_block(self, block):
        """
        Шифрование блока данных.
        """
        if len(block) != self.block_size:
            raise ValueError(f"Блок должен быть ровно {self.block_size} байт")

        A, B = struct.unpack("2I", block)
        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod

        for i in range(1, self.rounds + 1):
            A = (self._rotl(A ^ B, B % self.word_size) + self.S[2 * i]) % self.mod
            B = (self._rotl(B ^ A, A % self.word_size) + self.S[2 * i + 1]) % self.mod

        return struct.pack("2I", A, B)

    def decrypt_block(self, block):
        """
        Расшифрование блока данных.
        """
        if len(block) != self.block_size:
            raise ValueError(f"Блок должен быть ровно {self.block_size} байт")

        A, B = struct.unpack("2I", block)

        for i in range(self.rounds, 0, -1):
            B = self._rotr((B - self.S[2 * i + 1]) % self.mod, A % self.word_size) ^ A
            A = self._rotr((A - self.S[2 * i]) % self.mod, B % self.word_size) ^ B

        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod

        return struct.pack("2I", A, B)

    def _rotl(self, x, y):
        """
        Циклический сдвиг влево.
        """
        return ((x << y) & (self.mod - 1)) | (x >> (self.word_size - y))

    def _rotr(self, x, y):
        """
        Циклический сдвиг вправо.
        """
        return (x >> y) | ((x << (self.word_size - y)) & (self.mod - 1))


# Пример использования
if __name__ == "__main__":
    key = b"mysecretkey1234"  # Ключ произвольной длины
    rc5 = RC5(key)

    plaintext = b"meow"  # Сообщение (8 байт)
    plaintext = plaintext.ljust(8, b'\x00')  # Дополняем до размера блока (8 байт)

    # Шифрование
    encrypted = rc5.encrypt_block(plaintext)
    print("Зашифрованный текст:", encrypted)

    # Расшифрование
    decrypted = rc5.decrypt_block(encrypted)
    print("Расшифрованный текст:", decrypted.rstrip(b'\x00'))
