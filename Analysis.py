import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

path = r'C:\Users\yingk\Desktop\Douban_Top250\douban_top_250.csv'
data = pd.read_csv(path,encoding='utf-8-sig')

#Preprocessing
#extract Chinese title
data['Chinese_title'] = data['title'].apply(lambda title:title.split()[0])
data.drop(['title'],axis=1,inplace=True)

#re.sub() - Use "" to repleace characters which are not digit
data['movie_length'] = data['length'].apply(lambda length:re.sub("\D","",length))
data.drop(['length'], axis=1, inplace=True)

#extract main country_region when there are multiple
data['main_country_region'] = data['country_region'].apply(lambda cr:cr.split()[0])
data.drop(['country_region'],axis=1,inplace=True)

#extract main language
data['main_language'] = data['language'].apply(lambda lan:lan.split()[0])
data.drop(['language'],axis=1,inplace=True)

data.to_csv(r'C:\Users\yingk\Desktop\Douban_Top250\cleaned_data.csv',encoding='utf-8-sig')

#Correlation
pd.set_option('display.max_columns', None)
data.columns
metrics = data.drop(['link','director','Chinese_title','main_country_region','main_language'],axis=1)
metrics.columns
metrics.eval('total_rating_scores = avg_rating*num_of_ratings', inplace=True)
metrics['years to 2019'] = metrics['year'].apply(lambda y:2019-y)
metrics.drop(['year'],axis=1,inplace=True)
corr = metrics.corr()
plt.figure(figsize=(6,5), dpi=100)
sns.heatmap(corr,cmap='coolwarm',linewidths=0.5)
corr.head(1)
#total_rating_scores t-test
x = list(metrics['rank'])
y = list(metrics['total_rating_scores'])
r,p = stats.pearsonr(x,y)
print(r)
print(p)

#num_comment
corr.iloc[5:6,:]
#num_reviews
corr.iloc[6:7,:]

#years to 2019 into bins check num of comment/reviews
plt.figure(figsize=(20,5), dpi=100)
sns.countplot(x='years to 2019', data=metrics)    
comment_reviews = metrics.loc[:,['num_comment','num_reviews']]
def bin_years(value):
    for i in range(10,91,10):
        if value<i:
            return f'{i-9}-{i}'
comment_reviews['years_bin'] = metrics['years to 2019'].apply(bin_years)
bins = [f'{i-9}-{i}' for i in range(10,91,10)]
plt.figure(figsize=(12,5), dpi=100)
sns.boxplot(x='years_bin', y='num_comment', data=comment_reviews, order=bins)
plt.figure(figsize=(12,5), dpi=100)
sns.boxplot(x='years_bin', y='num_reviews', data=comment_reviews, order=bins)

