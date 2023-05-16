import mariadb
import sys
import datetime
import string

try:
    conn = mariadb.connect(
        user="gh",
        password="admin",
        host="127.0.0.1",
        port=3306,
        database="ghdb"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Paltform: {e}")
    sys.exit(1)

date = datetime.datetime.now().strftime("%Y_%m_%d")
timeStamp = datetime.datetime.now().strftime("%H_%M_%S")

cur = conn.cursor()
# comand = "CREATE TABLE" + " " + "dateset_" + str(ct) +" " + "(a int);" #"(Time CHAR(10)) (Output0 INT) (Output1 INT) (Input0 INT) (Input1 INT) (Input2 INT) (Input3 INT)" + ";"
table_name = f"data_set_{date}"
try:
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (time CHAR(10), Output_0 int, Output_1 int, Input_0 int, Input_1 int, Input_3 int);""")
except:
    sys.exit(1)

cur.close()
conn.close()