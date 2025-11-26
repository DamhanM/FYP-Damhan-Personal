#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


full_df = pd.read_csv("C:/Users/22358313/Desktop/University/BSc Fourth Year/FYP/Election_Data_CSVs/General_Election_2020_full-231125.csv")


# In[12]:


def proportion_per_constituency(df,k):
    
    consti_lst = list(df["Constituency Name"].unique())
    #consti_lst = ['Carlow-Kilkenny', 'Cavan-Monaghan', 'Clare', 'Cork East', 'Cork North Central', 'Cork North West', 
                  #'Cork South Central', 'Cork South West', 'Donegal', 'Dublin Bay North']
    
    #DEBUG: print(consti_lst)
    
    #--Filter by constituency
    for i in range(len(consti_lst)):
        
        consti_df = df[df["Constituency Name"]==consti_lst[i]]
        count_lst = list(consti_df["Count Number"].unique())
        if k > count_lst[-1]:
            print("Inputted count number exceeds max counts in the election.")
            return None
    
    propn_lst = []
    for i in range(len(consti_lst)):
        
        non_t = 0
        total_valid = consti_df["Required To Reach Quota"].iloc[0] + consti_df["Votes"].iloc[0]
        print(total_valid)
        
        for count in range(k):
            
            consti_df = df[df["Constituency Name"]==consti_lst[i]]
            
            count_df = consti_df[consti_df["Count Number"]==count]

            non_t += -(np.sum(list(count_df["Transfers"].values)))

        propn = non_t/total_valid
        print(propn)
        propn_lst.append(propn)
        
    #DEBUG: print(len(propn_lst))
    all_consti_bar_chart(consti_lst,propn_lst,k)
    


# In[13]:


def get_propn_list(df,constituency):
       
    consti_df = df[df["Constituency Name"]==constituency] 
    
    count_lst = list(consti_df["Count Number"].unique())
    count_lst.remove(1)

    propn_lst = []
    total_valid = consti_df["Required To Reach Quota"].iloc[0] + consti_df["Votes"].iloc[0]

    non_t = 0
    for count in count_lst:

        count_df = consti_df[consti_df["Count Number"]==count]

        non_t += -(np.sum(list(count_df["Transfers"].values)))

        propn = non_t/total_valid
        
        propn_lst.append(propn)
        
    print(propn_lst)
    return count_lst, propn_lst


# In[14]:


def propn_per_count(df,constituency):
       
    consti_df = df[df["Constituency Name"]==constituency] 
    
    count_lst = list(consti_df["Count Number"].unique())
    count_lst.remove(1)

    propn_lst = []
    total_valid = consti_df["Required To Reach Quota"].iloc[0] + consti_df["Votes"].iloc[0]
    #print(total_valid)

    non_t = 0
    for count in count_lst:

        count_df = consti_df[consti_df["Count Number"]==count]

        non_t += -(np.sum(list(count_df["Transfers"].values)))

        propn = non_t/total_valid
        
        propn_lst.append(round(propn,3))
        
    #DEBUG: print(len(propn_lst))
    #print(propn_lst)
    all_counts_bar_chart(count_lst,propn_lst,constituency)
    #return count_lst, propn_lst


# In[15]:


def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center')  # Aligning text at center


# In[20]:


def all_consti_bar_chart(ct_lst,vals_lst,k):
    plt.bar(ct_lst, vals_lst, color='skyblue',width=0.4,align = "center")
    plt.ylim(top=0.15)
    plt.xticks(rotation  ="vertical")
    
    plt.title(f'Cumul Proportion of Non-transferable Votes for Count {k:1}')
    plt.xlabel('Constituency')
    plt.ylabel('Proportion')
    
    plt.tight_layout()
    file_name = "non-transferable_count_"+str(k)
    #plt.savefig(file_name)
    plt.show()


# In[19]:


def all_counts_bar_chart(ct_lst, vals_lst, constituency):
    
    plt.figure(figsize=(10, 5))
    plt.bar(ct_lst, vals_lst, color='skyblue',width=0.4,align = "center")
    add_labels(ct_lst,vals_lst)
    
    plt.title(f'Cumul Proportion of Non-transferable Votes for Constituency {constituency:1}')
    plt.xlabel('Count')
    plt.ylabel('Proportion')
    
    save_results_to = "C:/Users/22358313/Desktop/University/BSc Fourth Year/FYP/figures/"
    file_name = str(constituency)+"_non-t"
    #plt.savefig(save_results_to + file_name)
    plt.show()


# In[24]:


proportion_per_constituency(full_df, 5)


# In[10]:


propn_per_count(full_df,"Donegal")


# In[36]:


#full_df
consti_lst = list(full_df["Constituency Name"].unique())
print(consti_lst)


# In[82]:


(dub_nw_ct, dub_nw_propn) = get_propn_list(full_df,"Dublin North West")
#(fingal_ct, fingal_propn) = proportion_per_count(full_df, "Dublin Fingal")
(kil_n_ct, kil_n_propn) = get_propn_list(full_df,"Kildare North")
#(donegal_ct, donegal_propn) = proportion_per_count(full_df, "Donegal")
(lim_county_ct, lim_county_propn) = get_propn_list(full_df, "Limerick County")


# In[86]:


barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

a = dub_nw_propn 
b = kil_n_propn
c = lim_county_propn

br1 = np.arange(len(a)) 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

plt.bar(br1, a, color ='r', width = barWidth, 
        edgecolor ='grey', label ='Dub NW') 
plt.bar(br2, b, color ='g', width = barWidth, 
        edgecolor ='grey', label ='Kildare North') 
plt.bar(br3, c, color ='b', width = barWidth, 
        edgecolor ='grey', label ='Lim County') 

plt.xlabel('Constituency', fontweight ='bold', fontsize = 15) 
plt.ylabel('Proportion', fontweight ='bold', fontsize = 15) 
plt.xticks([r + barWidth for r in range(len(a))], 
        ['2', '3', '4', '5', '6'])

plt.legend()

save_results_to = "C:/Users/22358313/Desktop/University/BSc Fourth Year/FYP/figures/"
file_name = "multiple_non-t_consti"
plt.savefig(save_results_to + file_name)

plt.show()


# In[62]:


result_df = (
    full_df.groupby("Constituency Name")["Count Number"]
    .max()
    .reset_index()
    .rename(columns={"Count Number": "Num Counts"})
    .sort_values(by="Max Count", ascending=False)
)


# In[65]:


candidate_counts = (
    full_df.groupby("Constituency Name")["Candidate surname"]
    .nunique()  # Use .nunique() for unique candidate names
    .reset_index()
    .rename(columns={"Candidate surname": "Num Candidates"})
)
result_df = result_df.merge(candidate_counts, on="Constituency Name")


# In[68]:


result_df


# In[ ]:




