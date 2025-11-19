#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def graph_of_data(df):
    #merge these columns, will be labels of the nodes
    df["Name"] = df["Candidate surname"].astype("str") +" " + df["Candidate First Name"].astype("str")
    #create the DiGraph
    G = nx.DiGraph()
    count_lst = list(df["Count Number"].unique())
    count_lst.remove(1)
    #DEBUG: print(count_lst)
    #filter by count
    for count in count_lst:
        filtered_df1 = df[df["Count Number"]==count]
        #DEBUG: filtered_df1
        #--get names of those whose votes are transferred
        src_cands = filtered_df1[filtered_df1["ln(Transfers)"]<0]
        #DEBUG: src_cands
        #--get names of those who receive these transfers
        to_cands =filtered_df1[filtered_df1["ln(Transfers)"]>0]
        #DEBUG: to_cands
        src_names = list(src_cands["Name"].values)
        #DEBUG: src_names
        to_names = list(to_cands["Name"].values)
        #DEBUG: to_names
        #--get number of transfers
        wgts = list(to_cands["ln(Transfers)"].values)
        #DEBUG: wgts
        
        #--Create a weighted edge between each source candidate and each target candidate
        
        for i in range(len(src_names)):
            edge_list = []
            for j in range(len(to_names)):
                edge = (src_names[i],to_names[j],wgts[j])
                print(edge)
                edge_list.append(edge)
            G.add_weighted_edges_from(edge_list)
    return G
    


# In[18]:


### make_networkx_from_csv.py
# DM and JMcG 30 Oct 2025
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def graph_of_data(df):
    #--Merge these columns, will be labels of the nodes
    df["Name"] = df["Candidate surname"].astype("str") +" " + df["Candidate First Name"].astype("str")
    #--Create the DiGraph
    G = nx.DiGraph()
    count_lst = list(df["Count Number"].unique())
    count_lst.remove(1)
    
    #--Filter by count
    for count in count_lst:
        filtered_df1 = df[df["Count Number"]==count]
        #--get names of those whose votes are transferred
        src_cands = filtered_df1[filtered_df1["Transfers"]<0]
        #--get names of those who receive these transfers
        to_cands =filtered_df1[filtered_df1["Transfers"]>0]
        src_names = list(src_cands["Name"].values)
        to_names = list(to_cands["Name"].values)
        
        #--get number of transfers
        
        wgts = []
        src_wgts = list(src_cands["Transfers"].values)
        to_wgts = list(to_cands["Transfers"].values)
        
        total=0
        for src_wgt in src_wgts:
            total+=src_wgt
        total=np.abs(total)
        
        for i in range(len(to_wgts)):
            
            quotient = to_wgts[i] / total
            #ln_quotient = np.log(quotient)
            normalised_wgt = quotient*np.log(to_wgts[i])
            wgts.append(round(normalised_wgt,2))
            
        for i in range(len(src_names)):
            for j in range(len(to_names)):
                G.add_edge(src_names[i],to_names[j],weight=wgts[j])
    return G


# In[19]:


G1 = graph_of_data(donegal_df)


# In[20]:


for i in G1.edges("Mc Guinness Arthur Desmond",data=True):
    print(i)


# In[22]:


for i in G1.edges("Doherty Pearse",data=True):
    print(i)


# In[21]:


plot_G(G1)


# In[10]:


def plot_G(G):
    #--Draw the graph
    plt.figure(figsize=(12, 12))
    #pos = nx.spring_layout(G, seed=42,k=1, iterations=100)
    #pos=nx.get_node_attributes(G,'pos')
    opts = {"with_labels":True,"node_size":600}
    nx.draw_circular(G,**opts)

    #nx.draw_networkx_labels(G, label_pos, font_size=10, font_color='black')
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=edge_labels)
    plt.title("Vote Transfers Graph")
    plt.savefig("filename1.png")
    plt.show()


# In[4]:


donegal_df = pd.read_excel("C:/Users/22358313/Desktop/University/BSc Fourth Year/FYP/Election_Data_CSVs/general_election_2020_count_details.xlsx",
                           engine='openpyxl',
                           sheet_name = "donegal-normalised")


# In[5]:


donegal_df


# In[7]:


def graph_of_data(df):
    #--Merge these columns, will be labels of the nodes
    df["Name"] = df["Candidate surname"].astype("str") +" " + df["Candidate First Name"].astype("str")
    #--Create the DiGraph
    G = nx.DiGraph()
    count_lst = list(df["Count Number"].unique())
    count_lst.remove(1)
    #--Filter by count
    for count in count_lst:
        filtered_df1 = df[df["Count Number"]==count]
        #--get names of those whose votes are transferred
        src_cands = filtered_df1[filtered_df1["Transfers"]<0]
        #--get names of those who receive these transfers
        to_cands =filtered_df1[filtered_df1["Transfers"]>0]
        src_names = list(src_cands["Name"].values)
        to_names = list(to_cands["Name"].values)

        #--add edge weights as the proportion of the src_cand's transfers the to_cand received.       
        src_wgts = list(src_cands["Transfers"].values)
        to_wgts = list(to_cands["Transfers"].values)

        #--if there's more than one src_cand per count, the number of transfers a candidate receives will a proportion of the this total
        total = np.abs(np.sum(src_wgts))

        wgts = [round(wgt/total, 2) for wgt in to_wgts]
            
        #--Create a weighted edge between each source candidate and each target candidate
        for i in range(len(src_names)):
            for j in range(len(to_names)):
                G.add_edge(src_names[i],to_names[j],weight=wgts[j])
    return G


# In[8]:


G2 = graph_of_data(donegal_df)


# In[11]:


plot_G(G2)


# In[9]:


for i in G2.edges("Mc Guinness Arthur Desmond",data=True):
    print(i)


# In[71]:


for i in G2.edges("Doherty Pearse",data=True):
    print(i)


# In[ ]:


communities = nx.community.louvain_communities(G2)

