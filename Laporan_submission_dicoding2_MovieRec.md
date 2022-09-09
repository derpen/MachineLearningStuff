# Laporan Proyek Machine Learning - Muhammad Rizqi Assabil

## Ulasan Proyek

Proyek ini adalah pembuatan sebuah sistem rekomendasi film. 

Adapun goal dari pembuatan sistem ini adalah untuk memberikan user sebuah rekomendasi film yang mungkin akan ia suka. Ini berguna dalam kasus dimana kita adalah pihak yang menayangkan film tersebut, misalnya kita adalah Netfliks. Dengan memberikan rekomendasi film serupa, user akan kembali lagi ke platform penanyangan film tersebut, sehingga meningkatkan keuntungan untuk perusahaan. 

Sistem rekomendasi sendiri pertama kali disebutkan pada 1998, yang dimana tujuan awalnya mirip seperti google scholar pada zaman sekarang[1].

## Business Understanding

### Problem Statement
* Sebagai perusahaan yang bergerak di bidang penayangan media, bagaimana cara merekomendasikan media hiburan yang serupa?

### Goals
* Merekomendasikan media hiburan yang serupa dengan apa yang user tersebut telah tonton.

### Solution Approach
* Kita akan menggunakan content-based recommendation system. Kita juga bisa menggunakan demographic based recommendation. Content based adalah dimana kita merekomendasikan sebuah item yang serupa dengan item yang telah dilihat/digunakan/disukai oleh user sebelumnya. Sedangkan demographic based adalah merekomendasikan sebuah item yang hampir seluruh user lain sukai. Asumsinya adalah jika item tersebut populer dikalang semua orang, maka user random ini juga akan menyukainya.

## Data Understanding

Data kita dapatkan dari kaggle, bernama [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset). Dataset akan kita download menggunakan API kaggle, langsung ke google colab

*Note: cara ini membutuhkan token yang diberikan oleh kaggle ke masing-masing user. Token bisa didapatkan dari page user anda*

