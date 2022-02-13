#!/usr/bin/env python
# coding: utf-8

# # Libraries Imported

# In[595]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
#import the necessary libraries
import warnings
warnings.filterwarnings("ignore")


# ## Importing Data

# In[596]:


df_company=pd.read_csv(r"E:\PG Diploma\Investment Analysis Assignment\companies.csv",encoding='unicode_escape')
df_company.info()

df_rounds2=pd.read_csv("E:/PG Diploma/Investment Analysis Assignment/rounds2.csv",encoding= 'unicode_escape')
df_rounds2.info()


# In[597]:


# 1
df_rounds2.company_permalink.nunique()
# 2 
df_company.permalink.nunique()


# #### converting permalink in both round2 and company dataframe into upper  to avoid mismatch

# In[598]:


df_rounds2.company_permalink=df_rounds2.company_permalink.str.upper()
df_company.permalink=df_company.permalink.str.upper()


# #### Merging Rounds2 and Company dataset

# In[599]:


master_frame=pd.merge(left=df_rounds2,right=df_company,left_on="company_permalink",right_on="permalink",how="inner")
master_frame.info()


# ### Data Cleansing

# In[601]:


# deleting rows with no funding amount and blank permalink
master_frame.dropna(how='any',inplace=True,subset=['raised_amount_usd'])

master_frame.info()

# inseting Unfined value in country code for no value
master_frame.loc[master_frame.country_code.isna(),"country_code"]="Undefined"


# In[602]:


# setting to view value upto 2 decimal places
pd.set_option('display.float_format', lambda x: '%.2f' % x)


# # Venture investment is suitable for Spark Funds

# In[603]:


# mean and median comparison for each funding type
master_frame.groupby(["funding_round_type"]).aggregate({"raised_amount_usd":["mean","median"]})#.sort_values(ascending=False)


# In[604]:


# Top 9 countries with venture type investment 
top9_country=pd.DataFrame(master_frame[(master_frame.funding_round_type=="venture") & (master_frame.country_code!="Undefined")].groupby(["country_code"])["raised_amount_usd"].sum().sort_values(ascending=False)).head(9).reset_index()["country_code"]
top9_country


# In[605]:


# top 9 countries for relevant funding type 
top9=master_frame[(master_frame.funding_round_type=="venture") & (master_frame.country_code.isin(list(top9_country)))]
top9


# ### USA, GBR and IND as top enlish speaking invested countries

# In[607]:


# Investment distribution by country
top9.groupby(["country_code"])["raised_amount_usd"].sum().sort_values(ascending=False).head(9)


# In[608]:


## Extracting primary sector from category list
top9["primary_category"]=top9.category_list.str.split("|").str[0]
top9.head()


# # Importing mapping data mapping

# In[609]:


df_mapping=pd.read_csv(r"E:\PG Diploma\Investment Analysis Assignment\mapping.csv",encoding= 'unicode_escape')
df_mapping


# ### Reshaping the data structure

# In[610]:


# restructing dataframe in 2 columns to get cateory and their sector
df_mapping1=df_mapping.melt(id_vars=["category_list"], var_name="Sector", value_name="Flag")
# final mapping dataframe with category and relevant sector
df_map=df_mapping1[df_mapping1.Flag==1]
df_map.head()


# ### Merging master dataframe with mapping file to get sector of each company

# In[612]:


df_master=pd.merge(left=top9,right=df_map, left_on="primary_category", right_on="category_list", how="inner")
df_master.head()


# ### Top 3 countries dataframe

# In[615]:


df_D1=df_master[df_master.country_code=="USA"]
df_D1.head()

df_D2=df_master[df_master.country_code=="GBR"]
df_D2.head()

df_D3=df_master[df_master.country_code=="IND"]
df_D3.head()


# ## adding investment count and amount by sector

# In[616]:


df_D1=pd.merge(right=df_D1.groupby(["Sector"]).agg({'Flag' :'sum',"raised_amount_usd":"sum"}), left=df_D1,on="Sector",how="inner")
df_D2=pd.merge(right=df_D2.groupby(["Sector"]).agg({'Flag' :'sum',"raised_amount_usd":"sum"}), left=df_D2,on="Sector",how="inner")
df_D3=pd.merge(right=df_D3.groupby(["Sector"]).agg({'Flag' :'sum',"raised_amount_usd":"sum"}), left=df_D3,on="Sector",how="inner")


# In[ ]:





# # Functions to delete and renaming inconsistent column names appeared due to join

# In[617]:


# function to delete irrelevant column that were created  and rename columns to relevant name
def column_del_rename(frame):
    frame.drop(['category_list_y','Flag_x'],axis='columns', inplace=True)
    frame.rename(columns = {'category_list_x': 'category_list', 'Flag_y': 'Investment Count by Sector','raised_amount_usd_y': 'Total Investment by sector',"raised_amount_usd_x":"raised_amount_usd" }, inplace = True)
    print(frame.columns)
    return frame


# In[618]:


#using column_del_rename function to avoid repeating task for 3 frames
df_D1=column_del_rename(df_D1)

df_D2=column_del_rename(df_D2)

df_D3=column_del_rename(df_D3)


