import os
import sys
from DAO import DAo
d=DAo("test-procedure")
#synchronisation du l'id
id = os.environ.get("id")
if id is not None:
    print(id)
    os.environ["id"]=str(int(int(id)+1))
else:
    print(1)
    id=1
    os.environ["id"]="2"
#***************OPENAI PART *****************************
import openai
import sqlite3
import mysql.connector

openai.api_key = "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"
# database con
try:
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        port='3306',
        database='test-procedure'
    )
    print('data connect good ...')
except:
    print('problems in connect to data ...')
# get files from database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test-procedure"
)

sql = "SELECT file FROM file WHERE id="+str(id)+" ;"
mcursor = mydb.cursor()
mcursor.execute(sql)
jid = mcursor.fetchall()
i = 1
string = ""
for tup in jid:
    string += tup[0] + " "
string = string.strip()
#print(string)
# code="this file code".join(jid)
#***************BASE ON THE LAST RESPONCE *******************
# if id==1 :
#  prompt = "What this code do :" + string
# else:
#     try:
#         print("im in else of prompt and that the id ",id)
#         sql = "SELECT response FROM davinci WHERE Id=(SELECT LAST_INSERT_ID());"
#         mcursor = mydb.cursor()
#         mcursor.execute(sql)
#         jid = mcursor.fetchall()
#         string2=""
#         for tup in jid:
#             string2 += tup[0] + " "
#
#         string2 = string.strip()
#   #      print("******PROMPT*******")
#         prompt = "based on your last reponse "+string2+"What this code do :" + string
#     except:
#          prompt = "What this code do :" + string
# # Generate a response
# if prompt.startswith("based on your last reponse "):
#     print("******PROMPT*******")
#***************BASE ON THE LAST RESPONCE *******************
#davinci analyse the code
prompt = "What this code do :" + string
try:
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0
    )

    response = completion.choices[0].text
    response = [response]
    d.insert(response,"davinci")
except:
    print("too long file")
    fail = os.environ.get("fail")
    # print("id",id)
    if fail is not None:
        os.environ["fail"] = str(int(int(fail) + 1))
    else:
        # print("id environment variable is not set")
        print(1)
        os.environ["fail"] = "1"
#***************END OPENAI PART *****************************
#The Last step
os.system("python script2-test.py")
sys.exit()