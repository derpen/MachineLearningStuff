# Laporan Proyek Machine Learning - Muhammad Rizqi Assabil

## Domain Proyek

Proyek kali ini adalah clustering data kartu kredit menggunakan algoritma K-Means. Adapun proyek ini sendiri dipilih karena penulis sedang ingin mempelajari kasus clustering.

Problem yang ingin diselesaikan adalah untuk mendeteksi fraud (pemalsuan/penipuan) dalam penggunaan kartu kredit. Teknik nya cukup mudah, yaitu dengan melakukan clustering pada data. Data dari hasil penipuan umumnya akan langsung terdeteksi sebagai outlier, dan otomatis terbuat cluster nya sendiri (In theory, at least). Mendeteksi fraud dengan teknik ini sudah sering digunakan sebelumnya.[1][2]

## Business Understanding

### Problem Statement
* Bagaimana cara kita mendeteksi fraud pada penggunaan kartu kredit?

### Goals
* Menggunakan algoritma clustering, pada kasus ini K-Means, untuk mendeteksinya

### Why K-Means (Solution Statement)?
* Karena ini adalah salah satu algoritma paling umum untuk melakukan clustering. Referensi sudah banyak, sehingga hasil dari proyek ini dapat direplikasi secara konsisten, dan mudah untuk di-improve

## Data Understanding

Data didapatkan dari kaggle, [CC General](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata), yang berupa file csv dengan 17 column yang bisa digunakan. Antara lain adalah berapa banyak uang lagi di akun mereka, sampai pengunaan total dari sebuah akun.

* CUSTID : ID dari pemilik (Categorical)
* BALANCE : Jumlah uang tersisa di akun
* BALANCEFREQUENCY : Seberapa sering jumlah uang nya berubah. Value dari 0-1, 0 berarti jarang berubah, 1 sering
* PURCHASES : Jumlah belanja pada akun
* ONEOFFPURCHASES : Jumlah belanja terbanyak pada satu kali beli
* INSTALLMENTSPURCHASES : Jumlah belanja seluruh sampai sekarang
* CASHADVANCE : Cash yang disetor oleh user
* PURCHASESFREQUENCY : Seberapa sering membeli. Value dari 0-1, 0 berarti jarang belanja, 1 sering
* ONEOFFPURCHASESFREQUENCY : Seberapa sering berbelanja dalam sekali beli. Value 0-1. 0 Jarang, 1 Sering
* PURCHASESINSTALLMENTSFREQUENCY : Seberapa sering membeli dalam keseluruhan. Value 0-1. 0 Jarang, 1 Sering
* CASHADVANCEFREQUENCY : Seberapa sering menyetor cash
* CASHADVANCETRX : Berapa sering transaksi dengan setoran cash
* PURCHASESTRX : Jumlah transaksi belanja
* CREDITLIMIT : Batas kartu kredit per user
* PAYMENTS : Total bayar per user
* MINIMUM_PAYMENTS : Jumlah terkecil bayaran oleh user
* PRCFULLPAYMENT : Persentasi bayar sepenuhnya oleh user
* TENURE : Tenure per user

Pertama, kita menggunakan `pandas` untuk mengload data csv menjadi sebuah dataframe pandas. Pandas sudah kita alias menjadi pd
```python
CreditCards = pd.read_csv("cc.csv")
```

Kita membuang column `CUST_ID` yang berisi data yang kita tidak perlu, yaitu ID dari Customer.
```python
CreditCards.drop(labels="CUST_ID", axis=1, inplace=True)
```

Selanjutnya kita bisa menggunakan `describe` untuk melihat summary dari dataset, sekaligus column apa saja disana. Dan gunakan `info` untuk mengecek tipe data dari tiap column

