
import dask
import dask.dataframe as dd
import dask.array as da
from dask.delayed import delayed
import numpy as np
import pandas as pd
from dask.threaded import get


def load(filename):
    parts = [dask.delayed(pd.read_excel)(filename, sheet_name = 0)] 
    file_data = dd.from_delayed(parts)
    return file_data
    
def readDescription(file_data):
    file_word = np.array(file_data.Description)
    return file_word

def readJobTitle(file_data):
    file_job = np.array(file_data.Job_Title)
    return file_job


final_data=[]
def finaldata(file_word, file_job):
    for i in range(len(file_word)):
        data = str(file_word[i]).lower() +" "+ str(file_job[i]).lower()
        final_data.append(data)
        return final_data



def readClusterFile(filename) :
    colName = ['Blockchain','CyberSecurity','ArtificialIntelligence','RiskManagement','BigData','InformationTechnology','FinacialOperations','Business_Accounting']
    cluster_data = dd.read_csv(filename, names=colName)
    return cluster_data


# In[302]:


def readBlockchain(cluster_data) :
    block_list = np.array(cluster_data.Blockchain)
    return block_list
def readCyber(cluster_data) :
    cyber_list = np.array(cluster_data.CyberSecurity)
    return cyber_list
def readAI(cluster_data) :
    ai_list = np.array(cluster_data.ArtificialIntelligence)
    return ai_list
def readRisk(cluster_data) :
    risk_list = np.array(cluster_data.RiskManagement)
    return risk_list
def readBig(cluster_data) :
    big_list = np.array(cluster_data.BigData)
    return big_list
def readIT(cluster_data) :
    it_list = np.array(cluster_data.InformationTechnology)
    return it_list
def readFO(cluster_data) :
    fo_list = np.array(cluster_data.FinacialOperations)
    return fo_list
def readBA(cluster_data) :
    ba_list = np.array(cluster_data.Business_Accounting)
    return ba_list


# In[303]:


def categorizeData(block_list,cyber_list,ai_list,risk_list,big_list,it_list,fo_list,ba_list):
    cluster=[]
    category=[]
    fintech = ["Blockchain","Cyber Security","Artificial Intelligence and Data Science","Big Data","Information Technology"]
    non_fintech = ["Risk Management","Financial Operation","Business/Accounting"]
    data = {}
    #for word in file_word:
    for word in final_data:
        #print(word)
        block_count=0
        cyber_count=0
        ai_count=0
        risk_count=0
        big_count=0
        it_count=0
        fo_count=0
        ba_count=0
        word_list=[]
        for list_word in block_list:
            if(not list_word is np.nan):
                word_block_nbr = str(word).count(str(list_word).lower())
                block_count += word_block_nbr
        for list_word in cyber_list:
            if(not list_word is np.nan):
                word_cyber_nbr = str(word).count(str(list_word).lower())
                #if word_cyber_nbr != 0:
                 #   print(list_word)
                cyber_count += word_cyber_nbr
        for list_word in ai_list:
            if(not list_word is np.nan):
                word_ai_nbr = str(word).count(str(list_word).lower())
                #if word_ai_nbr != 0:
                 #   print(list_word)
                ai_count += word_ai_nbr
        for list_word in risk_list:
            if(not list_word is np.nan):
                word_risk_nbr = str(word).count(str(list_word).lower())
                #if word_risk_nbr != 0:
                 #   print(list_word)
                risk_count += word_risk_nbr
        for list_word in big_list:
            if(not list_word is np.nan):
                word_big_nbr = str(word).count(str(list_word).lower())
                #if word_big_nbr != 0:
                    #print(list_word)
                big_count += word_big_nbr
        for list_word in it_list:
            if(not list_word is np.nan):
                word_it_nbr = str(word).count(str(list_word).lower())
                #if word_it_nbr != 0:
                 #   print(list_word)
                it_count += word_it_nbr
        for list_word in fo_list:
            if(not list_word is np.nan):
                word_fo_nbr=0
                word_fo_nbr = str(word).count(str(list_word).lower())
                #print(list_word," ",word_fo_nbr)
                #if word_fo_nbr != 0:
                    #print(list_word)
                fo_count += word_fo_nbr
        for list_word in ba_list:
            if(not list_word is np.nan):
                word_ba_nbr = str(word).count(str(list_word).lower())
                ba_count += word_ba_nbr
        blockchain_tuple=("Blockchain",block_count)
        word_list.append(blockchain_tuple)
        cyber_tuple=("Cyber Security",cyber_count)
        word_list.append(cyber_tuple)
        ai_tuple=("Artificial Intelligence and Data Science",ai_count)
        word_list.append(ai_tuple)
        risk_tuple=("Risk Management",risk_count)
        word_list.append(risk_tuple)
        big_tuple=("Big Data",big_count)
        word_list.append(big_tuple)
        it_tuple=("Information Technology",it_count)
        word_list.append(it_tuple)
        fo_tuple=("Financial Operation",fo_count)
        word_list.append(fo_tuple)
        ba_tuple=("Business/Accounting",ba_count)
        word_list.append(ba_tuple)
        word_list.sort(key=lambda tup: tup[1], reverse=True)
        #print(word_list)
        if (str(word).count("blockchain")>1 or str(word).count("block chain")>1):
            cluster.append("Blockchain")
            category.append("Fintech")
        elif it_count>ai_count and it_count>cyber_count and it_count>big_count and it_count>20:
            cluster.append("Information Technology")
            category.append("Fintech")
        else:
            if word_list[0][1] >0:
                cluster.append(word_list[0][0])
                if word_list[0][0] in fintech:
                    category.append("Fintech")
                else:
                    category.append("Non Fintech")
            else:
                #print(word_list[0][0],":",word_list[0][1])
                cluster.append("Not available")
                category.append("Not available")
    data['cluster'] = cluster
    data['category'] = category
    return data


# In[304]:


def writeCategorizedData(data) :
  
    df = pd.read_excel("Final_Dataset.xlsx")
    df['Cluster'],df['Category']=data
    df.to_excel("Final_Dataset.xlsx")


# In[298]:


dsk = {'load-data' : (load,'Final_Dataset.xlsx'),
       'read-description' : (readDescription,'load-data'),
       'read-job-title' : (readJobTitle,'load-data'),
       'finaldata' : (finaldata,'read-description','read-job-title'),
       'cluster_data' : (readClusterFile,'cluster_data.csv'),
       'block_list' : (readBlockchain,'cluster_data'),
       'cyber_list' : (readCyber,'cluster_data'),
       'ai_list' : (readAI,'cluster_data'),
       'risk_list' : (readRisk,'cluster_data'),
       'big_list' : (readBig,'cluster_data'),
       'it_list' : (readIT,'cluster_data'),
       'fo_list' : (readFO,'cluster_data'),
       'ba_list' : (readBA,'cluster_data'),
       'categorizedData' : (categorizeData,'block_list','cyber_list','ai_list','risk_list','big_list','it_list','fo_list','ba_list'),
       'final_dataset' : (writeCategorizedData,'categorizedData')}


# In[299]:


get(dsk,['load-data','read-description','read-job-title','finaldata'])
get(dsk,['cluster_data','block_list','cyber_list','ai_list','risk_list','big_list','it_list','fo_list','ba_list'])
get(dsk,['categorizedData'])
get(dsk,['final_dataset'])



