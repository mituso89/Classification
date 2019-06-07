

import os,sys
import json
from common.common import Common

class CheckMaster():

    
        

    def handle(text):
        script_dir = os.path.split(os.path.dirname(os.path.realpath('__file__')))[0]
        check = {"View":0,"Bed":0,"BedType":0}        
            
        listarray = {"bedName":"bed.json","bedtypeName":"bedtype.json","viewName":"view.json"}
        rel_path = "room_master_api_machinelearning/share"
                
        listjson={}

        for key in listarray.items():

            bs_file_path = os.path.join(script_dir, (rel_path + "/"+ "{}").format(key[1]))
                                   
            getvalue = CheckMaster.readjson(bs_file_path)
                    
            listjson[key[0]] = getvalue
                
        words = Common.clean_text(text)
        words = words.split(" ")      
        print (words)
        for word in words:
            if word !="":
                
                
                for item in listjson["viewName"]:
                    
                    if item['name'] == word:
                        check["View"] =1
                
                for item in listjson["bedtypeName"]:
                    
                    if item['name'] == word:
                        check["BedType"] =1 
                        

                for item in listjson["bedName"]:
                    if item['name'] == word:
                        check["Bed"] =1 
            
        
        return check
        

       
    

    

    def readjson(file):
        with open(file,'r') as json_file:  
            data = json.load(json_file)
                
            return data    


  

      
    
