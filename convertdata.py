import pandas as pd
import numpy as np
import json
import os,sys
import mysql.connector
from mysql.connector import Error
import csv
import common.common as cm
from datetime import datetime as dt



def connectMysql():
    try:
        mySQLconnection = mysql.connector.connect(host='13.251.123.143',port='3306',database='HotelGatewayNew',user='hotelgateway',password='SeechoitlOfwoRwObEaphOabdLVy')
        sql_select_Query = "SELECT master_room_type,room_name FROM HotelGatewayNew.room_type_mapping where master_room_type  is  null and room_name <> '' group by room_name"
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
    rel_path = "Classification/share"
    
    listjson={}

    for key in listarray.items():
        bs_file_path = os.path.join(script_dir, (rel_path + "/"+ "{}").format(key[1]))
        
        getvalue = readjson(bs_file_path)
        
        listjson[key[0]] = getvalue
      
    
    return listjson

def saveCsv():
    pd =connectMysql()
    listjson = handle()
    
    
    df=[]
    
    for item in pd:
        
        savetext =handlText(item[1],listjson,item[0]) 
        df.append(savetext)
        

    keys = df[0].keys()
    
    filename = str(dt.now().year)+ "-"+ str(dt.now().month) +  "-" +str(dt.now().day) +  "-" + str(dt.now().hour) +   "-" + str(dt.now().minute) +  "-"+ str(dt.now().second)

    with open(filename+'people.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(df)
    print (keys)
   

    
def handlText(text,listjson,room_master):
    
    words = cm.Common.clean_text(text)
    

    words = words.split(" ") 
    listHotel = {}
    hotelType=""
    bedType =""
    bed=""
    roomType=""
    view=""

    for word in words:
        if word !="":
            for item in listjson["hotelTyleName"]:
               
                if item['name'] == word and item['name'] not in hotelType:
                    hotelType =hotelType + word+ " "
              
            for item in listjson["bedName"]:
                
                if item['name'] == word and item['name'] not in bedType:
                    bedType =bedType +word +" "
            
            for item in listjson["bedtypeName"]:
                
                if item['name'] == word  and item['name'] not in bed:
                    bed =bed+ word + " "
              
            for item in listjson["roomTypeName"]:
                
                if item['name'] == word  and item['name'] not in roomType:
                    roomType =roomType+ word+ " "
              
            for item in listjson["viewName"] :
                if item['name'] == word   and item['name'] not in view:
                    view =view+ word + " "

    if hotelType.strip() =="":
        hotelType = "Standart"
    else:
        hotelType.strip()
    if bedType.strip() =="":
        bedType = "Other"
    else:
        bedType.strip()
    if bed.strip() =="":
        bed = "Other"
    else:
        bed.strip()
    if roomType.strip() =="":
        roomType = "Other"
    else:
        roomType.strip()
    if view.strip() =="":
        view = "Other"
    else:
        view.strip()
    
    listHotel["hotelType"] =hotelType
    listHotel["bedType"] =bedType
    listHotel["bed"] =bed
    listHotel["roomType"] =roomType
    listHotel["view"] =view
    listHotel["origin"] = text
    listHotel["room_master"] = room_master
    
    return listHotel
    #for item,value in listjson.items():
      #  print()
        #print(value[0]["name"])
        
            
def readjson(file):
    with open(file,'r') as json_file:  
        data = json.load(json_file)
        return data
        
saveCsv()