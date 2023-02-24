import mysql.connector




class DAo:

 def __init__(self,database):
  self.x=2
  try:
    con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database=database
    )
    print('data connect good ...')
  except:
    print('problems in connect to data ...')


 def create_tables(self):
  con = mysql.connector.connect(
   host='localhost',
   user='root',
   password='',
   port='3306',
   database='rekrute_test3'
  )
  cursor =con.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXIST post (
    post_id int NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    secteur varchar(255),
    comp_jours varchar(255),
    region varchar(255),
    PRIMARY KEY (post_id)
   );
  
  """)
  con.commit()
  cursor.execute("""
    CREATE TABLE entreprise (
      ent_id int NOT NULL AUTO_INCREMENT,
      ent_secteur varchar(255),
      description varchar(255),
      PRIMARY KEY (ent_id)
     );

    """)
  con.commit()
  cursor.execute("""
      CREATE TABLE job (
        job_id int NOT NULL AUTO_INCREMENT,
        job_name varchar(255),
        experiance varchar(255),
        type_contra varchar(255),
        niveau_etude varchar(255),
        PRIMARY KEY (job_id)
       );

      """)

  con.commit()
  cursor.execute("""
      CREATE TABLE soft_skills (
        soft_id int NOT NULL AUTO_INCREMENT,
        soft_skill varchar(255)
        PRIMARY KEY (soft_id)
       );

      """)

  con.commit()
  cursor.execute("""
      CREATE TABLE job_skills (

        job varchar(255),
        skill varchar(255),
        FOREIGN KEY (job) REFERENCES job(job_id),
        FOREIGN KEY (skill) REFERENCES soft_skill(soft_id),
        PRIMARY KEY (job,skill)
       );

      """)


 def insert(self,values,table):

  mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="test-procedure"
  )
  from scrap_backup import no_accent_word
  i=0
  for i in range(0,len(values)):

    #print("with accent",values[i])
    if isinstance(values[i], str):
    # print("without accent",no_accent_word(values[i]))
     values[i]=no_accent_word(values[i])
  mycursor = mydb.cursor()
  print("from def insert : ",table)
  #print("from def insert : ",len(values),values)
  if table == 'davinci':
    print("in if davi")
    sql =" INSERT INTO davinci(response) VALUES(%s)"
  if table == 'file':
    print("in if tabel")
    sql =" INSERT INTO file(file) VALUES(%s)"
  if table == 'post':
    sql =" INSERT INTO post(secteur,comp_jours,ville,post_propose,date_du,date_au,lien,job_id,ent_id,pays) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  if table == 'entreprise':
   sql = "INSERT INTO {} (ent_title,ent_secteur,description ) VALUES (%s, %s , %s)".format(table)
  if table == 'job':
   sql = "INSERT INTO {} (job_name,experiance,type_contra,niveau_etude,exp_au_mois,exp_au_plus,bac_plus ) VALUES (%s,%s,%s, %s,%s,%s,%s)".format(table)
  mycursor.execute(sql,values)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")
  print('insert done ...')
 def insert_skill(self,values):
  mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="rekrute_test3"
  )

  print("im in function skill")
  query = 'select soft_skill from soft_skills'
  query2='select LAST_INSERT_ID() from job '
  mcursor=mydb.cursor()


  for skill in values :
   skill=skill.replace("'","")
   print('list of soft ',values)
   mcursor.execute(query)
   records = mcursor.fetchall()
   print("records of skills names : ", records)
   print("skill in for : ",skill)
   if (skill,) not in records:
    print("skill in if : ",skill)
    sql= f"INSERT INTO soft_skills (soft_skill) VALUES ('{skill}')"
    mcursor.execute(sql)
 def ff(self,values):
  print("im in ff")
  mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="rekrute_test3"
  )
  sql="select job_id from job "
  mcursor = mydb.cursor()
  mcursor.execute(sql)
  jid=mcursor.fetchall()
  for skill in values:
   skill = str(skill).rstrip(",)").lstrip("(")
   skill=skill.replace("'","")
   print("J_ID",jid[-1])
   print(skill)
   sql3 = f"INSERT INTO job_skillss (job_id, soft_id) "
   sql2 = f"select soft_id from soft_skills where soft_skill = '{skill}'"
   mcursor.execute(sql2)
   so_id=str(mcursor.fetchone())
   so_id=so_id.lstrip('(').rstrip(",)")
   jiid=jid[-1]
   print("job id",type(jiid[0]),":", jiid,"soft id",type(so_id),so_id)
   sql3 = f"INSERT INTO job_skillss (job_id, soft_id) values({jiid[0]},{int(so_id)})"
   mcursor.execute(sql3)
