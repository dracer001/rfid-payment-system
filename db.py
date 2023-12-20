import json
from datetime import datetime as d
class DB():
    def __init__(self, path):
        self.path = path

    def read(self):
        f = open(self.path, "r")
        json_obj = f.read()
        f.close()
        return json.loads(json_obj)

    def write(self, json_obj):
        f = open(self.path, "w")
        json.dump(json_obj, f, indent=4)
        f.close()

    def search_by_id(self, id):
        json_obj = self.read()
        return json_obj[id]

    def search_by_name(self, name):
        res = dict()
        json_obj = self.read()
        for x in json_obj:
            if name.lower() in json_obj[x]["name"].lower():
                res[x] = json_obj[x]
        return res

    def get_last_index(self):
        json_obj = self.read()
        obj = json_obj.popitem()
        return int(obj[0])

    def insert(self, json_data):
        last_id = self.get_last_index()
        id = last_id+1
        json_obj = self.read()
        json_obj[id] = json_data
        try:
            self.write(json_obj)
        except:
            return False
        # json_data["date"] = str(d.today())
        # self.update(id, json_data)
        return id

    def update(self, id, new_data):
        id = str(id)
        json_obj = self.read()
        json_obj[id].update(new_data)
        try:
            self.write(json_obj)
        except:
            return False
        return True

    def get_user(self, id):
        json_obj = self.read()
        id = str(id)
        user_info = json_obj[id]
        user_info['id'] = id
        return user_info

    def delete(self, id):
        json_obj = self.read()
        # print(json_obj)
        try:
            del json_obj[id]
            self.write(json_obj)
        except KeyError:
            return "file cannot be found"
        return "File Deleted"




