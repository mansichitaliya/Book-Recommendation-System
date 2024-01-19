#make necesarry imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation, cosine
import ipywidgets as widgets
from IPython.display import display, clear_output
from sklearn.metrics import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt
import sys, os
from contextlib import contextmanager

#M is user-item ratings matrix where ratings are integers from 1-10
M = np.asarray([[3,7,4,9,9,7], 
                [7,0,5,3,8,8],
               [7,5,5,0,8,4],
               [5,6,8,5,9,8],
               [5,8,8,8,10,9],
               [7,7,0,4,7,8]])
M=pd.DataFrame(M)

#declaring k,metric as global which can be changed by the user later
global k,metric
k=4
metric='cosine' #can be changed to 'correlation' for Pearson correlation similaries
# print('Matrix')
# print(M)
# User-based Recommendation Systems
#get cosine similarities for ratings matrix M; pairwise_distances returns the distances between ratings and hence
#similarities are obtained by subtracting distances from 1
cosine_sim = 1-pairwise_distances(M, metric="cosine")
# print('cosine similaritie Matrix')
# print(pd.DataFrame(cosine_sim))
#get pearson similarities for ratings matrix M
pearson_sim = 1-pairwise_distances(M, metric="correlation")

#Pearson correlation similarity matrix
# print('correlation similaritie Matrix')
# print(pd.DataFrame(pearson_sim))
#This function finds k similar users given the user_id and ratings matrix M
#Note that the similarities are same as obtained via using pairwise_distances
def findksimilarusers(user_id, ratings, metric = metric, k=k):
    similarities=[]
    indices=[]
    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute') 
    model_knn.fit(ratings)

    distances, indices = model_knn.kneighbors(ratings.iloc[user_id-1, :].values.reshape(1, -1), n_neighbors = k+1)
    similarities = 1-distances.flatten()
    # print ('{0} most similar users for User {1}:\n'.format(k,user_id))
    for i in range(0, len(indices.flatten())):
        if (indices.flatten()[i]+1 == user_id):
            continue;

        else:
            #print ('{0}: User {1}, with similarity of {2}'.format(i, indices.flatten()[i]+1, similarities.flatten()[i]))
            pass
    return similarities,indices
# similarities,indices = findksimilarusers(1,M, metric='cosine')
# print('findksimilarusers')
# print(similarities, indices)
# similarities,indices = findksimilarusers(1,M, metric='correlation')
# print('findksimilarusers')
# print(similarities, indices)
#This function predicts rating for specified user-item combination based on user-based approach
def predict_userbased(user_id, item_id, ratings, metric = metric, k=k):
    prediction=0
    similarities, indices=findksimilarusers(user_id, ratings,metric, k) #similar users based on cosine similarity
    mean_rating = ratings.loc[user_id-1,:].mean() #to adjust for zero based indexing
    sum_wt = np.sum(similarities)-1
    product=1
    wtd_sum = 0 
    
    for i in range(0, len(indices.flatten())):
        if (indices.flatten()[i]+1 == user_id):
            continue;
        else: 
            ratings_diff = ratings.iloc[indices.flatten()[i],item_id-1]-np.mean(ratings.iloc[indices.flatten()[i],:])
            product = ratings_diff * (similarities[i])
            wtd_sum = wtd_sum + product
    
    prediction = int(round(mean_rating + (wtd_sum/sum_wt)))
    # print ('\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id,item_id,prediction))

    return prediction
# print('user based')
# print(predict_userbased(3,4,M))
# Item-based Recommendation Systems
#This function finds k similar items given the item_id and ratings matrix M

def findksimilaritems(item_id, ratings, metric=metric, k=k):
    similarities=[]
    indices=[]    
    ratings=ratings.T
    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute')
    model_knn.fit(ratings)

    distances, indices = model_knn.kneighbors(ratings.iloc[item_id-1, :].values.reshape(1, -1), n_neighbors = k+1)
    similarities = 1-distances.flatten()
    # print ('{0} most similar items for item {1}:\n'.format(k,item_id))
    for i in range(0, len(indices.flatten())):
        if (indices.flatten()[i]+1 == item_id):
            continue;

        else:
            pass
            # print ('{0}: User {1}, with similarity of {2}'.format(i, indices.flatten()[i]+1, similarities.flatten()[i]))

    return similarities,indices

similarities,indices=findksimilaritems(3,M)
# print('fink k similar items')
# print(similarities, indices)
#mbination based on item-based approach
def predict_itembased(user_id, item_id, ratings, metric = metric, k=k):
    prediction= wtd_sum =0
    similarities, indices=findksimilaritems(item_id, ratings) #similar users based on correlation coefficients
    sum_wt = np.sum(similarities)-1
    product=1
    
    for i in range(0, len(indices.flatten())):
        if (indices.flatten()[i]+1 == item_id):
            continue;
        else:
            product = ratings.iloc[user_id-1,indices.flatten()[i]] * (similarities[i])
            wtd_sum = wtd_sum + product                              
    prediction = int(round(wtd_sum/sum_wt))
    # print ('\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id,item_id,prediction))    

    return prediction