![image](https://user-images.githubusercontent.com/76782988/189083517-1a6a8d66-9877-46df-b158-d244411ca2fb.png)

Kita unzip data nya, ternyata terdapat 7 file csv. Pada kasus ini, kita hanya membutuhkan `movies_metadata.csv`

Terdapat 45466 data, dan 24 kolom yang bisa kita gunakan

|index|0|1|2|3|4|
|---|---|---|---|---|---|
|adult|False|False|False|False|False|
|belongs\_to\_collection|\{'id': 10194, 'name': 'Toy Story Collection', 'poster\_path': '/7G9915LfUQ2lVfwMEEhDsn3kT4B\.jpg', 'backdrop\_path': '/9FBwqcd9IRruEDUrTdcaafOMKUq\.jpg'\}|NaN|\{'id': 119050, 'name': 'Grumpy Old Men Collection', 'poster\_path': '/nLvUdqgPgm3F85NMCii9gVFUcet\.jpg', 'backdrop\_path': '/hypTnLot2z8wpFS7qwsQHW1uV8u\.jpg'\}|NaN|\{'id': 96871, 'name': 'Father of the Bride Collection', 'poster\_path': '/nts4iOmNnq7GNicycMJ9pSAn204\.jpg', 'backdrop\_path': '/7qwE57OVZmMJChBpLEbJEmzUydk\.jpg'\}|
|budget|30000000|65000000|0|16000000|0|
|genres|\[\{'id': 16, 'name': 'Animation'\}, \{'id': 35, 'name': 'Comedy'\}, \{'id': 10751, 'name': 'Family'\}\]|\[\{'id': 12, 'name': 'Adventure'\}, \{'id': 14, 'name': 'Fantasy'\}, \{'id': 10751, 'name': 'Family'\}\]|\[\{'id': 10749, 'name': 'Romance'\}, \{'id': 35, 'name': 'Comedy'\}\]|\[\{'id': 35, 'name': 'Comedy'\}, \{'id': 18, 'name': 'Drama'\}, \{'id': 10749, 'name': 'Romance'\}\]|\[\{'id': 35, 'name': 'Comedy'\}\]|
|homepage|http://toystory\.disney\.com/toy-story|NaN|NaN|NaN|NaN|
|id|862|8844|15602|31357|11862|
|imdb\_id|tt0114709|tt0113497|tt0113228|tt0114885|tt0113041|
|original\_language|en|en|en|en|en|
|original\_title|Toy Story|Jumanji|Grumpier Old Men|Waiting to Exhale|Father of the Bride Part II|
|overview|Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene\. Afraid of losing his place in Andy's heart, Woody plots against Buzz\. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences\.|When siblings Judy and Peter discover an enchanted board game that opens the door to a magical world, they unwittingly invite Alan -- an adult who's been trapped inside the game for 26 years -- into their living room\. Alan's only hope for freedom is to finish the game, which proves risky as all three find themselves running from giant rhinoceroses, evil monkeys and other terrifying creatures\.|A family wedding reignites the ancient feud between next-door neighbors and fishing buddies John and Max\. Meanwhile, a sultry Italian divorcée opens a restaurant at the local bait shop, alarming the locals who worry she'll scare the fish away\. But she's less interested in seafood than she is in cooking up a hot time with Max\.|Cheated on, mistreated and stepped on, the women are holding their breath, waiting for the elusive "good man" to break a string of less-than-stellar lovers\. Friends and confidants Vannah, Bernie, Glo and Robin talk it all out, determined to find a better way to breathe\.|Just when George Banks has recovered from his daughter's wedding, he receives the news that she's pregnant \.\.\. and that George's wife, Nina, is expecting too\. He was planning on selling their home, but that's a plan that -- like George -- will have to change with the arrival of both a grandchild and a kid of his own\.|
|popularity|21\.946943|17\.015539|11\.7129|3\.859495|8\.387519|
|poster\_path|/rhIRbceoE9lR4veEXuwCC2wARtG\.jpg|/vzmL6fP7aPKNKPRTFnZmiUfciyV\.jpg|/6ksm1sjKMFLbO7UY2i6G1ju9SML\.jpg|/16XOMpEaLWkrcPqSQqhTmeJuqQl\.jpg|/e64sOI48hQXyru7naBFyssKFxVd\.jpg|
|production\_companies|\[\{'name': 'Pixar Animation Studios', 'id': 3\}\]|\[\{'name': 'TriStar Pictures', 'id': 559\}, \{'name': 'Teitler Film', 'id': 2550\}, \{'name': 'Interscope Communications', 'id': 10201\}\]|\[\{'name': 'Warner Bros\.', 'id': 6194\}, \{'name': 'Lancaster Gate', 'id': 19464\}\]|\[\{'name': 'Twentieth Century Fox Film Corporation', 'id': 306\}\]|\[\{'name': 'Sandollar Productions', 'id': 5842\}, \{'name': 'Touchstone Pictures', 'id': 9195\}\]|
|production\_countries|\[\{'iso\_3166\_1': 'US', 'name': 'United States of America'\}\]|\[\{'iso\_3166\_1': 'US', 'name': 'United States of America'\}\]|\[\{'iso\_3166\_1': 'US', 'name': 'United States of America'\}\]|\[\{'iso\_3166\_1': 'US', 'name': 'United States of America'\}\]|\[\{'iso\_3166\_1': 'US', 'name': 'United States of America'\}\]|
|release\_date|1995-10-30|1995-12-15|1995-12-22|1995-12-22|1995-02-10|
|revenue|373554033|262797249|0|81452156|76578911|
|runtime|81|104|101|127|106|
|spoken\_languages|\[\{'iso\_639\_1': 'en', 'name': 'English'\}\]|\[\{'iso\_639\_1': 'en', 'name': 'English'\}, \{'iso\_639\_1': 'fr', 'name': 'Français'\}\]|\[\{'iso\_639\_1': 'en', 'name': 'English'\}\]|\[\{'iso\_639\_1': 'en', 'name': 'English'\}\]|\[\{'iso\_639\_1': 'en', 'name': 'English'\}\]|
|status|Released|Released|Released|Released|Released|
|tagline|NaN|Roll the dice and unleash the excitement\!|Still Yelling\. Still Fighting\. Still Ready for Love\.|Friends are the people who let you be yourself\.\.\. and never let you forget it\.|Just When His World Is Back To Normal\.\.\. He's In For The Surprise Of His Life\!|
|title|Toy Story|Jumanji|Grumpier Old Men|Waiting to Exhale|Father of the Bride Part II|
|video|false|false|false|false|false|
|vote\_average|7\.7|6\.9|6\.5|6\.1|5\.7|
|vote\_count|5415|2413|92|34|173|

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

Kita hanya akan menggunakan 2-3 kolom dari kolom diatas. Awalnya, penulis ingin mengambil kolom `title`, `overview`, dan `adult`. Tetapi setelah penulis telusuri datanya, terdapat kejanggalan pada `adult`

Mayoritas kolom diisi oleh False, hanya ada 9 film yang dianggap True, dan 3 data lain bukanlah True False.

Jadi, akan kita hiraukan

Kita mengambil kolom `title` dan `overview` saja. Lalu kita buang nilai duplicate

|index|title|overview|
|---|---|---|
|0|Toy Story|Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene\. Afraid of losing his place in Andy's heart, Woody plots against Buzz\. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences\.|
|1|Jumanji|When siblings Judy and Peter discover an enchanted board game that opens the door to a magical world, they unwittingly invite Alan -- an adult who's been trapped inside the game for 26 years -- into their living room\. Alan's only hope for freedom is to finish the game, which proves risky as all three find themselves running from giant rhinoceroses, evil monkeys and other terrifying creatures\.|
|2|Grumpier Old Men|A family wedding reignites the ancient feud between next-door neighbors and fishing buddies John and Max\. Meanwhile, a sultry Italian divorcée opens a restaurant at the local bait shop, alarming the locals who worry she'll scare the fish away\. But she's less interested in seafood than she is in cooking up a hot time with Max\.|
|3|Waiting to Exhale|Cheated on, mistreated and stepped on, the women are holding their breath, waiting for the elusive "good man" to break a string of less-than-stellar lovers\. Friends and confidants Vannah, Bernie, Glo and Robin talk it all out, determined to find a better way to breathe\.|
|4|Father of the Bride Part II|Just when George Banks has recovered from his daughter's wedding, he receives the news that she's pregnant \.\.\. and that George's wife, Nina, is expecting too\. He was planning on selling their home, but that's a plan that -- like George -- will have to change with the arrival of both a grandchild and a kid of his own\.|

Jumlah data berkurang menjadi 45421. Setelah penulis coba, ternyata colab tidak kuat untuk menghandle data sebanyak ini, jadi kita kurangkan menjadi 20000 data. Lalu kita buang row yang tidak memiliki nilai.

Jumlah data final berupa 19863 data.

## Modeling

### Demographic based recommendation

Demographic based adalah dimana kita merekomendasikan item yang disenangi seluruh orang, tidak ada personaliasi sama sekali

Seperti disebut diatas, cara ini sangatlah simple, braindead solution, jadi penulis bahkan tidak ingin repot repot mendemonstrasikannya. Ingat kolom `popularity`? Pada cara ini, kita tinggal mengsortir seluruh dataframe berdasarkan kolom ini, dari terbesar ke terkecil. Ya.. itu doang.

### Content based recommendation

Cara yang akan kita gunakan sekarang adalah merekomendasikan tergantung dari konten yang pernah dilihat oleh pengguna sebelumnya, sehingga terdapat beberapa personalisasi. 

Kita telah mengambil kolom `overview`, yang berisi sinopsis dari film. Sistem rekomendasi akan mencari film dengan sinopsis yang serupa. Kita akan menggunakan cosine similarity untuk menentukan kemiripan antar sinopsis, oleh karena itu kita harus merubah sinopsis menjadi vektor terlebih dahulu.

Menghitung cosine similarity

![image](https://user-images.githubusercontent.com/76782988/189089990-f76e6189-1836-4abb-afd9-785eb8d6e75c.png)

Cosine similarity sendiri adalah cos dari perbedaan sudut dua titik vektor. Semakin sedikit perbedaan sudutnya, semakin besar juga hasil dari similarity nya. Implementasi dari formula ini adalah mencari kalimat yang serupa dengan melihat apakah kata-kata didalamnya juga serupa.

![image](https://user-images.githubusercontent.com/76782988/189264316-7a735e74-029b-4615-9909-d7191f8ac91e.png)

Lalu membuat fungsi yang akan mengembalikan 5 item pertama yang paling mirip dengan judul film yang kita input.

![image](https://user-images.githubusercontent.com/76782988/189090349-b96c89fa-5dba-49d2-8830-ac6ab0581c2e.png)

Hasil

Memberikan 'Toy Story' sebagai input

|index|title|overview|
|---|---|---|
|0|Toy Story 3|Woody, Buzz, and the rest of Andy's toys haven't been played with in years\. With Andy about to go to college, the gang find themselves accidentally left at a nefarious day care center\. The toys must band together to escape and return home to Andy\.|
|1|Toy Story 2|Andy heads off to Cowboy Camp, leaving his toys to their own devices\. Things shift into high gear when an obsessive toy collector named Al McWhiggen, owner of Al's Toy Barn kidnaps Woody\. Andy's toys mount a daring rescue mission, Buzz Lightyear meets his match and Woody has to decide where he and his heart truly belong\.|
|2|The 40 Year Old Virgin|Andy Stitzer has a pleasant life with a nice apartment and a job stamping invoices at an electronics store\. But at age 40, there's one thing Andy hasn't done, and it's really bothering his sex-obsessed male co-workers: Andy is still a virgin\. Determined to help Andy get laid, the guys make it their mission to de-virginize him\. But it all seems hopeless until Andy meets small business owner Trish, a single mom\.|
|3|The Champ|The more you love, the harder you fight\.The world looks at Billy Flynn and sees a has-been who seemingly never was, an ex-boxing champion slammed to the mat years ago by booze and gambling\. But Billy's son TJ sees what the world doesn't\. He knows his flawed but loving father is, was and always will be The Champ\.|
|4|The Champ|Dink Purcell loves his alcoholic father, ex-heavyweight champion Andy "Champ" Purcell, despite his frequent binges, his frequent gambling and their squalid living conditions\. And there's nothing Andy wouldn't do for Dink\. When Andy wins a race horse gambling, he gives it to Dink and they race it at a Tijuana track\. There, Dink meets Linda Carleton, a race horse owner herself, and they have an immediate rapport\. But Linda's rich husband sees Andy and realizes Dink is Linda's son, who she gave up when she and Andy divorced\. Andy is bribed $200 to allow Dink to visit with Linda, but refuses to allow Dink to spend six months with the Carletons\. When Andy loses the horse gambling and winds up in jail after a drunken tirade, he realizes Dink's place is with his mother\. Dink tearfully goes but sneaks out and returns at his first opportunity, filling a depressed Andy with a desire to make good\. So Andy goes into training after his managers arrange a boxing match with the Mexican champion\.|

Memberikan 'Jumanji' sebagai input

|index|title|overview|
|---|---|---|
|0|Brainscan|A lonely teenage horror-movie fan discovers a mysterious computer game that uses hypnosis to custom-tailor the game into the most terrifying experience imaginable\. When he emerges from the hypnotic trance he is horrified to find evidence that the brutal murder depicted in the game actually happened -- and he's the killer\.|
|1|Stay Alive|After the mysterious, brutal death of an old friend, a group of teenagers find themselves in possession of "Stay Alive," an ultra-realistic 3-D videogame based on the spine-chilling true story of a 17th century noblewoman, known as "The Blood Countess\." The gamers don't know anything about the game other than they're not supposed to have it\.\.\. and they're dying to play it\. Not able to resist temptation, the kids begin to play the grisly game but soon make a chilling connection -- they are each being murdered one-by-one in the same way as the characters they played in the game\. As the line between the game world and the real world disappears, the teens must find a way to defeat the vicious and merciless Blood Countess, all the while trying to\.\.\. stay alive\.|
|2|Word Wars|The classic board game, Scrabble, has been popular for decades\. In addition, there are fanatics who devote heart and soul to this game to the expense of everything else\. This film profiles a group of these enthusiasts as they converge for a Scrabble convention where the word game is almost a bloodsport\.|
|3|The Dark Angel|Kitty Vane, Alan Trent, and Gerald Shannon have been inseparable friends since childhood\. Kitty has always known she would marry one of them, but has waited until the beginning of World War I before finally choosing Alan\. Gerald graciously gives them his blessing\. Then, Gerald and Alan go to war\. Angered over a misunderstanding involving Alan and Kitty, Gerald sends Alan on a dangerous mission that will change all their lives forever\.|
|4|The Mindscape of Alan Moore|The Mindscape of Alan Moore is a psychedelic journey into one of the world's most powerful minds; chronicling the life and work of Alan Moore, author of several acclaimed graphic novels, including "From Hell," "Watchmen" and "V for Vendetta\." It is the only feature film production on which Alan Moore has collaborated, with permission to use his work\. Alan Moore presents the story of his development as an artist, starting with his childhood and working through to his comics career and impact on that medium, and his emerging interest in magic\.|

## Evaluation & Conclusion

Dari hasil diatas, bisa dilihat bahwa sistem bekerja dengan cukup baik. Ketika menginput judul 'Toy Story', sistem dapat merekomendasikan Toy Story 2 dan 3 yang memang merupakan *direct sequel* dari film tersebut. Ketika kita mencari film yang mirip dengan 'Jumanji', film yang direkomendasikan adalah film-film lain yang bertemakan permainan.

Untuk metric sendiri, pada kasus ini, tidak ada metric yang bisa digunakan untuk menghitung tingkat akurasi dari sistem ini. Sistem ini tidak memiliki sebuah *True Value* yang bisa digunakan, karena kita menggunakan sinopsis film untuk membuat sebuah rekomendasi. Sistem tidak tau apakah isi sinopsis sesuai dengan keinginan user atau tidak. Benar atau tidaknya hasil rekomendasi merupakan hal yang sangat subjektif. Seseorang dapat mengira bahwa rekomendasi yang ia dapatkan sesuai, atau tidak sesuai, tergantung dari cara ia memandang film tersebut. Idealnya kita juga  memperhitungkan kolom lain seperti *genre* dan/atau *production companies* agar seorang domain expert dapat menentukan lebih mudah apakah film tersebut serupa atau tidak. 

Atau, jika ingin iseng menggunakan precision, dilihat dari contoh output 'Toy Story', jika kita anggap Toy Story 2 dan 3 sebagai nilai benar, dan sisanya sebagai nilai salah, kita mendapatkan akurasi sebesar 40%.

[1] Bollacker, Kurt D., Steve Lawrence, and C. Lee Giles. "CiteSeer: An autonomous web agent for automatic retrieval and identification of interesting publications." Proceedings of the second international conference on Autonomous agents. 1998.
