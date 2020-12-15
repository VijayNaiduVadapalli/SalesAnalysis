#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as p
import os

#Task 1 :Merging 12 months sales data into a single CSV file.
# In[2]:


df=pd.read_csv("D:\Datasciencetasks\Pandas-Data-Science-Tasks-master\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data/Sales_April_2019.csv")

files=[file for file in os.listdir('D:\Datasciencetasks\Pandas-Data-Science-Tasks-master\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data')] 

all_months_data=pd.DataFrame()

for file in files:
    df=pd.read_csv("D:\Datasciencetasks\Pandas-Data-Science-Tasks-master\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,df])

all_months_data.to_csv("all_data.csv",index=False)
    


# In[13]:


all_data=pd.read_csv("all_data.csv")
all_data.head()

##augument data ##Cleaning up the data and dropping NAN
# In[14]:


nan_df=all_data[all_data.isna().any(axis=1)]
nan_df.head()

all_data=all_data.dropna(how='all')
#all_data=all_data.drop()


# In[15]:


all_data.head()

# Delete the rows that are duplicated in the dataframe
# In[16]:


all_data=all_data[all_data['Order Date'].str[0:2] !='Or']
all_data.head()


# In[131]:


##Converting columns to the correct type from str to int 


# In[20]:


all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered']) #making int 
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])#make float

###Task 2:Add Month Column
# In[19]:


all_data['Month']=all_data['Order Date'].str[0:1]
all_data['Month']=all_data['Month'].astype('int32')
all_data.head()


# In[ ]:


#Adding a city column


# In[21]:


#all_data['Column']=all_data['Purchase Address'].apply(lambda x:x.split(',')[1])
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City']=all_data['Purchase Address'].apply(lambda x:f"{get_city(x)}  ({get_state(x)})")

all_data.head()


# In[ ]:


#Adding sales column


# In[22]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# In[ ]:


###What was the best month for sales ? how much was earned that month?


# In[23]:


results=all_data.groupby('Month').sum()


# In[24]:


import matplotlib.pyplot as plt
months=range(1,5)
plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# In[ ]:


##which city had the highest number of sales?


# In[25]:


results=all_data.groupby('City').sum()
results


# In[26]:


import matplotlib.pyplot as plt
#cities=all_data['City'].unique()
cities=[city for city,df in all_data.groupby('City')]

plt.bar(cities,results['Sales'])
plt.xticks(cities,rotation='vertical',size=10)
plt.ylabel('sales in USD ($)')
plt.xlabel('cityNames')
plt.show()


# In[ ]:


###What time should we display advertisments to maximize likelihood of customers buying product?


# In[28]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])


# In[29]:


all_data['Hour']=all_data['Order Date'].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute
all_data.head()


# In[32]:


hours=[hour for hour ,df in all_data.groupby('Hour')]

plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()


# In[ ]:


## What products are most often sold together?


# In[33]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))

df=df[['Order ID','Grouped']].drop_duplicates()
df.head()


# In[35]:


from itertools import combinations
from collections import Counter

count=Counter()

for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))
    
for key,value in count.most_common(10):
    print(key,value)
    
    


# In[ ]:


##What product sold the most ? Why do you think it sold the most?


# In[36]:


all_data.head()


# In[46]:


product_group=all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']

products=[product for product,df in product_group]

plt.bar(products,quantity_ordered)

plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products,rotation='vertical',size=8)
plt.show()


# In[47]:


prices=all_data.groupby('Product').mean()['Price Each']

fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products , quantity_ordered,color='g')
ax2.plot(products ,prices,'b-')

ax2.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color='b')
ax2.set_ylabel('Price($)',color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)


# In[ ]:



