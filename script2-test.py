import os
import sys
from DAO import DAo
import mysql.connector
import openai
d=DAo("test-procedure")
#synchronisation d'id
id=os.environ.get("id")
id=int(id)
print(id)
oss=id+1
os.environ["id"]=str(oss)

stop=""
if id>30:
    stop="stop"
    openai.api_key = "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"
    print("Im in the last if ")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test-procedure"
    )
    sql = "SELECT response FROM davinci ;"
    mcursor = mydb.cursor()
    mcursor.execute(sql)
    responses = mcursor.fetchall()
    print("responses ",responses)
    les_reponces =""
    les_reponces = [t[0] for t in responses]
    les_reponces=" ".join(les_reponces)
    print("les responces ",les_reponces)
   #Analyse des reponses
    prompt="what these codes do "+les_reponces+"""give me a test procedure for using this web of states not the code ,
    first put list of steps one after one and than put list of the expected result from doing or following the steps one after one"""
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0
    )
    response = completion.choices[0].text
    print("response for the test procedure", response)

    print("failed in", os.environ.get("fail"))

if stop == "stop":
    sys.exit()

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
#print("jid", jid)
#print(len(jid))
string = ""

for tup in jid:
    string += tup[0] + " "


string = string.strip()
#print(string)
# code="this file code".join(jid)
#***************BASE ON THE LAST RESPONCE *******************
# try:
#     sql = "SELECT response FROM davinci where Id=(SELECT LAST_INSERT_ID());"
#     mcursor = mydb.cursor()
#     mcursor.execute(sql)
#     jid = mcursor.fetchall()
#     string2=""
#     for tup in jid:
#         string2 += tup[0] + " "
#
#     string2 = string.strip()
#    # print("******PROMPT*******")
#     prompt = "based on your last reponse "+string2+"What this code do :" + string
# except:
#***************BASE ON THE LAST RESPONCE *******************
prompt="What this code do :" + string
if prompt.startswith("based on your last reponse "):
    print("******PROMPT*******")
#prompt = "What this code do :" + string
# Generate a response
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
    print("response", response)
    response = [response]
    d.insert(response, "davinci")
except:
    print("too long file")
    os.environ["fail"] = str(int(int(os.environ["fail"]) + 1))
#***************END OPENAI PART *****************************

os.system("python script1-test.py")
sys.exit()