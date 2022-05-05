import json

with open("login.json",'w') as f:
    personal_info = {
        'email' : 'deamerrong123@gmail.com',
        'passward' : '1520QZrong'
        }

    json.dump(personal_info,f)

##f = open("login.json",'r')
##data = json.load(f)
##f.close()
##
##print(data)
