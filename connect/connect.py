import mysql.connector
from mysql.connector import Error
try:
   mySQLconnection = mysql.connector.connect(host='13.251.123.143',
                             post='3306',
                             database='HotelGatewayNew',
                             user='hotelgateway',
                             password='SeechoitlOfwoRwObEaphOabdLVy')
   sql_select_Query = "SELECT room_name,master_room_type FROM HotelGatewayNew.room_type_mapping where master_room_type is not null group by room_name,master_room_type order by room_name desc "
   cursor = mySQLconnection .cursor()
   cursor.execute(sql_select_Query)
   records = cursor.fetchall()
   cursor.close()
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(mySQLconnection .is_connected()):
        connection.close()
        print("MySQL connection is closed")