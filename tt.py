import json

with open('LOGIN.json','w') as f:
	info = {
	'email' : 'deamerrong123@gmail.com',
	'password':'1520QZrong'
	}
	json.dump(info,f)