# -*- coding: utf-8 -*-
"""credit card.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aXw-86PACfGScJVsYoLIRzV2wtWqwKQ6

# Importing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# For collab
from google.colab import drive
drive.mount('/content/drive')

# CreditCards = pd.read_csv("cc.csv")
CreditCards = pd.read_csv("/content/drive/MyDrive/cc.csv") 
CreditCards

CreditCards.drop(labels="CUST_ID", axis=1, inplace=True) # just remove lmao

CreditCards.describe().T

CreditCards.info()

CreditCards.isna().sum()

CreditCards.dropna(subset=['CREDIT_LIMIT'], inplace=True) # Karena cuma 1 yang na, buang aja

CreditCards['MINIMUM_PAYMENTS'].fillna(CreditCards['MINIMUM_PAYMENTS'].median(), inplace=True) # isi dengan median, can try with mean later

CreditCards.isna().sum()

col = list(CreditCards.columns)
CreditCards.hist(bins=20, figsize=(20, 15), layout=(5, 4)) # lets see the data

"""# Data terlalu skewed, ini berarti terdapat outlier. Dan pada kasus ini, jumlahnya cukup banyak

# Mengurus Outlier

# Jika tugas kita mendeteksi outlier
* outliernya ga usah diapa apain

# Kalau mau ngurus outlier, 3 cara
* Just delete it. Metode ini buruk kalau outlier nya terlalu banyak, karena akan membuang terlalu banyak data
* Ganti dengan median/mean/apalah. Simple dan efektif
* Buat Batas. Ex: nilai berapapun yang diatas 5.6 akan dirubah jadi 5.6. Butuh effort ekstra, tetapi akan membantu model nantinya

# Today, we will ignore outliers and see what happens
"""

# Process the data
# X = np.asarray(CreditCards)

# Standardize the data, then normalize
X = CreditCards

scale = StandardScaler()
X = scale.fit_transform(X)

X = normalize(X)

# we reduce dimension to 2 with PCA to make things easier later
pca = PCA(2)
X = pca.fit_transform(X)

X.shape

# K means for clustering
# this will take quite some time

n_clusters=15
cost=[]
for i in range(1,n_clusters):
    kmean = KMeans(i).fit(X)
    cost.append(kmean.inertia_)  
  
plt.plot(cost, 'bx-')

"""# 3 Cluster sepertinya paling optimal
## Bisa di cek menggunakan silhouette_score
"""

s_scores = []

for i in range(2,13):
  s_scores.append(
      silhouette_score(X, KMeans(n_clusters = i).fit_predict(X))
  )

label = [i for i in range(2,13)]
plt.bar(label, s_scores)
plt.xlabel('le cluster')
plt.ylabel('le score')
plt.show()

"""# We go with 3

"""

kmean = KMeans(3).fit(X)
labels = kmean.labels_

# Add labels to original dataset
clusters=pd.concat([CreditCards, pd.DataFrame({'cluster':labels})], axis=1)
clusters.head().T

# See what each label means
for c in clusters:
    grid = sns.FacetGrid(clusters, col='cluster')
    grid.map(plt.hist, c)

"""# Cluster ke 2 memiliki jumlah paling sedikit, bisa diasumsikan bahwa cluster 2 adalah outlier"""

#Visualization

pca_result = pd.DataFrame(X)
pca_result.columns = ['D1', 'D2'] # add header, first pca dimension, and 2nd dimension

pca_result['Labels'] = labels # add cluster label as columns

grouped = pca_result.groupby("Labels") # group the labels

fig, ax = plt.subplots()

colors = { 0: 'red',
           1: 'blue',
           2: 'green'
        }

legend = { 0: "First cluster",
           1: "Second cluster",
           2: "Third cluster"
        }

for cluster, value in grouped:
    ax.scatter(value.D1, value.D2, 
               c = colors[cluster], 
               label = legend[cluster])

ax.legend()

plt.show()

"""# Untuk Metric, bisa gunakan silhouette_score"""

print(silhouette_score(X, labels))