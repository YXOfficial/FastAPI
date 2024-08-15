import mysql.connector
import datetime
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Khoa12345@",
  database='logininfo'
)

cursor = mydb.cursor(buffered=True)

def getuser(data):
  cursor.execute('USE logininfo;')
  cursor.execute('SELECT * FROM LoginInfo WHERE GMAIL = %s', (data,))
  account = cursor.fetchone()
  return {"account": account}

def checkUser(account):
  if account["account"] == None:
      return {}
  return account
def checkToken(AccessToken):
  mydb.commit()
  cursor.execute('USE logininfo;')
  cursor.execute('SELECT * FROM LoginInfo WHERE AccessToken = %s', (AccessToken,))
  account = cursor.fetchone()
  return account

def CreateUser(data):
  cursor.execute('INSERT INTO LoginInfo (USERNAME, PASSWORD, GMAIL) VALUES (%s, %s, %s)', (data["username"], data["password"], data["gmail"], ))
  mydb.commit()
  return True



def CreateToken(access_token, data):
  query = "UPDATE LoginInfo SET AccessToken=%s, EXPIRY_DATE=current_timestamp() + INTERVAL 30 SECOND WHERE GMAIL=%s"
  parameters = (access_token, data,)
  cursor.execute(query, parameters)
  mydb.commit()
  return True

# if __name__ == "__main__":
#   account = getuser({"gmail":"aaaaaaaaaa@gmail.com"})
#   checkUser(account)