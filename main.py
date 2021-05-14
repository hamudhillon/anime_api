import requests
import json
BASE='http://127.0.0.1:5000/'

# data=[{'name':'Hamu','email':'hamu@gmail.com','password':'123'},
#       {'name':'vind','email':'vind@gmail.com','password':'998'},
#       {'name':'prab','email':'prab@gmail.com','password':'545'}]

# for i in range(len(data)):
#     response=requests.put(BASE+'user/'+str(i),data[i])
#     print(response.json())
    
res=requests.get('http://127.0.0.1:5000/anime/all')
data=res.json()

import pprint

pprint.pprint(data[0]['ani_episodes'])