# # Funtion to avoid repeaed task of getting values for table 5.1 for 3 dataframes

# In[619]:


# function to get name of the sector at particular rank
def sector_position(df,pos):
    pos=pos-1
    sector=list(pd.DataFrame(df.Sector.value_counts()).reset_index().iloc[pos])[0]
    print()
    return sector


# function to display information required in table 5.1
def table_5_1(df):
        print("Total Investment Count: {}\n".format(df['company_permalink'].count()))
        print("Total Investment Amount: {}\n".format(df['raised_amount_usd'].sum()))
        print("\nTop 3 Sector with investment Count:",)
        print(pd.DataFrame(df.Sector.value_counts()).reset_index().loc[0:2])
        print("\n\nCompany by investment in Top Sector")
        pos=1
        # dataframe with only top sector
        df2=df[df.Sector==sector_position(df,pos)]
        print(df2.groupby(['name'])['raised_amount_usd'].sum().sort_values(ascending=False))
        print("\n\nCompany by investment in Second Sector")
        pos=2
        df2=df[df.Sector==sector_position(df,pos)]
        print(df2.groupby(['name'])['raised_amount_usd'].sum().sort_values(ascending=False))


# In[620]:


table_5_1(df_D1)


# In[621]:


table_5_1(df_D2)


# In[622]:


table_5_1(df_D3)


# # Plot 1

# In[586]:


plt.style.use("dark_background")
plt.figure(figsize=(25, 20))
funding_plt=sns.barplot(x=master_frame.loc[master_frame["funding_round_type"].isin(["venture","seed","angel","private_equity"]),"funding_round_type"],y=master_frame['raised_amount_usd'],estimator=np.median,palette="Blues_d")
# funding_plt.title("Average Funding Amount",fontsize=30)
funding_plt.set_title('Average Funding Amount',fontsize=70)
funding_plt.set_xlabel("Funding Type",fontsize=30)
funding_plt.set_ylabel("Average Funding Amount",fontsize=30)
plt.ticklabel_format(axis='y',  scilimits=None,style='plain', useOffset=None, useLocale=None, useMathText=None)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
# sns.set(font_scale=1)
# ax.ticklabel_format(useOffset=False)
plt.show()
plt.savefig('Analysis1.png')


# In[ ]:




df_plot1=master_frame.groupby("funding_round_type").aggregate({'raised_amount_usd':['sum','median']})
df_plot1.reset_index(inplace=True)



df_plot1[( 'raised_amount_usd','sum')]=(df_plot1[( 'raised_amount_usd','sum')]/master_frame['raised_amount_usd'].sum())*100
df_plot1[('raised_amount_usd','sum')]
df_plot1=df_plot1[df_plot1[('funding_round_type',       '')].isin(["venture","private_equity","angel","seed"])]


# In[453]:


df_plot1.columns


# In[486]:


plt.style.use('grayscale')
plt.style.use("ggplot")
plt.figure(figsize=(25, 20))
ax=df_plot1.plot.bar(x=('funding_round_type',       ''),y=[( 'raised_amount_usd',    'sum')])
ax.set_title('Average Funding Amount',fontsize=30)
ax.set_xlabel("Funding Type",fontsize=15)
ax.set_ylabel("Percentage of Share",fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)


# ## PLOT 2

# ### Top Countries by invested amount

# In[581]:


# plt.subplots(1,2,1)


plt.figure(figsize=(15, 15))
ax=top9.groupby("country_code")["raised_amount_usd"].sum().sort_values(ascending=True).plot.barh()
ax.set_title('Distribution of Investment by Countries',fontsize=40)
ax.set_xlabel("Total Invested Amount(in Million)",fontsize=20)
ax.set_ylabel("Countries",fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


# ### Total number of investment in each country

# In[582]:


# plt.subplots(1,2,2)
plt.figure(figsize=(15, 15))
ax2=top9.groupby("country_code").size().sort_values(ascending=True).plot.barh()
ax2.set_title('# of Investment by Countries',fontsize=40)
ax2.set_xlabel("# of Investment ",fontsize=20)
ax2.set_ylabel("Countries",fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)


# # Top 3 Countries in one dataframe 

# In[ ]:


top3=df_D1.append(df_D2).append(df_D3)

top3.columns

top3.groupby(["country_code","Sector"])['raised_amount_usd'].sum().sort_values(ascending=False)


# In[542]:


top3=pd.DataFrame(df_D1.groupby(["country_code","Sector"]).size().sort_values(ascending=False)).reset_index().loc[0:2].append(
pd.DataFrame(df_D2.groupby(["country_code","Sector"]).size().sort_values(ascending=False)).reset_index().loc[0:2]).append(
pd.DataFrame(df_D3.groupby(["country_code","Sector"]).size().sort_values(ascending=False)).reset_index().loc[0:2])
top3


# In[548]:


top3.columns


# In[626]:



plt.figure(figsize=(25, 20))
ax=top3.groupby(["country_code","Sector"])[0].sum().sort_values(ascending=True).plot.barh()
ax.set_title('Top 3 Sector of Top 3 invested Countries',fontsize=50)
ax.set_xlabel("# of Investments",fontsize=30)
ax.set_ylabel("Countries, Sectors",fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


# In[ ]:




