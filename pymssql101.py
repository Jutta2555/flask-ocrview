# import pymysql.cursors
# from pymysql import connections, connect

# mydb = connect(host='192.168.1.252',
#                user='flask',
#                password='F8HM4G6etPMjuYBa',
#                database='asteriskcdrdb'
#                )

# print(mydb)

import pymysql.cursors
# Connect to the database
print(dir(pymysql.cursors))
connection = pymysql.connect(host='192.168.1.252',
                             user='flask',
                             password='F8HM4G6etPMjuYBa',
                             charset='utf8',
                             database='asteriskcdrdb')
# ,cursorclass = pymysql.cursors.DictCursor
with connection:
    with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        sql = "SELECT VERSION() "
        cursor.execute(sql)
        print(cursor)
        result = cursor.fetchone()
        print(result)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
# AttributeError: module 'pymysql._auth' has no attribute 'scramble_old_password'

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='kanha@12345',
#                              database='mydb23',
#                              charset='utf8mb4')
# cur1 = connection.cursor()
# cur1.execute("select * from emp where city='hyd'")
# import mysql.connector

# mydb = mysql.connector.connect(host='192.168.1.252',
#                                user='flask',
#                                password='F8HM4G6etPMjuYBa',
#                                database='asteriskcdrdb'
#                                )

# print(mydb)
# # mysql.connector.errors.OperationalError: 1043 (08S01): Bad handshake
# Successfully uninstalled mysql-connector-python-8.0.29


# import mysql.connector
# import mysql
# # from _mysql_connector import Error
# # import Error
# try:
#     conn = mysql.connector.connect(host='192.168.1.252',
#                                    user='flask',
#                                    password='F8HM4G6etPMjuYBa',
#                                    database='asteriskcdrdb')
#     if conn.is_connected():
#         db_Info = conn.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = conn.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)
# # except Error as e:
# #     print("Error while connecting to MySQL", e)
# finally:
#     if conn.is_connected():
#         cursor.close()
#         conn.close()
#         print("MySQL connection is closed")
# mysql.connector.errors.OperationalError: 1043 (08S01): Bad handshake
# Successfully uninstalled mysql-connector-python-8.0.29


# Successfully installed mysql-connector-python-8.0.5
# import mysql.connector

# mydb = mysql.connector.connect(host='192.168.1.252',
#                                user='flask',
#                                password='F8HM4G6etPMjuYBa',
#                                database='asteriskcdrdb'
#                                )

# print(mydb)
