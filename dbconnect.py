import mysql.connector
def connection(): #here 'connection' is the name of the connection function
    cn=mysql.connector.Connect(host='localhost',user='root',passwd='',db='dedup',port=3306)
    cu=cn.cursor(buffered=True) #cursor is an inbuild class in mysql cu is the object
    return cu,cn