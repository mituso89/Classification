import pandas as pd
from model.svm_model import SVMModel
from model.naive_bayes_model import NaiveBayesModel
from sklearn.feature_extraction.text import TfidfVectorizer
from model.svm_model import SVMModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from time import time
from sklearn.feature_selection import SelectPercentile, f_classif
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
import pickle
import common.common as cm
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


class TextClassificationPredict(object):

   
    def __init__(self):
        self.test = None


    def connectMysql():
        try:
            mySQLconnection = mysql.connector.connect(host='13.251.123.143',port='3306',database='HotelGatewayNew',user='hotelgateway',password='SeechoitlOfwoRwObEaphOabdLVy')
            sql_select_Query = "SELECT room_name,master_room_type FROM HotelGatewayNew.room_type_mapping where master_room_type is not null"
            cursor = mySQLconnection .cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            cursor.close()
            
            df = pd.read_sql(sql_select_Query,mySQLconnection)
            return df
        except Error as e :
            print ("Error while connecting to MySQL", e)
        finally:
            #closing database connection.
            if(mySQLconnection .is_connected()):
                mySQLconnection.close()
                print("MySQL connection is closed")
    def save_model(filename, clf):
        with open(filename, 'wb') as f:
            pickle.dump(clf, f)

    
        

    def clean_text(text):
        REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
        BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
        STOPWORDS = set(stopwords.words('english'))
        """
            text: a string
            
            return: modified initial string
        """
        
        text = text.lower() # lowercase text
        text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
        text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
        text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
        return text

    def get_train_data(self):
        common = cm.Common()
        #  train data

        url = "/home/ubutu/Documents/Untitled1.csv"
        train_data = TextClassificationPredict.connectMysql()
     
        df_train = pd.DataFrame(train_data)

        print(df_train.iloc[3714])

        df_train['room_name'] = df_train["room_name"].apply(TextClassificationPredict.clean_text)

        print(df_train.iloc[3714])

        target = train_data['master_room_type']
        
        traindata, testdata,labels_train, labels_test = train_test_split(df_train,target, test_size = 0.2, random_state = 10)

        model = NaiveBayesModel()
   
        clf = model.clf.fit(traindata["room_name"], traindata.master_room_type)
            
        predicted = clf.predict(testdata['room_name'].apply(TextClassificationPredict.clean_text))
         
        print (predicted)
        print('accuracy %s' % accuracy_score(predicted, labels_test))
        a = clf.predict_proba(testdata["room_name"])
        TextClassificationPredict.save_model(os.path.abspath(os.path.dirname(__file__)) + "/x_transformer.pkl", clf)
     
    

        

if __name__ == '__main__':
    tcp = TextClassificationPredict()
    tcp.get_train_data()


    