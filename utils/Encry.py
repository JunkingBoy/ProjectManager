import base64

from typing import Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from utils.Logs import ExceptionLog
from tools.Files import get_env_val
from tools.Re import generate_aes_params

'''
AES-128加密算法
'''
async def encrypt(
    data: Any,
    iv: str = ""
) -> str:
    e: ExceptionLog = ExceptionLog.get_instance()
    if not data:
        e.info("加密数据为空!")
        return ""
    tmp_key: str = get_env_val("aes", "dev")
    if not tmp_key:
        e.info("获取密钥数据失败,请检查密钥文件!")
        raise ValueError("获取密钥数据失败,请检查密钥文件!")
    if not iv: tmp_vector: bytes = generate_aes_params()
    else: tmp_vector: bytes = bytes.fromhex(iv)
    tmp_cipher = AES.new(bytes.fromhex(tmp_key), AES.MODE_CBC, tmp_vector)
    # 使用PKCS7填充数据使其成为16字节倍数
    paded_data: bytes = pad(
        str(data).encode("utf-8"),
        AES.block_size
    )
    encryed_data: bytes = tmp_cipher.encrypt(paded_data)
    # iv+密文拼接
    return base64.b64encode(tmp_vector + encryed_data).decode("utf-8")

'''
AES-128解密算法
'''
async def decrypt(data: str) -> str:
    e: ExceptionLog = ExceptionLog.get_instance()
    if not data:
        e.info("解密数据为空!")
        return ""
    try:
        encryed_data: bytes = base64.b64decode(data)
        # 提取前16字节iv - 字符数组处理方式
        tmp_vector: bytes = encryed_data[:AES.block_size]
        tmp_cipher = AES.new(bytes.fromhex(get_env_val("aes", "dev")), AES.MODE_CBC, tmp_vector)
        # 解密、去填充
        padded_data: bytes = tmp_cipher.decrypt(encryed_data[AES.block_size:])
        return unpad(padded_data, AES.block_size).decode("utf-8")
    except Exception as err:
        e.info(f"解密数据失败!{err}")
        raise ValueError(f"解密数据失败,解密数据为{data}")
