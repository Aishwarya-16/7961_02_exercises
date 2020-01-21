#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np


# In[47]:


df = pd.read_csv('imdb.csv',escapechar='\\')
df1 = pd.read_csv('movie_metadata.csv')
df2 = pd.read_csv('diamonds.csv')


# In[48]:


#3 :

df2['z']=pd.to_numeric(df2['z'],errors='coerce')
vol=[]
for i in df2.itertuples():
    if i[5] > 60 :
        vol.append(float(i[8]) * float(i[9]) * float(i[10]))
    else :
        vol.append(8)
df2['Volume']=vol

df2


# In[49]:


df2['Bins']=pd.qcut(df2.Volume, q=16)
cross = pd.crosstab(df2['Bins'],df2['cut']).apply(lambda r: r/r.sum(),axis=1)

cross


# In[ ]:





# In[ ]:



    
    


# In[50]:


#6 :
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[51]:


sns.barplot(x=df['nrOfGenre'], y=df['nrOfUserReviews'], palette="deep")



# In[52]:


sns.jointplot(x=df['nrOfWins'], y=df['nrOfNominations'],kind = "kde",xlim={0,20},ylim={0,20})
#g = sns.jointplot(x, x, kind="kde", height=7, space=0)


# In[53]:


plt.figure(figsize=(20,8))
sns.scatterplot(x=df['imdbRating'], y=df['ratingCount'], palette="deep")


# In[54]:


plt.figure(figsize=(100,8))

sns.catplot(x="year",y="type",kind='violin',data=df)


# In[55]:


df5=df.corr()
sns.heatmap(df5, linewidths=1)


# In[56]:


plt.figure(figsize=(100,50))
sns.boxplot(x="language",y="imdb_score",data=df1)


# In[57]:


sns.jointplot("budget", "aspect_ratio", data=df1, kind="reg", color="m", height=7)


# In[58]:


sns.lmplot(x="gross", y="budget", hue="facenumber_in_poster",truncate=True, height=5, data=df1)


# In[59]:


plt.figure(figsize=(10,10))
sns.swarmplot(x="title_year", y="language",data=df1)


# In[60]:


#2 :

list=[]
for i in df.itertuples():
    list.append(len(i[3])-7)
df['Lenghth_of_title']=list   


# In[61]:


ae= df['Lenghth_of_title'].quantile([.25, .5, .75, 1])
ae


# In[62]:


as25=df[df['Lenghth_of_title']<ae[.25]]['year'].reset_index()
as25['num_videos_less_than25Percentile']=1
as25=as25.groupby('year')['num_videos_less_than25Percentile'].sum().reset_index()

as50=df[df['Lenghth_of_title']<ae[.50]]['year'].reset_index()
as50['num_videos_25_50Percentile']=1
as50=as50.groupby('year')['num_videos_25_50Percentile'].sum().reset_index()

as75=df[df['Lenghth_of_title']<ae[.75]]['year'].reset_index()
as75['num_videos_50_75Percentile']=1
as75=as75.groupby('year')['num_videos_50_75Percentile'].sum().reset_index()

as100=df[df['Lenghth_of_title']<ae[1.00]]['year'].reset_index()
as100['num_videos_greaterthan75Precentile']=1
as100=as100.groupby('year')['num_videos_greaterthan75Precentile'].sum().reset_index()


# In[63]:


min=df.groupby('year')['Lenghth_of_title'].min().reset_index()
max=df.groupby('year')['Lenghth_of_title'].max().reset_index()


# In[64]:


quan=pd.DataFrame()
quan['year']=df['year'].unique()
quan=quan.sort_values(by ='year' )
quan['Max_Length']=max['Lenghth_of_title']
quan['Min_Length']=min['Lenghth_of_title']
quan=pd.merge(quan,as25,how='outer',on='year')
quan=pd.merge(quan,as50,how='outer',on='year')
quan=pd.merge(quan,as75,how='outer',on='year')
quan=pd.merge(quan,as100,how='outer',on='year')

quan


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:







#!/usr/bin/env python
# coding: utf-8

# In[55]:


#1 :

import pandas as pd
import numpy as np


# In[56]:


df = pd.read_csv('imdb.csv',escapechar='\\')


# In[57]:


columns = list(df)
l=(len(columns))
op=[]
lis=[]
for i in df.itertuples():
    for j in range (16,l):
        if i[j+1] == 1:
            op.append(columns[j])
    lis.append(op)
    op=[]
df['GenreCombinations']=lis
df


# In[18]:





# In[58]:


comb=df.groupby(['year','type'])['GenreCombinations'].apply(pd.Series.tolist).tolist()

comb


# In[ ]:





# In[59]:


ae=[]
i=0
for a in comb:
    for b in a:
        if b not in ae:
            ae.append(b)
    
    comb[i]=ae
    i=i+1
    ae=[]
        


# In[60]:


ea=[]
l1=[]
i=0
for a in comb:
    for b in a:
        if b!=[]:
            l1.append(b)
    ea.append(l1)
    l1=[]
comb=ea
        


# In[ ]:





# In[ ]:





# In[62]:


max=df.groupby(['year','type'])['imdbRating'].max().reset_index()
min=df.groupby(['year','type'])['imdbRating'].min().reset_index()
sum=df.groupby(['year','type'])['duration'].sum().reset_index()
mean=df.groupby(['year','type'])['imdbRating'].mean().reset_index()


# In[63]:


df11=pd.DataFrame()
df11['YEAR']=min['year']
df11['TYPE']=min['type']
df11['GENRE']=comb
df11['MAXIMUM_RATING']=max['imdbRating']
df11['MINIMUM_RATING']=min['imdbRating']
df11['TOTAL_TIME']=sum['duration']
df11['AVERAGE_RATING']=mean['imdbRating']
df11


# In[ ]:





# In[64]:


#5 :

df['Deciles'] = pd.qcut(df['duration'], 10, labels=False)
gn=df.groupby('Deciles').sum().reset_index()
gn.to_csv('deciles.csv')


# In[65]:


col = list(gn)
l1=(len(col))
gl=[]
for i in gn.itertuples():
    li=[]
    o=[]
    r=np.arange(11,l1)
    for j in range (11,l1):
        o.append(i[j+1])
    a=np.argsort(o)
    li.append(col[a[l1-11-1]+11])
    li.append(col[a[l1-2-11]+11])
    li.append(col[a[l1-3-11]+11])
    gl.append(li)


# In[66]:


wins=df.groupby('Deciles')['nrOfWins'].sum().reset_index()
nominations=df.groupby('Deciles')['nrOfNominations'].sum().reset_index()
df['Values']=1
counts=df.groupby('Deciles')['Values'].sum().reset_index()

counts


# In[67]:


new=pd.DataFrame()
new['DECILE']=nominations['Deciles']
new['NOMINATIONS']=nominations['nrOfNominations']
new['WINS']=wins['nrOfWins']
new['COUNT']=counts['Values']
new['TOP3_GENRES']=gl
new


# In[ ]:




