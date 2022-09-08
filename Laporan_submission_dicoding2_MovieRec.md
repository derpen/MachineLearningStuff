# Laporan Proyek Machine Learning - Muhammad Rizqi Assabil

## Project Overview

Proyek ini adalah pembuatan sebuah sistem rekomendasi film. Mengapa memilih rekomendasi film ? Dikarenakan dataset yang saya temukan tidak terlalu rumit, sehingga saya rasa pengerjaannya tidak akan memakan waktu lama.

Adapun tujuan dari pembuatan ini adalah untuk memberikan user sebuah rekomendasi film yang mungkin akan ia suka. Ini berguna dalam kasus dimana kita adalah pihak yang menayangkan film tersebut. Dengan memberikan rekomendasi film serupa, user akan kembali lagi ke platform penanyangan film tersebut, sehingga meningkatkan keuntungan untuk perusahaan.

>Referensi here

## Business Understanding

### Problem Statement
* Sebagai perusahaan yang bergerak di bidang penayangan media, bagaimana kita bisa memastikan bahwa user akan kembali menggunakan platform kita?

### Goals
* Merekomendasikan media hiburan yang serupa dengan apa yang user tersebut telah tonton.

### Solution Approach
* Kita akan menggunakan content-based recommendation system. Kita juga bisa menggunakan demographic based recommendation, tetapi itu sangat amat terlalu simple, dan saya rasa bukan sebuah tantangan

## Data Understanding

Data kita dapatkan dari kaggle, bernama [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset). Dataset akan kita download menggunakan API kaggle, langsung ke google colab

*Note: cara ini membutuhkan token yang diberikan oleh kaggle ke masing-masing user. Token bisa didapatkan dari page user anda*

