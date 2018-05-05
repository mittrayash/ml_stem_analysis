
### PLEASE NOTE: This is NOT  the complete assignment. Find the complete assignment in the ipynb file with the same name.
### This file has been converted from the ipynb file for the convenience of importing it into the testing module py file.




# ## Preprocessing

# In[23]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from sklearn.metrics import mutual_info_score
from sklearn.model_selection import train_test_split
sns.set()



# In[24]:

def read_file():
    df = pd.read_excel('2010 Federal STEM Education Inventory Data Set.xls')
    return df

df = read_file()


# In[25]:

df.shape


# In[26]:

from IPython.display import display
with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
    display(df.head(3))


# In[27]:

df.columns = df.iloc[0]
df.head(3)


# In[28]:

df = df.iloc[1:]


# In[29]:

df.columns


# In[30]:

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



# In[31]:

df.columns = lis


# In[32]:

df.head(3)


# ## Stage 1
# 

# #### 1) Calculate % growth of funding between year 2008 & 2009.

# In[33]:

df.columns[:10]


# In[34]:

# Some of the df['C1) Funding FY2008'] are = NaN. Assuming that the funding for those years was 0

df['C1) Funding FY2008'].fillna(0, inplace=True)
df['C2) Funding FY2009'].fillna(0, inplace=True)
df['C3) Funding FY2010'].fillna(0, inplace=True)


# In[35]:

def calculate_percent_increase(x):
    try:
        ans = (x['C3) Funding FY2010'] - x['C1) Funding FY2008']) / x['C1) Funding FY2008']
        return (ans * 100)
    except ZeroDivisionError:
        return (100)


# In[36]:


df["% Increase"] = df.apply(lambda x: calculate_percent_increase(x), axis=1)
df


# #### 2) If funding is positive, tag it as 1, if funding is negative tag it as 0. This is the target variable.

# In[37]:

df['Target Variable'] = df['% Increase'].apply(lambda x: 1 if x >= 0 else 0)


# In[44]:

df.head(3)


# ## Stage 2

# #### 1) Create graphs of univariate distribution of all non funding variables and share on a jupyter notebook. Just FYI - Funding FY2008, FY2009, FY2010 are the "funding variables"

# In[38]:

def get_eliminate(df):
    eliminate = []
    for col in df.columns:
        if len(df[col].unique()) > 15:
            eliminate.append(col)
    return eliminate

eliminate = get_eliminate(df)


# In[39]:

print(eliminate)


# #####  Creating groups of columns as in the excel spreadsheet

# In[40]:



lis2 = [x for x in lis if ')' not in x]

# Removing columns where univariate distribution is basically 1 for each element due to unique or a lot of elements:
for x in ['Investment Name', 'Agency', 'Subagency']:
    try:
        lis2.remove(x)
    except ValueError:
        
        continue
for x in eliminate:
    try:
        lis.remove(x)
    except ValueError:
        continue
lis 


# In[41]:


def get_final_groups_as_excel_file(lis):
    grp = []
    group = []
    for j in range(65, 65+25):
        for col in lis:
            if col.startswith(chr(j)) and ')' not in col:
                grp.append(col)
            else:
                pass
        if len(grp) > 0:
            group.append(grp)
        grp = []


    for j in range(65, 65+25):
        for col in lis:
            if col.startswith(chr(j) + ')'):
                if chr(j) == "C":
                    break
                grp.append(col)
            elif col.startswith(chr(j)+')'):
                grp.append(col)
            else:
                pass
            
        if len(grp) > 0:
            group.append(grp)
        grp = []


    for j in range(65, 65+25):
        for k in range(12):
            for col in lis:
                if col.startswith(chr(j) + str(k) + ')'):
                    if chr(j) == "C":
                        break
                    grp.append(col)
                else:

                    #grp =[]
                    pass
            if len(grp) > 0:
                group.append(grp)
            grp = []
    return group
group = get_final_groups_as_excel_file(lis)


# In[42]:

len(group)


# In[43]:

group


# In[1046]:

def plot_graphs(group, df):
    dic = {}
    for counter, grp in enumerate(group[:-1]):
        i = 0
        lis1 = []
        lis2= []

        try:
            temp = int(grp[0][-1])
            heading = grp[0][:-1]
        except ValueError:
            heading = grp[0]
            pass
            # print(grp[0])
        for elem in (grp):


            df_temp = (pd.DataFrame(df[elem].value_counts()))

            df_temp.columns = [df_temp.columns[0][:-2]]

            for j, var in enumerate(df_temp):
                try:
                    varr = df_temp.index[j]
                    lis1.append(varr)
                    lis2.append(df_temp.values[0][j])
                except IndexError:
                    continue


            i += 1
        dic['Field'] = (lis1)
        dic['Value'] = lis2
        temp_df = pd.DataFrame(dic)
        sys.stdout.write("\r")
        sys.stdout.write("Completed %d of %d" % (counter+1, len(group)))
        sys.stdout.flush()
        plt.figure()

        temp_df['Field'] = temp_df['Field'].apply(lambda x: x.split(' ')[0] if type(x) == str else x)

        temp_df.plot(x=temp_df['Field'], kind='bar')
        plt.title(heading + " Univariate Distribution")
        plt.xlabel(grp[0][:-1])
        plt.ylabel('count')
        try:
            plt.tight_layout()
        except ValueError:
            pass
# plot_graphs(group, df)


# ##### 2) Calculate mutual_info_score of target variable created in stage 1 & ALL non funding variables and share on a jupyter notebook.

# In[45]:

df.head(3)


# In[46]:

# Since there are many NaNs in the df, it won't work if I simply try to find the mutual info score.
# However, since I am dealing with string data in every column which contains NaN, so I can change all the NaNs to a 
# constant value, say "None" for instance. This will help in completing this task.

df2 = df.fillna(value='None')

# Also, let us remove the % increase column which was not present in the dataset originally

df2 = df2.drop('% Increase', axis=1)

# Also, converting all int values to str for compatibility

df2 = df2.astype(str)


# In[47]:

df2.head(3)


# In[48]:

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
    
mutual_info_score_with_target_variable = get_mutual_info_score(df2)


# In[49]:

mutual_info_score_with_target_variable = pd.DataFrame(mutual_info_score_with_target_variable)
mutual_info_score_with_target_variable.head(3)


# ## Stage 3

# ##### 1) Divide data into train & test samples. (70-30 split)

# In[50]:

X = df
X.columns


# In[51]:
def get_unique_count(X):
    l1 = []
    l2 = []
    collect = {}
    for col in X.columns:
        l1.append(col)
        l2.append(len(X[col].unique()))

    collect['Column Name'] = l1
    collect['Unique Count'] = l2
    count_df = pd.DataFrame(collect)
    return count_df

count_df = get_unique_count(X)


# In[52]:

for row in count_df.iterrows():
    if row[1]['Unique Count'] > 13:
        if row[1]['Column Name'] not in ['B) Year Established', 'C1) Funding FY2008', 'C2) Funding FY2009', 'C3) Funding FY2010']:
            X.drop([row[1]['Column Name']], axis=1, inplace=True)
    else:
        pass
    
X


# In[53]:

X = X[pd.notnull(X['B) Year Established'])]


# In[54]:

y = X['Target Variable']
X = X[X.columns[:-2]]
X.columns


### PLEASE NOTE: This is NOT  the complete assignment. Find the complete assignment in the ipynb file with the same name.
### This file has been converted from the ipynb file for the convenience of importing it into the testing module py file.
