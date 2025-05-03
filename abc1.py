# -*- coding: utf-8 -*-


import pandas as pd

data=pd.read_csv("/content/insurance.csv")

data.head()

data.tail()

data.shape

print("Number of Rows",data.shape[0])
print("Number of Columns",data.shape[1])

data.info()

data.isnull().sum()

data.describe(include='all')

data['sex'].unique()
data['sex']=data['sex'].map({'female':0,'male':1})
data['smoker']=data['smoker'].map({'yes':1,'no':0})
data['region']=data['region'].map({'southwest':1,'southeast':2,
                   'northwest':3,'northeast':4})

X = data.drop(['charges'],axis=1)
y = data['charges']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

lr = LinearRegression()
lr.fit(X_train,y_train)
svm = SVR()
svm.fit(X_train,y_train)
rf = RandomForestRegressor()
rf.fit(X_train,y_train)
gr = GradientBoostingRegressor()
gr.fit(X_train,y_train)

y_pred1 = lr.predict(X_test)
y_pred2 = svm.predict(X_test)
y_pred3 = rf.predict(X_test)
y_pred4 = gr.predict(X_test)

df1 = pd.DataFrame({'Actual':y_test,'Lr':y_pred1,
                  'svm':y_pred2,'rf':y_pred3,'gr':y_pred4})

df1

import matplotlib.pyplot as plt

from sklearn import metrics

score1 = metrics.r2_score(y_test,y_pred1)
score2 = metrics.r2_score(y_test,y_pred2)
score3 = metrics.r2_score(y_test,y_pred3)
score4 = metrics.r2_score(y_test,y_pred4)

print(score1,score2,score3,score4)

s1 = metrics.mean_absolute_error(y_test,y_pred1)
s2 = metrics.mean_absolute_error(y_test,y_pred2)
s3 = metrics.mean_absolute_error(y_test,y_pred3)
s4 = metrics.mean_absolute_error(y_test,y_pred4)

print(s1,s2,s3,s4)

data = {'age' : 40,
        'sex' : 1,
        'bmi' : 40.30,
        'children' : 4,
        'smoker' : 1,
        'region' : 2}

df = pd.DataFrame(data,index=[0])
df

new_pred = gr.predict(df)
print("Medical Insurance cost for New Customer is : ",new_pred[0])

gr = GradientBoostingRegressor()
gr.fit(X,y)

new_pred = gr.predict(df)
print("Medical Insurance cost for New Customer is : ",new_pred[0])

import joblib

joblib.dump(gr,'model_joblib_gr')

model =joblib.load('model_joblib_gr')

model.predict(df)

"""GUI"""