![5](https://user-images.githubusercontent.com/76782988/188809176-29c350f2-237b-4dc6-bf45-b8358c2dbbf3.png)

![6](https://user-images.githubusercontent.com/76782988/188809274-623818d1-5bbc-4c01-9d1b-d792b4297d50.png)


Kita cek data yang tidak memiliki nilai

```python
CreditCards.isna().sum()
```
![7](https://user-images.githubusercontent.com/76782988/188809335-49be02f2-b997-45f9-80ef-4c32534e6fa3.png)


Tidak banyak yang hilang. Untuk `CREDIT_LIMIT` bisa kita buang saja data yang tidak lengkap, karena hanya ada 1.

Untuk `MINIMUM_PAYMENT`, bisa kita ganti dengan Median atau Mean. Bisa juga kita buang, tetapi 300 data cukup berharga, jadi kali ini, akan kita ganti dengan Median.

```python
CreditCards.dropna(subset=['CREDIT_LIMIT'], inplace=True)
CreditCards['MINIMUM_PAYMENTS'].fillna(CreditCards['MINIMUM_PAYMENTS'].median(), inplace=True)
```

Data sudah bisa kita visualisasi, mari kita lihat.

![Data](https://user-images.githubusercontent.com/76782988/188809401-1b450975-6740-48a9-a94a-cb196c4b6c78.png)


Data terlalu skewed (mencong), ini berarti banyak outlier pada data. Kita bisa melakukan beberapa hal untuk menangani ini.

Jika kita ingin mendeteksi outlier:
* Biarkan saja outlier nya

Jika kita ingin membuang nya:
* Bisa langsung dihapus saja. Pada kasus kita, jumlah outlier sangat banyak, sehingga akan mengurangi total data nanti
* Sama seperti `MINIMUM_PAYMENT`, bisa kita ganti dengan median atau mean
* Atau kita atur sebuah batas yang tidak bisa dilewati. Contohnya kita atur batas "6". Maka semua value diatas 6 akan diubah menjadi 6

Kali ini, kita akan membiarkan saja outlier datanya

## Modeling

Sebelum memasukkan data kedalam model K-Means, kita standarisasi dan normalisasi data terlebih dahulu. Ukuran data juga akan kita reduksi menjadi 2 dimensi menggunakan Principal Component Analysis. Semua hal ini dilakukan untuk mempercepat, mengoptimisasi, dan mempermudah modeling nantinya.

```python
X = CreditCards

scale = StandardScaler()
X = scale.fit_transform(X)

X = normalize(X)

# we reduce dimension to 2 with PCA to make things easier later
pca = PCA(2)
X = pca.fit_transform(X)

X.shape
```
Pada kasus K-Means, terdapat beberapa cluster yang bisa tentukan. Tetapi umumnya hanya ada 1 atau 2 cluster yang optimal untuk suatu dataset. Untuk mencari value cluster ini, kita menjalankan K-Means berkali-kali, sambil merubah jumlah cluster nya. Kita lalu memilih cluster mana yang memiliki perubahan inertia yang dari signifikan, ke yang paling tidak signifikan. Ini disebut dengan elbow. Inertia sendiri secara singkat nya adalah sebagus apa K-Means melakukan clustering pada data tersebut dengan jumlah cluster yang diminta

```python
n_clusters=15 # Kita coba sampai 15 cluster
cost=[]
for i in range(1,n_clusters):
    kmean = KMeans(i).fit(X)
    cost.append(kmean.inertia_)  
  
plt.plot(cost, 'bx-')
```
![Elbow](https://user-images.githubusercontent.com/76782988/188809449-b8030a37-a176-4b11-bb0f-acdb408f4950.png)


Bisa dilihat bahwa sekitar cluster 2-4 perubahnnya cukup signifikan. Cluster optimal berada di 2 sampai 4. Untuk mencari mana yang optimal, bisa kita gunakan `silhouette_score`. Penulis sendiri masih kurang mengerti matematikanya, tetapi yang penting adalah semakin besar score nya, semakin baik

```python
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
```

![Score](https://user-images.githubusercontent.com/76782988/188809488-76664015-b1fd-49ee-87f7-f3944b6da866.png)


Cluster 3 memiliki skor tertinggi. Kita akan memilih 3

```python
kmean = KMeans(3).fit(X)
labels = kmean.labels_
```

Kita gabungkan label hasil clustering kedalam dataframe awal

```python
clusters=pd.concat([CreditCards, pd.DataFrame({'cluster':labels})], axis=1)
```
Lalu kita bisa visualisasikan data pada tiap cluster

```python
for c in clusters:
    grid = sns.FacetGrid(clusters, col='cluster')
    grid.map(plt.hist, c)
```

![image](https://user-images.githubusercontent.com/76782988/188813259-567c9368-01ff-4d3b-9d11-1c10f7703eca.png)
![image](https://user-images.githubusercontent.com/76782988/188813582-bfdb3868-2970-4df4-93f0-869eabc335b6.png)
![image](https://user-images.githubusercontent.com/76782988/188813343-af879995-d4b8-4e19-bc72-af15e9f9f94e.png)
![image](https://user-images.githubusercontent.com/76782988/188813384-8e05ea7f-b213-46b7-abb0-56ea28a6621b.png)
![image](https://user-images.githubusercontent.com/76782988/188813411-29ac0ca2-bb34-46dc-8589-8b482c4bd768.png)
![image](https://user-images.githubusercontent.com/76782988/188813434-47060307-b935-4d10-a06c-3196d0c2de1a.png)


Cluster ke-2 memiliki jumlah paling sedikit. Bisa diasumsikan bahwa cluster 2 adalah orang-orang yang melakukan fraud, atau setidaknya orang yang pola pengunaan kartu kreditnya aneh dibandingkan yang lain. Goal kita tercapai (For now, at least).

![Visualization](https://user-images.githubusercontent.com/76782988/188809571-b8a37342-cdd8-4285-84a7-1c73944286fc.png)

## Evaluation

Evaluasi clustering umumnya menggunakan silhouette score. Ini dikarenakan clustering tidak mempunyai true value yang bisa digunakan untuk mengecek apakah prediksi kita benar atau tidak. Ini menyebabkan akurasi, recall, dan semacamnya tidak bisa digunakan. 

Silhouette score sendiri dihitung dengan cara

`(b - a) / max(a, b)`

Dimana a adalah jarak rata rata antara satu cluster, dan b adalah jarak dari sebuah sample ke sebuah cluster tetangga. 

Hasil dari score ini adalah sebuah nilai diantara -1 dan 1, dimana semakin dekat ke 1, maka semakin bagus.

Pada model, ini, kita mendapatkan hasil sebagai berikut

![Score2](https://user-images.githubusercontent.com/76782988/188809624-2c081c07-edc2-488c-8b63-264713bbbdfc.png)

Sehingga bisa dikatakan, model kita masih dapat diperbaiki, dan kita juga dapat melakukan teknik teknik lain pada data untuk mengurus outlier. Tetapi pada kali ini, penulis cukupkan


## Reference

[1]Deng, Qingshan, and Guoping Mei. "Combining self-organizing map and k-means clustering for detecting fraudulent financial statements." 2009 IEEE International Conference on Granular Computing. IEEE, 2009.

[2]Monamo, Patrick, Vukosi Marivate, and Bheki Twala. "Unsupervised learning for robust Bitcoin fraud detection." 2016 Information Security for South Africa (ISSA). IEEE, 2016.

