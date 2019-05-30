import pandas as pd
import numpy as np
import json
import os,sys
import mysql.connector
from mysql.connector import Error
mango_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/common/')

sys.path.append(mango_dir)
import common


def connectMysql():
    try:
        mySQLconnection = mysql.connector.connect(host='13.251.123.143',port='3306',database='HotelGatewayNew',user='hotelgateway',password='SeechoitlOfwoRwObEaphOabdLVy')
        sql_select_Query = "SELECT room_name FROM HotelGatewayNew.room_type_mapping where master_room_type is not null "
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        cursor.close()
            
        return records
        
    except Error as e :
        print ("Error while connecting to MySQL", e)
    finally:
            #closing database connection.
        if(mySQLconnection .is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")  


def handle():
    script_dir = os.path.split(os.path.dirname(os.path.realpath('__file__')))[0]

    listarray = {"hotelTyleName":"hotelType.json","bedName":"bed.json","bedtypeName":"bedtype.json","roomTypeName":"roomType.json","viewName":"view.json"}
    rel_path = "share"
    
    listjson={}

    for key in listarray.items():
        bs_file_path = os.path.join(script_dir, (rel_path + "/"+ "{}").format(key[1]))
        getvalue = readjson(bs_file_path)
        
        listjson[key[0]] = getvalue
      
    
    return listjson

def saveCsv():
    pd =connectMysql()
    listjson = handle()
    handlText(pd[1][0],listjson)

    
def handlText(text,listjson):
    
    for item,value in listjson.items():
        print((item))
        
        
        
def readjson(file):
    with open(file,'r') as json_file:  
        data = json.load(json_file)
        return data
        
saveCsv()