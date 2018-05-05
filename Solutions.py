
# coding: utf-8

# In[1]:


# ## Preprocessing

# In[530]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from sklearn.metrics import mutual_info_score
from sklearn.model_selection import train_test_split
sns.set()

# In[118]:

df = pd.read_excel('2010 Federal STEM Education Inventory Data Set.xls')


# In[967]:

df.shape


# In[120]:

from IPython.display import display
with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
    display(df.head(3))


# In[121]:

df.columns = df.iloc[0]
df.head(3)


# In[122]:

df = df.iloc[1:]


# In[123]:

df.columns


# In[124]:

# Create a list for df columns as shown in excel (here, multiple spanning of columns will be shown as colname + 0/1/2....)
lis = []
k = 0
for x, y in zip(df.columns.isnull(), df.columns):
    if not x:
        z = y
        lis.append(y)
        j = 0
        k = 0
    else:
        if j == 0:
            lis.pop()
            lis.append(z + str(k))
            k += 1
            lis.append(str(z) + str(k))
        else:
            k += 1
            lis.append(str(z) + str(k))
lis[:15]


# In[125]:

df.columns = lis


# In[126]:

df.head(3)


# ## Stage 1
# 

# #### 1) Calculate % growth of funding between year 2008 & 2009.

# In[127]:

df.columns[:10]


# In[128]:

# Some of the df['C1) Funding FY2008'] are = NaN. Assuming that the funding for those years was 0

df['C1) Funding FY2008'].fillna(0, inplace=True)
df['C2) Funding FY2009'].fillna(0, inplace=True)
df['C3) Funding FY2010'].fillna(0, inplace=True)


# In[129]:

def calculate_percent_increase(x):
    try:
        ans = (x['C3) Funding FY2010'] - x['C1) Funding FY2008']) / x['C1) Funding FY2008']
        return (ans * 100)
    except ZeroDivisionError:
        return (100)


def get_eliminate(df):
    eliminate = []
    for col in df.columns:
        if len(df[col].unique()) > 15:
            eliminate.append(col)
    return eliminate


# now, we can easily calculate mutual info score using a loop
def get_mutual_info_score(df2):
    mutual_info_score_with_target_variable = {}
    lis1 = []
    lis2 = []

    banned_cols = ['C1) Funding FY2008','C2) Funding FY2009','C3) Funding FY2010']
    for i, col in enumerate(df2.columns):
        if col in banned_cols:
            continue
        else:
            sys.stdout.write("\r")
            sys.stdout.write("Iteration %d of %d" % (i+1, len(df2.columns)))
            sys.stdout.flush()
            lis1.append(col)
            lis2.append(mutual_info_score(df2['Target Variable'], df2[col]))

    mutual_info_score_with_target_variable['Non-Funding Variable'] = lis1
    mutual_info_score_with_target_variable['Mutual Info Score'] = lis2
    return mutual_info_score_with_target_variable
