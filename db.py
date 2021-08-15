def signup(usr,psw,dbname): #Creating Database where usr= username and psw= password
    
    import mysql.connector as con
    try:
        mycon = con.connect(host="localhost",user=usr,passwd=psw)
    except con.errors.ProgrammingError:
        print('access denied!')
        quit()

    cur = mycon.cursor()
    cur.execute('show databases')
    if (dbname,) not in cur.fetchall():
        cur.execute("create database {}".format(dbname))
        mycon.commit()
        cur.close()
        mycon.close()
    
    mycon = con.connect(host="localhost",user=usr,passwd=psw,database=dbname)
    return mycon

def addscore(mycon,player,score): #add the score to mysql table

    cur = mycon.cursor()
    cur.execute('select count(*) from score')
    data = cur.fetchall()
    for i in data:
        for j in i:
            sno = j
    sno+=1
    cur.execute("Insert into score values({},'{}',{},now())".format(sno,player,score))
    mycon.commit()

def getHighScores(mycon): #gets the top 5 scores

    cur = mycon.cursor()
    cur.execute('select player, score from score order by score desc;')
    data = cur.fetchall()[:5]
    return data

def createtable(mycon): #creating the table

    cur = mycon.cursor()
    cur.execute("show tables")
    data = cur.fetchall()
    if ('score',) not in data:
        str1 = 'Create Table score(sno int primary key,player varchar(30),score int(30),time varchar(30))'
        cur.execute(str1)
        mycon.commit()
