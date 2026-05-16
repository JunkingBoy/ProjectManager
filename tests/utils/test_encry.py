import base64
import importlib
import sys
import types

import pytest


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


class FakeAESInstance:
    def __init__(self, key, mode, iv):
        self.iv = iv

    def encrypt(self, data):
        return data[::-1]

    def decrypt(self, data):
        return data[::-1]


class FakeAESModule:
    MODE_CBC = "MODE_CBC"
    block_size = 16

    @staticmethod
    def new(key, mode, iv):
        return FakeAESInstance(key, mode, iv)


def load_encry_module():
    sys.modules.pop("utils.Encry", None)

    crypto_module = types.ModuleType("Crypto")
    cipher_module = types.ModuleType("Crypto.Cipher")
    util_module = types.ModuleType("Crypto.Util")
    padding_module = types.ModuleType("Crypto.Util.Padding")

    cipher_module.AES = FakeAESModule
    padding_module.pad = lambda data, block_size: data + b"|pad"
    padding_module.unpad = lambda data, block_size: data[:-4] if data.endswith(b"|pad") else data

    sys.modules["Crypto"] = crypto_module
    sys.modules["Crypto.Cipher"] = cipher_module
    sys.modules["Crypto.Util"] = util_module
    sys.modules["Crypto.Util.Padding"] = padding_module

    return importlib.import_module("utils.Encry")


encry_module = load_encry_module()


@pytest.mark.asyncio
async def test_encrypt_and_decrypt_round_trip_with_fixed_iv(monkeypatch):
    monkeypatch.setattr(encry_module, "get_env_val", lambda key, env=None: "00112233445566778899aabbccddeeff")

    encrypted = await encry_module.encrypt("hello-world", "0102030405060708090a0b0c0d0e0f10")
    decrypted = await encry_module.decrypt(encrypted)

    assert decrypted == "hello-world"


@pytest.mark.asyncio
async def test_encrypt_returns_empty_string_for_empty_data(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(encry_module.ExceptionLog, "get_instance", classmethod(lambda cls: logger))

    result = await encry_module.encrypt("")

    assert result == ""
    assert logger.messages == ["加密数据为空!"]


@pytest.mark.asyncio
async def test_decrypt_returns_empty_string_for_empty_data(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(encry_module.ExceptionLog, "get_instance", classmethod(lambda cls: logger))

    result = await encry_module.decrypt("")

    assert result == ""
    assert logger.messages == ["解密数据为空!"]


@pytest.mark.asyncio
async def test_encrypt_raises_value_error_when_aes_key_missing(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(encry_module.ExceptionLog, "get_instance", classmethod(lambda cls: logger))
    monkeypatch.setattr(encry_module, "get_env_val", lambda key, env=None: "")

    with pytest.raises(ValueError, match="获取密钥数据失败"):
        await encry_module.encrypt("hello")

    assert logger.messages == ["获取密钥数据失败,请检查密钥文件!"]


@pytest.mark.asyncio
async def test_decrypt_raises_value_error_for_invalid_ciphertext(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(encry_module.ExceptionLog, "get_instance", classmethod(lambda cls: logger))
    monkeypatch.setattr(encry_module, "get_env_val", lambda key, env=None: "00112233445566778899aabbccddeeff")
    monkeypatch.setattr(encry_module, "unpad", lambda data, block_size: (_ for _ in ()).throw(ValueError("bad padding")))

    with pytest.raises(ValueError, match="解密数据失败"):
        await encry_module.decrypt(base64.b64encode(b"short").decode("utf-8"))

    assert logger.messages == ["解密数据失败!"]
