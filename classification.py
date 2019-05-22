import pickle
import pandas as pd
import os
import common.common as cm




def classification(room_name):

    room_name = cm.Common.clean_text(room_name)
    test_data = []
    test_data.append({"room_name": room_name, "master_room_type": "Executive Suite"})

    df_test = pd.DataFrame(test_data)
    loaded_model = pickle.load(open(os.path.abspath(os.path.dirname(__file__))+ "/x_transformer.pkl", 'rb'))
    result = loaded_model.predict(df_test['room_name'])
    print(room_name)
    print(result)
    


classification("Family Deluxe Room")    