prediction = predict_itembased(1,3,M)
# print('predict item based')
# print(prediction)
#This function is used to compute adjusted cosine similarity matrix for items
def computeAdjCosSim(M):
    sim_matrix = np.zeros((M.shape[1], M.shape[1]))
    M_u = M.mean(axis=1) #means
          
    for i in range(M.shape[1]):
        for j in range(M.shape[1]):
            if (i == j):
                
                sim_matrix[i][j] = 1
            else:                
                if i<j:
                    
                    sum_num = sum_den1 = sum_den2 = 0
                    for k,row in M.loc[:,[i,j]].iterrows(): 

                        if ((M.loc[k,i] != 0) & (M.loc[k,j] != 0)):
                            num = (M[i][k]-M_u[k])*(M[j][k]-M_u[k])
                            den1= (M[i][k]-M_u[k])**2
                            den2= (M[j][k]-M_u[k])**2
                            
                            sum_num = sum_num + num
                            sum_den1 = sum_den1 + den1
                            sum_den2 = sum_den2 + den2
                        
                        else:
                            continue                          
                                       
                    den=(sum_den1**0.5)*(sum_den2**0.5)
                    if (den!=0):
                        sim_matrix[i][j] = sum_num/den
                    else:
                        sim_matrix[i][j] = 0


                else:
                    sim_matrix[i][j] = sim_matrix[j][i]           
            
    return pd.DataFrame(sim_matrix)
adjcos_sim = computeAdjCosSim(M)
# print('adjusted cosine similarity')
# print(adjcos_sim)
#This function finds k similar items given the item_id and ratings matrix M

def findksimilaritems_adjcos(item_id, ratings, k=k):
    
    sim_matrix = computeAdjCosSim(ratings)
    similarities = sim_matrix[item_id-1].sort_values(ascending=False)[:k+1].values
    indices = sim_matrix[item_id-1].sort_values(ascending=False)[:k+1].index
    
    # print ('{0} most similar users for User {1}:\n'.format(k,item_id))
    for i in range(0, len(indices)):
            if (indices[i]+1 == item_id):
                continue;

            else:
                pass
                # print ('{0}: User {1}, with similarity of {2}'.format(i, indices[i]+1, similarities[i]))
        
    return similarities ,indices
similarities, indices = findksimilaritems_adjcos(3,M)
# print('find k similar adjusted cosine similarity')
# print(similarities, indices)
#This function predicts the rating for specified user-item combination for adjusted cosine item-based approach
#As the adjusted cosine similarities range from -1,+1, sometimes the predicted rating can be negative or greater than max value
#Hack to deal with this: Rating is set to min if prediction is negative, Rating is set to max if prediction is above max
def predict_itembased_adjcos(user_id, item_id, ratings):
    prediction=0

    similarities, indices=findksimilaritems_adjcos(item_id, ratings) #similar users based on correlation coefficients
    sum_wt = np.sum(similarities)-1

    product=1
    wtd_sum = 0 
    for i in range(0, len(indices)):
        if (indices[i]+1 == item_id):
            continue;
        else:
            product = ratings.iloc[user_id-1,indices[i]] * (similarities[i])
            wtd_sum = wtd_sum + product                              
    prediction = int(round(wtd_sum/sum_wt))
    if (prediction < 0):
        prediction = 1
    elif (prediction >10):
        prediction = 10
    # print ('\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id,item_id,prediction))      
        
    return prediction
prediction=predict_itembased_adjcos(3,4,M)
# print('adjusted similarity',adjcos_sim)
#This function utilizes above function to recommend items for selected approach. Recommendations are made if the predicted
#rating for an item is greater than or equal to 6, and the items has not been rated already
def recommendItemUBCosine(user_id, item_id, ratings):
    
    prediction = 0
    if (user_id<1 or user_id>6 or type(user_id) is not int):
        print ('Userid does not exist. Enter numbers from 1-6')
    else:        
        metric = 'cosine'
        prediction = predict_userbased(user_id, item_id, ratings, metric)
                   
        if (ratings[item_id-1][user_id-1] != 0): 
            print('Item already rated')
        else:
            if (prediction>=6):
                print('\nItem recommended')
            else:
                print('Item not recommended')

def recommendItemUBCorrelation(user_id, item_id, ratings):
    
    prediction = 0
    if (user_id<1 or user_id>6 or type(user_id) is not int):
        print ('Userid does not exist. Enter numbers from 1-6')
    else:    
        metric = 'correlation'               
        prediction = predict_userbased(user_id, item_id, ratings, metric)
                   
        if (ratings[item_id-1][user_id-1] != 0): 
            print('Item already rated')
        else:
            if (prediction>=6):
                print('\nItem recommended')
            else:
                print('Item not recommended')

