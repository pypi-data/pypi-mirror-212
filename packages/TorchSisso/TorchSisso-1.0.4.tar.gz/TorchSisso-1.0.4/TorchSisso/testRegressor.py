#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:101:33 2023

@author: muthyala.7
"""

import FeatureSpaceConstruction
import Feature_space_construction_1
import SISSORegressor
import SISSORegressor_L1L0
import FC_copy
import torch
import numpy as np 
import pandas as pd 
import time
import os 
from sklearn.linear_model import LassoCV
from sklearn.metrics import mean_squared_error

'''
########################################################################################################

#CaseStudy - 1

#######################################################################################################
'''
x = [np.random.uniform(0,2,size=10) for i in range(5)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
operators = ['+','/']
y = 10*((df.iloc[:,0])/(df.iloc[:,1]*(df.iloc[:,2]+df.iloc[:,3]))) + 3 + 0.01*np.random.normal(0,1,10)
df.insert(0,'Target',y)
start = time.time()
fc = FeatureSpaceConstruction.feature_space_construction(operators,df,3,'cuda')
df_created = fc.feature_space()

#Create Instace for class 
x = torch.tensor(df_created.iloc[:,1:].values)
y = torch.tensor(df_created.iloc[:,0])
names = df_created.iloc[:,1:].columns
sr = SISSORegressor.SISSO_Regressor(x,y,names,1,20,'cuda','L0')
rmse, equation = sr.SISSO()
print('SISSO Completed',time.time()-start,'\n')
print('\n')

#Implementing LASSO on the initial dataset
x = df.iloc[:,1:]
y = df.iloc[:,0]
lasso = LassoCV(cv=10)
lasso.fit(x,y)
y_pred = lasso.predict(x)
rmse1 = np.sqrt(mean_squared_error(y,y_pred))
print('RMSE of the LASSO implementation on initial dataset: ',rmse1)
'''
x = df_created.iloc[:,1:]
y = df_created.iloc[:,0]
lasso = LassoCV(cv=10)
lasso.fit(x,y)
y_pred = lasso.predict(x)
rmse1 = np.sqrt(mean_squared_error(y,y_pred))
print('RMSE of the LASSO implementation on expanded dataset: ',rmse1)
'''
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/1/')
df.to_csv('train.csv')
df.insert(0,'Index',df.index)
df.to_csv('train.dat',sep='\t',index=False)

'''
###############################################################################################

#CaseStudy -2 
###############################################################################################
'''
x = [np.random.uniform(0,2,size=10) for i in range(5)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
y1 = 3*np.sqrt(df.iloc[:,1]) + 2.10*np.sin(df.iloc[:,2]) + 2.10 + 0.010*np.random.normal(0,1,10)
df.insert(0,'Target',y1)
operators = ['sqrt','sin']
start_c = time.time()
FC = FC_copy.feature_space_construction(operators, df,3,'cpu')
df_created = FC.feature_space()
#Create Instace for class 
x = torch.tensor(df_created.iloc[:,1:].values)
y = torch.tensor(df_created.iloc[:,0])
names = df_created.iloc[:,1:].columns
start = time.time()
sr = SISSORegressor.SISSO_Regressor(x,y,names,2,10,'cpu')
rmse, equation = sr.SISSO()
print(time.time()-start)
#sr = SISSORegressor_L1L0.SISSO_Regressor(x,y,names,2,10,'cuda','L1L0')
#rmse, equation = sr.SISSO()
start = time.time()
sr = SISSORegressor.SISSO_Regressor(x,y,names,2,10,'cuda')
rmse, equation = sr.SISSO()
print(time.time()-start)
print("SISSO Completed: ",time.time()-start_c,'\n')
import os 
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/2/')
df.to_csv('train.csv')
df.insert(0,'Index',df.index)
df.to_csv('train.dat',sep='\t',index=False)

'''
##########################################################################################################

#CaseStudy-3

#########################################################################################################
'''
x = [np.random.uniform(0,2,size=10) for i in range(3)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
y2 = 3*(np.exp(df.iloc[:,3])/(df.iloc[:,2]+np.exp(df.iloc[:,1]))) + 0.01*np.random.normal(0,1,10)
df.insert(0,'Target',y2)
operators = ['/','+','exp']
start_c = time.time()
start_f = time.time()
FC = FC_copy.feature_space_construction(operators, df,4,'cpu')
df_created= FC.feature_space()
print(time.time()-start_f)
stat = time.time()
#fc = FeatureSpaceConstruction.feature_space_construction(operators, df,4,'cpu')
#df_cret = fc.feature_space()
print(time.time()- stat)
#Create Instace for class 
x = torch.tensor(df_created.iloc[:,1:].values)
y = torch.tensor(df_created.iloc[:,0])
names = df_created.iloc[:,1:].columns
start = time.time()
sr = SISSORegressor.SISSO_Regressor(x,y,names,1,20,'cuda')
rmse, equation = sr.SISSO()

print("SISSO Completed: ",time.time()-start_c,'\n')
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/3/')
df.to_csv('train.csv')
df.insert(0,'Index',df.index)
df.to_csv('train.dat',sep='\t',index=False)

'''
##############################################################################################################

#CaseStudy 4

##############################################################################################################

'''
df = pd.read_csv('/home/muthyala.7/Downloads/NOMAD_TEST_FILE.csv')

operators = ['+','-','*','/']
start_time = time.time()
FC = FC_copy.feature_space_construction(operators, df,3,'cpu')
df_created = FC.feature_space()
x = torch.tensor(df_created.iloc[:,1:].values)
y = torch.tensor(df_created.iloc[:,0])
names = df_created.iloc[:,1:].columns

sr = SISSORegressor.SISSO_Regressor(x,y,names,3,20,'cpu')
rmse, equation = sr.SISSO()
print(rmse,'\n',equation,'\n')
print("SISSO Completed: ",time.time()-start_time,'\n')

'''
##########################################################################################################

#CaseStudy-5

#########################################################################################################
'''
x = [np.random.uniform(0,2,size=20) for i in range(10)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
y2 = 3*df.iloc[:,0]**3 + 2*df.iloc[:,1]**2 - 3.5*(df.iloc[:,2]) - 2 + 0.01*np.random.normal(0,1,size=20)
df.insert(0,'Target',y2)
operators = ['^3','^2']
start_c = time.time()
start_f = time.time()
FC = FeatureSpaceConstruction.feature_space_construction(operators, df,3,'cpu')
df_created= FC.feature_space()
x = torch.tensor(df_created.iloc[:,1:].values)
y = torch.tensor(df_created.iloc[:,0])
names = df_created.iloc[:,1:].columns
sr = SISSORegressor.SISSO_Regressor(x,y,names,3,5,'cpu')
rmse, equation = sr.SISSO()
print("SISSO Completed: ",time.time()-start_c,'\n')
#os.mkdir('/home/muthyala.7/TorchSisso/Case_Studies/4')
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/4/')
df.to_csv('train.csv')
df.insert(0,'Index',df.index)
df.to_csv('train.dat',sep='\t',index=False)





