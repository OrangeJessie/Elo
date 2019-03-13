
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import warnings
pd.set_option('max_columns', 100)
pd.set_option('max_colwidth', 100)
warnings.filterwarnings('ignore')

# get_ipython().run_line_magic('matplotlib', 'inline')


# # train test

# In[7]:


train = pd.read_csv('data/train.csv')


# In[8]:


test = pd.read_csv('data/test.csv')


# In[9]:


test['first_active_month'] = test['first_active_month'].fillna('2017-09')


# **合并训练集测试集**

# In[10]:


train_y = train['target']
train = train.drop('target', axis=1)


# In[11]:


data = pd.concat([train, test], axis=0)


# 把训练集测试集的时间换算成月

# In[12]:


def time_to_month(x):
    year, month = x.split('-')
    time = int(year)*12 + int(month)
    return time


# In[13]:


data['first_active_month'] = data['first_active_month'].apply(time_to_month)
min_time = min(data['first_active_month'])
data['first_active_month'] -= min_time


# In[20]:




# In[78]:


category_features = ['feature_1', 'feature_2', 'feature_3']


# # historical trasactions

# In[3]:


historical = pd.read_csv('data/new_merchant_transactions.csv')


# ## 时间转换

# In[4]:


def purchase_day(x):
    big, small = x.split(' ')
    year, month, day = big.split('-')
    all_day = (int(year)*12+int(month)-24143)*30 + int(day)
    return all_day


# In[5]:


def purchase_second(x):
    big, small = x.split(' ')
    hour, minite, second = small.split(':')
    all_second = int(hour)*24*60 + int(minite)*60 + int(second)
    return all_second


# In[6]:


historical['purchase_day'] = historical['purchase_date'].apply(purchase_day)
historical['purchase_second'] = historical['purchase_date'].apply(purchase_second)


# In[7]:


historical = historical.drop('purchase_date', axis=1)


# ## 合并merchant特征

# In[8]:


mf = pd.read_csv('data/mf.csv')
mcf = pd.read_csv('data/mcf.csv')
sf = pd.read_csv('data/sf.csv')


# In[9]:


historical = pd.merge(historical, mf, on=['merchant_id'], how='left')
historical = pd.merge(historical, mcf, on=['merchant_category_id'], how='left')
historical = pd.merge(historical, sf, on=['subsector_id'], how='left')


# ## factorize

# In[160]:


sub_cate = ['city_id', 'authorized_flag', 'category_1', 'category_2', 'category_3', 'merchant_category_id', 'month_lag', 'state_id', 'subsector_id']


# In[184]:


sub_nume = ['installment', 'purchase_amount']


# In[161]:


# 处理分期付款的异常值
historical['installments'][historical['installments'] == 999] = -1


# In[163]:


for f in sub_cate:
    historical[f] = historical[f].map(dict(zip(historical[f].unique(), range(0, historical[f].nunique()))))


# In[183]:


historical.head()


# ## card_id相关特征

# In[271]:


card = historical[['card_id']]


# In[272]:


buy_num = pd.DataFrame(historical['card_id'].value_counts()).reset_index()
buy_num = buy_num.rename(columns={'index': 'card_id', 'card_id': 'card_times'})


# In[273]:


card = pd.merge(card, buy_num, on=['card_id'], how='left')


# In[ ]:


for i in sub_num2:
    t4 = merchant[['subsector_id', i]].groupby('subsector_id').mean().reset_index()
    t4 = t4.rename(columns={i: 'subsector_'+i})
    sf = pd.merge(sf, t4, on=['subsector_id'], how='left')


# # Merchant feature

# In[232]:


merchant = pd.read_csv('data/merchants.csv')


# In[233]:


merchant.head()


# In[234]:


merchant = merchant.fillna(-1)


# ## numerical特征处理

# In[235]:


sub_num2 = ['numerical_1', 'numerical_2', 'avg_sales_lag3', 'avg_purchases_lag3', 'active_months_lag3', 'avg_sales_lag6', 'avg_purchases_lag6', 'active_months_lag6', 'avg_sales_lag12', 'avg_purchases_lag12', 'active_months_lag12']


# ### mf合并与merchant_id相关的特征

# In[236]:


mf = merchant[['merchant_id']]


# In[237]:


for i in sub_num2:
    t1 = merchant[['merchant_id', i]].groupby('merchant_id').mean().reset_index()
    t1 = t1.rename(columns={i: 'merchant_'+i})
    mf = pd.merge(mf, t1, on=['merchant_id'], how='left')


# In[238]:


mgf = merchant[['merchant_id', 'merchant_group_id']]


# In[239]:


for i in sub_num2:
    t2 = merchant[['merchant_group_id', i]].groupby('merchant_group_id').mean().reset_index()
    t2 = t2.rename(columns={i: 'mgroup_'+i})
    mgf = pd.merge(mgf, t2, on=['merchant_group_id'], how='left')


# In[240]:


mf = pd.merge(mf, mgf, on=['merchant_id'], how='left')


# ### mcf合并与merchant_category_id相关的特征

# In[241]:


mcf = merchant[['merchant_category_id']]


# In[242]:


for i in sub_num2:
    t3 = merchant[['merchant_category_id', i]].groupby('merchant_category_id').mean().reset_index()
    t3 = t3.rename(columns={i: 'mcategory_'+i})
    mcf = pd.merge(mcf, t3, on=['merchant_category_id'], how='left')


# ### sf合并与subsector_id相关的特征

# In[243]:


sf = merchant[['subsector_id']]


# In[244]:


for i in sub_num2:
    t4 = merchant[['subsector_id', i]].groupby('subsector_id').mean().reset_index()
    t4 = t4.rename(columns={i: 'subsector_'+i})
    sf = pd.merge(sf, t4, on=['subsector_id'], how='left')


# ## category特征处理

# In[ ]:


sub_cate2 = ['category_1', 'most_recent_sales_range', 'most_recent_purchases_range', 'category_4', 'category_2']

