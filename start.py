import sqlite3

conn = sqlite3.connect("login_details.db")
cur = conn.cursor()

#query = '''CREATE TABLE login 
#        ( username varchar(50),
#          password varchar(50) )
#         '''

def login(username,password):
    login = "SELECT username,password from LOGIN where username=? AND password=?"
    cur.execute(login,(username,password))
    data = cur.fetchone()
    if(data==None):
        return False
    else:
        return True

def register(username,password):
    query = "INSERT into LOGIN values (?,?)"
    try:
        cur.execute(query,(username,password))
        conn.commit()
        return True
    except:
        return "There was an error"

#query = "SELECT * from LOGIN"
#cur.execute(query)
#data = cur.fetchall()
#print(data)