def recommendItemIBCosine(user_id, item_id, ratings):
    
    prediction = 0
    if (user_id<1 or user_id>6 or type(user_id) is not int):
        print ('Userid does not exist. Enter numbers from 1-6')
    else:
        prediction = predict_itembased(user_id, item_id, ratings)
                   
        if (ratings[item_id-1][user_id-1] != 0): 
            print('Item already rated')
        else:
            if (prediction>=6):
                print('\nItem recommended')
            else:
                print('Item not recommended')

def recommendItemIBAdjCosine(user_id, item_id, ratings):
    
    prediction = 0
    if (user_id<1 or user_id>6 or type(user_id) is not int):
        print ('Userid does not exist. Enter numbers from 1-6')
    else:        
        prediction = predict_itembased_adjcos(user_id,item_id,ratings)
                
        if (ratings[item_id-1][user_id-1] != 0): 
            print('Item already rated')
        else:
            if (prediction>=6):
                print('\nItem recommended')
            else:
                print('Item not recommended')

        # approach.observe(on_change)
        # display(approach)
#check for incorrect entries
# print('recommendItemUBCosine')
# print(recommendItemUBCosine(-1,3,M))
# print('recommendItemUBCosine')
# print(recommendItemUBCorrelation(3,4,M))
# print('recommendItemUBCosine')
# print(recommendItemIBCosine(3,4,M))
# #if the item is already rated, it is not recommended
# print('recommendItemUBAdjCosine')
# print(recommendItemIBAdjCosine(3,4,M))
#This is final function to evaluate the performance of selected recommendation approach and the metric used here is RMSE
#suppress_stdout function is used to suppress the print outputs of all the functions inside this function. It will only print 
#RMSE values
def evaluateRSUBCosine(ratings):
    
    n_users = ratings.shape[0]
    n_items = ratings.shape[1]
    prediction = np.zeros((n_users, n_items))
    prediction= pd.DataFrame(prediction)
    metric = 'cosine'
    for i in range(n_users):
        for j in range(n_items):
            prediction[i][j] = predict_userbased(i+1, j+1, ratings, metric)
    MSE = mean_squared_error(prediction, ratings)
    RMSE = round(sqrt(MSE),3)
    print("MSE using evaluateRSUBCosine approach is: {0}".format(MSE))
    print("RMSE using evaluateRSUBCorrelation approach is: {0}".format(RMSE))
def evaluateRSUBCorrelation(ratings):
    
    n_users = ratings.shape[0]
    n_items = ratings.shape[1]
    prediction = np.zeros((n_users, n_items))
    prediction= pd.DataFrame(prediction)
                # elif (approach.value == 'User-based CF (correlation)')  :                       
    metric = 'correlation'               
    for i in range(n_users):
        for j in range(n_items):
            prediction[i][j] = predict_userbased(i+1, j+1, ratings, metric)
    MSE = mean_squared_error(prediction, ratings)
    RMSE = round(sqrt(MSE),3)
    print("MSE using evaluateRSUBCorrelation approach is: {0}".format(MSE))
    print("RMSE using evaluateRSUBCorrelation approach is: {0}".format(RMSE))
def evaluateRSIBCosine(ratings):
    
    n_users = ratings.shape[0]
    n_items = ratings.shape[1]
    prediction = np.zeros((n_users, n_items))
    prediction= pd.DataFrame(prediction)
    # elif (approach.value == 'Item-based CF (cosine)'):
    for i in range(n_users):
        for j in range(n_items):
            prediction[i][j] = predict_userbased(i+1, j+1, ratings)
    MSE = mean_squared_error(prediction, ratings)
    RMSE = round(sqrt(MSE),3)
    print("MSE using evaluateRSIBCosine approach is: {0}".format(MSE))
    print("RMSE using evaluateRSIBCosine approach is: {0}".format(RMSE))
def evaluateRSIBAdjCosine(ratings):
    
    n_users = ratings.shape[0]
    n_items = ratings.shape[1]
    prediction = np.zeros((n_users, n_items))
    prediction= pd.DataFrame(prediction)
    # else:
    for i in range(n_users):
        for j in range(n_items):
            prediction[i][j] = predict_userbased(i+1, j+1, ratings) 
    MSE = mean_squared_error(prediction, ratings)
    RMSE = round(sqrt(MSE),3)
    print("MSE using evaluateRSIBAdjCosine approach is: {0}".format(MSE))
    print("RMSE using evaluateRSIBAdjCosine approach is: {0}".format(RMSE))
print('evaluateRSUBCosine')
evaluateRSUBCosine(M)
print('evaluateRSUBCorrelation')
evaluateRSUBCorrelation(M)
print('evaluateRSIBCosine')
evaluateRSIBCosine(M)
print('evaluateRSIBAdjCosine')
evaluateRSIBAdjCosine(M)
