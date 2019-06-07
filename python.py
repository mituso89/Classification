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
import csv


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

    def readCSV(filename):

        df = pd.read_csv(filename)
        return df

    def clean_text(text):
        REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;-]')
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
        
        url = "people.csv"
        #train_data = TextClassificationPredict.connectMysql()
        
        train_data = TextClassificationPredict.readCSV(url)

        checkdata =  TextClassificationPredict.readCSV("peoplemaster.csv")
        print(checkdata)

        
       
        df_train = pd.DataFrame(train_data)
        chectrain = pd.DataFrame(checkdata)

        df_train['category_id'] = df_train['master_room_type'].factorize()[0]
        train_outcome = pd.crosstab(index=train_data["master_room_type"],  # Make a crosstab
                              columns="count")      # Name the count column

        
        df_train['room_name'] = df_train["room_name"].apply(TextClassificationPredict.clean_text)
        chectrain['room_name'] = chectrain["room_name"].apply(TextClassificationPredict.clean_text)

        
        dfview = df_train.drop(df_train[ df_train['view'] == "Other" ].index )
        dfBedType = df_train.drop(df_train[ df_train['bedType'] == "Other" ].index )
        dfBed = df_train.drop(df_train[ df_train['bed'] == "Other" ].index )

        
        

        #target = train_data['master_room_type']
        target = checkdata['master_room_type']
        targetview = dfview['view']

        
        targetBedType = dfBedType['bedType']
        targetBed = dfBed['bed']
        
      
        traindata, testdata,labels_train, labels_test = train_test_split(chectrain,target, test_size = 0.2, random_state = 10)
        traindataview, testdataview,labels_trainview, labels_testview = train_test_split(dfview,targetview, test_size = 0.2, random_state = 10)
        traindataBedType, testdataBedType,labels_trainBedType, labels_testBedType = train_test_split(dfBedType,targetBedType, test_size = 0.2, random_state = 10)
        traindataBed, testdataBed,labels_trainBed, labels_testBed = train_test_split(dfBed,targetBed, test_size = 0.2, random_state = 10)

        #model = NaiveBayesModel()
        model = SVMModel()
        modelview = SVMModel()
        modelBedType = SVMModel()
        modelBed = SVMModel()
       
        clf = model.clf.fit(traindata["room_name"], traindata.master_room_type)
        clfview = modelview.clf.fit(traindataview["room_name"], traindataview.view)
        clfBedType = modelBedType.clf.fit(traindataBedType["room_name"], traindataBedType.bedType)
        clfBed = modelBed.clf.fit(traindataBed["room_name"], traindataBed.bed)
        
        predicted = clf.predict(testdata['room_name'].apply(TextClassificationPredict.clean_text))
        predictedview = clfview.predict(testdataview['room_name'].apply(TextClassificationPredict.clean_text))
        predictedBedType = clfBedType.predict(testdataBedType['room_name'].apply(TextClassificationPredict.clean_text))
        predictedBed = clfBed.predict(testdataBed['room_name'].apply(TextClassificationPredict.clean_text))
         
        #print (predicted)
        print('accuracy %s' % accuracy_score(predicted, labels_test))
        print('accuracyView %s' % accuracy_score(predictedview, labels_testview))
        print('accuracyBedType %s' % accuracy_score(predictedBedType, labels_testBedType))
        print('accuracyBed %s' % accuracy_score(predictedBed, labels_testBed))
        
        a = clf.predict_proba(testdata["room_name"])
        TextClassificationPredict.save_model(os.path.abspath(os.path.dirname(__file__)) + "/x_transformer.pkl", clf)
        TextClassificationPredict.save_model(os.path.abspath(os.path.dirname(__file__)) + "/x_transformerView.pkl", clfview)
        TextClassificationPredict.save_model(os.path.abspath(os.path.dirname(__file__)) + "/x_transformerBedType.pkl", clfBedType)
        TextClassificationPredict.save_model(os.path.abspath(os.path.dirname(__file__)) + "/x_transformerViewBed.pkl", clfBed)


        dt = pd.DataFrame(testdata)
        dt["predicted"] = predicted

        #dt.to_csv("test.csv")
      
       

        

if __name__ == '__main__':
    tcp = TextClassificationPredict()
    tcp.get_train_data()


    