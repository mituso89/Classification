from flask import Flask, request
from flask_restful import Resource, Api
import pickle
import pandas as pd
import os
import common.common as cm
from time import time

from json import dumps
#from flask.ext.jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self,employee_id):
        room_name = employee_id
        room_name = cm.Common.clean_text(room_name)
        test_data = []
        test_data.append({"room_name": room_name, "master_room_type": "Executive Suite"})
        t0 = time()
        df_test = pd.DataFrame(test_data)
        loaded_model = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformer.pkl", 'rb'))
       

        result = {"room_master":loaded_model.predict(df_test['room_name'])[0]}

        
        print(room_name)
        print(result)
        return result

api.add_resource(Employees, '/employees/<employee_id>') # Route_1



if __name__ == '__main__':
     app.run(host="0.0.0.0")