import os
import json
import time

class Database:
    def __init__(self, path): # path = database.json 파일 경로
        self.path = path
        print("Database path: ", self.path)
        self.data = {}
        self.load()

    def load(self): # Database를 JSON으로부터 불러온다.
        if not os.path.exists(self.path):
            self.save()
        with open(self.path, 'r') as f:
            self.data = json.load(f)
            f.close()

    def save(self): # 현재 self.data를 path에 json형식으로 저장한다
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)
            f.close()
        
    def get(self, key): # key에 해당하는 value를 가져온다 -> self.data
        return self.data.get(key, None)

    def set(self, key, value): # key에 해당하는 value를 self.data에 저장한다.
        self.data[key] = value
        self.save()

    def delete(self, key): # key에 해당하는 value를 삭제한다
        if(key in self.data):
            del self.data[key]
            self.save()

    def exists(self, key): # key의 존재를 확인한다.
        return key in self.data

    def keys(self): # key의 목록을 불러온다
        return self.data.keys()

    def values(self): # 모든 value들을 가져온다
        return self.data.values()

    def items(self): # key, value 쌍을 반환한다.
        return self.data.items()
    
    def clear(self):
        self.data = {}
        self.save()

def main():
    db = Database("database.json")
    print(db.data)

    key = "name"
    value = "John"
    db.set(key, value)
    print("db.get(key!!!!) : ", db.get(key))
    is_exists = db.exists(key)
    print("db.exists(key!!!!!!!) : ", is_exists)
    db.delete(key)
    print("db.get(key!!!!!!!!!!!!11!!) : ", db.get(key), "....deleted!")
    is_exists = db.exists(key)
    print("db.exists(key!!!!!!!) : ", is_exists)


if __name__=="__main__":
    main()