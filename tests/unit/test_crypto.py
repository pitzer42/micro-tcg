import unittest
from micro_tcg.crypto import (
    encrypt,
    equals_to_encrypted
)

plain_text = 'plaintext'

plain_values = [
    'text',
    123,
    1.23,
    dict(),
    list(),
    object,
    b'bytes'
]


class TestEncrypt(unittest.TestCase):
    """ Unit tests for micro_tcg.models.encrypt """

    def test_hash_is_different_from_plain_text(self):
        hashed = encrypt(plain_text)
        self.assertNotEqual(plain_text, hashed)

    def test_hash_type_is_bytes(self):
        hashed = encrypt(plain_text)
        self.assertIsInstance(hashed, bytes)

    def test_hashes_any_type(self):
        try:
            map(encrypt, plain_values)
        except Exception as e:
            error_msg = str(e)
            self.fail(msg=error_msg)


class TestEqualsToEncrypted(unittest.TestCase):
    """ Unit tests for micro_tcg.models.equals_to_encrypted """

    def test_compares_original_plain_value_to_hashed_value(self):
        hashes = list(map(encrypt, plain_values))
        try:
            for i in range(len(hashes)):
                plain_value = plain_values[i]
                hash_value = hashes[i]
                are_equal = equals_to_encrypted(plain_value, hash_value)
                self.assertTrue(are_equal)
        except Exception as e:
            error_msg = str(e)
            self.fail(msg=error_msg)