![image](https://user-images.githubusercontent.com/76782988/189083707-5d140e24-736b-44c5-86cd-900faaaab2c3.png)

![image](https://user-images.githubusercontent.com/76782988/189083517-1a6a8d66-9877-46df-b158-d244411ca2fb.png)

Kita unzip data nya, ternyata terdapat 7 file csv. Pada kasus ini, kita hanya membutuhkan `movies_metadata.csv`

![image](https://user-images.githubusercontent.com/76782988/189084110-ba1a2036-31a9-408b-b403-e77d6ffad173.png)

Terdapat 45466 data, dan 24 kolom yang bisa kita gunakan

![image](https://user-images.githubusercontent.com/76782988/189084429-67697e6c-a620-4521-942d-84414f3c9e52.png)


![image](https://user-images.githubusercontent.com/76782988/189084247-9750901e-e1ef-4711-aa3a-b8c5f1a674ca.png)

Beberapa kolom cukup membingungkan karena bernama cukup ambigu dan author data nya sendiri tidak mencatumkan deskripsinya. Meskipun begitu isi dari mayoritas kolomnya masih bisa kita prediksi:
* adult : boolean true false, menunjukkan apakah film termasuk film dewasa atau tidak
* belongs_to_collection : key pair value menunjukkan masuk grup mana sajakah film ini
* budget : biaya pembuatan film, probably
* genres : genre
* homepage : berisi link dari homepage film tersebut
* id : id dari film
* imdb_id : id dari film, pada imdb
* original_language : bahasa awal dari film
* original_title : judul film yang awal
* overview : berisi sinopsis dari film
* popularity : sebuah bilangan float yang menunjukkan seberapa populer film tersebut
* poster_path : link gambar dari poster promosi film tersebut
* production_companies : perusahaan yang memproduksi film tersebut
* production_countries : asal negara perusahaan nya
* release_date : tanggal rilis
* revenue : penghasilan
* runtime : lama film
* spoken_language : bahasa apa saja yang ada di film tersebut, probably
* status : apakah film tersebut sudah rilis, atau belum
* tagline : sinopsis, tapi lebih singkat ? idk tbh
* title : Judul film
* video : i have no idea. Kolom hanya diisi dengan 'False', can be ignored
* vote_average : rating yang diberikan user, probably
* vote_count : berapa banyak rating yang terhitung

## Data Preparation

Kita hanya akan menggunakan 2-3 kolom dari kolom diatas. Awalnya, saya ingin mengambil kolom `title`, `overview`, dan `adult`. Tetapi setelah saya telusuri datanya, terdapat kejanggalan pada `adult`

![image](https://user-images.githubusercontent.com/76782988/189086769-a071d65a-e690-4c06-9c70-40484e096eea.png)

Mayoritas kolom diisi oleh False, hanya ada 9 film yang dianggap True, dan 3 data lain bukanlah True False.

Jadi, akan kita hiraukan

Kita mengambil kolom `title` dan `overview` saja. Lalu kita buang nilai duplicate

![image](https://user-images.githubusercontent.com/76782988/189087183-cb33cdb1-6247-4620-8b93-36ca5553d8e9.png)

Jumlah data berkurang menjadi 45421. Setelah penulis coba, ternyata colab tidak kuat untuk menghandle data sebanyak ini, jadi kita kurangkan menjadi 20000 data. Lalu kita buang row yang tidak memiliki nilai.

![image](https://user-images.githubusercontent.com/76782988/189087734-6961a5ae-65fc-4069-8b2f-c21b3c860b8c.png)


Jumlah data final berupa 19863 data.

## Modeling

### Demographic based recommendation

Demographic based adalah dimana kita merekomendasikan item yang disenangi seluruh orang, tidak ada personaliasi sama sekali

Seperti disebut diatas, cara ini sangatlah simple, braindead solution, jadi saya bahkan tidak ingin repot repot mendemonstrasikannya. Ingat kolom `popularity`? Pada cara ini, kita tinggal mengsortir seluruh dataframe berdasarkan kolom ini, dari terbesar ke terkecil. Ya.. itu doang.

### Content based recommendation

Cara yang akan kita gunakan sekarang adalah merekomendasikan tergantung dari konten yang pernah dilihat oleh pengguna sebelumnya, sehingga terdapat beberapa personalisasi. 

Kita telah mengambil kolom `overview`, yang berisi sinopsis dari film. Sistem rekomendasi akan mencari film dengan sinopsis yang serupa. Kita akan menggunakan cosine similarity untuk menentukan kemiripan antar sinopsis, oleh karena itu kita harus merubah sinopsis menjadi vektor terlebih dahulu.

![image](https://user-images.githubusercontent.com/76782988/189089927-83d34ebd-98c6-4a65-9aff-370822490044.png)

Menghitung cosine similarity

![image](https://user-images.githubusercontent.com/76782988/189089990-f76e6189-1836-4abb-afd9-785eb8d6e75c.png)

Melihat cosine similarity

![image](https://user-images.githubusercontent.com/76782988/189090093-7ef34b9f-2c2a-458e-83ba-495d24fcb606.png)

Lalu membuat fungsi yang akan mengembalikan 15 item pertama yang paling mirip dengan judul film yang kita input.

![image](https://user-images.githubusercontent.com/76782988/189090349-b96c89fa-5dba-49d2-8830-ac6ab0581c2e.png)

Hasil

![image](https://user-images.githubusercontent.com/76782988/189090411-9e9ddc88-7d5d-4dab-9d45-86cbc16dcf56.png)

## Evaluation & Conclusion

Dari hasil diatas, bisa dilihat bahwa sistem bekerja dengan cukup baik. Ketika menginput judul 'Toy Story', sistem dapat merekomendasikan Toy Story 2 dan 3 yang memang merupakan *direct sequel* dari film tersebut.

Untuk metric sendiri, pada kasus ini, tidak ada metric yang bisa digunakan untuk menghitung tingkat akurasi dari sistem ini, dikarenakan benar atau tidaknya hasil rekomendasi merupakan hal yang sangat subjektif. Seseorang dapat mengira bahwa rekomendasi yang ia dapatkan sesuai, atau tidak sesuai, tergantung dari cara ia memandang film tersebut.

[1]
