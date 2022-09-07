# Laporan Proyek Machine Learning - Muhammad Rizqi Assabil

## Domain Proyek

Proyek kali ini adalah clustering data kartu kredit menggunakan algoritma K-Means. Adapun proyek ini sendiri dipilih karena penulis sedang ingin mempelajari kasus clustering.

Problem yang ingin diselesaikan adalah untuk mendeteksi fraud (pemalsuan/penipuan) dalam penggunaan kartu kredit. Teknik nya cukup mudah, yaitu dengan melakukan clustering pada data. Data dari hasil penipuan umumnya akan langsung terdeteksi sebagai outlier, dan otomatis terbuat cluster nya sendiri (In Theory at least).

Referensi: Soon™

## Business Understanding

### Problem Statement
* Bagaimana cara kita mendeteksi fraud pada penggunaan kartu kredit?

### Goals
* Menggunakan algoritma clustering, pada kasus ini K-Means, untuk mendeteksinya

### Why K-Means (Solution Statement)?
* Karena ini adalah salah satu algoritma paling umum untuk melakukan clustering. Referensi sudah banyak, sehingga hasil dari proyek ini dapat direplikasi secara konsisten, dan mudah untuk di-improve

## Data Understanding

Data didapatkan dari kaggle, [CC General](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata), yang berupa file csv dengan 17 column yang bisa digunakan. Antara lain adalah berapa banyak uang lagi di akun mereka, samapi pengunaan total dari sebuah akun.

