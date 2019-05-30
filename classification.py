import pickle
import pandas as pd
import os
import common.common as cm
from time import time




def classification(room_name):

    room_name = cm.Common.clean_text(room_name)
    test_data = []
    test_data.append({"room_name": room_name, "master_room_type": "Executive Suite"})
    t0 = time()
    df_test = pd.DataFrame(test_data)
    loaded_model = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformer.pkl", 'rb'))
    loaded_modelView = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformerView.pkl", 'rb'))
    loaded_modelBedType = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformerBedType.pkl", 'rb'))
    loaded_modelBed = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformerViewBed.pkl", 'rb'))

    result = loaded_model.predict(df_test['room_name'])
    resultview =  loaded_modelView.predict(df_test['room_name'])
    resultBedType =  loaded_modelBedType.predict(df_test['room_name'])
    resultviewBed =  loaded_modelBed.predict(df_test['room_name'])

    print(time() -t0)
    print(room_name)
    print(result,resultview,resultBedType,resultviewBed)
    


classification("Twin Room - Deluxe - Executive - City View")    