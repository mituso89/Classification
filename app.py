from flask import Flask, request,json
from flask_restful import Resource, Api
import pickle
import pandas as pd
import os
import common.common as cm
from time import time

from json import dumps
from common.checkSubMaster import CheckMaster
#from flask.ext.jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

class Roommaster(Resource):
    def post(self):
        name =""
        if request.headers['Content-Type'] == 'application/json':
            name= (request.json)["data"]
        else:
            return "415 Unsupported Media Type",400
        
        
       
        roommaster_id = name
        room_name = roommaster_id
        room_name = cm.Common.clean_text(room_name)
        test_data = []
        test_data.append({"room_name": room_name, "master_room_type": "Executive Suite"})
        t0 = time()
        df_test = pd.DataFrame(test_data)
        loaded_model = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformer.pkl", 'rb'))
        loaded_modelView = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformerView.pkl", 'rb'))
        loaded_modelBedType = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformerBedType.pkl", 'rb'))
        loaded_modelBed = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformerViewBed.pkl", 'rb'))

        check = CheckMaster.handle(room_name)
        print(check)
        if(check["View"]==1):
            resultview =  loaded_modelView.predict(df_test['room_name'])[0]
        else:
            resultview=""
        if(check["Bed"]==1):

            resultBed =  loaded_modelBed.predict(df_test['room_name'])[0]
            print(loaded_modelBed.predict(df_test['room_name']))
        else:
            resultBed=""
        if(check["BedType"]==1):
            resultBedType =  loaded_modelBedType.predict(df_test['room_name'])[0]
        else:
            resultBedType=""
        
       

        result = {"Room_master":str(loaded_model.predict(df_test['room_name'])[0]),"Bed":resultBed,"View":resultview,"BedType":resultBedType}
        
        return result

api.add_resource(Roommaster, '/roommaster') # Route_1



if __name__ == '__main__':
     app.run(host="0.0.0.0")