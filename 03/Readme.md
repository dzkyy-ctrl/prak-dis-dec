# Praktikum 03 — Sinkronisasi dan Koordinasi Sistem Terdistribusi

## Tujuan

Modul ini membahas cara sistem terdistribusi mengelola waktu dan urutan kejadian, menjalankan pekerjaan secara bersamaan, mencegah konflik akses data, menangani deadlock, serta memilih pemimpin menggunakan algoritma Raft. Praktikum menggunakan NetTime dan contoh program Python.

## Dasar Teori

### Sinkronisasi waktu

Setiap komputer memiliki jam fisik yang dapat berbeda karena perbedaan perangkat keras, drift, dan kondisi jaringan. Protokol Network Time Protocol (NTP) membantu menyelaraskan jam komputer dengan server waktu. Sinkronisasi waktu berguna untuk pencatatan waktu dan pemantauan, tetapi jam fisik saja tidak cukup untuk menentukan urutan sebab-akibat antarperistiwa pada sistem terdistribusi.

### Vector clock dan hubungan kausal

Vector clock menyimpan sebuah penghitung untuk setiap proses. Proses menaikkan penghitung lokal saat terjadi peristiwa; saat mengirim pesan, nilai vector clock ikut dikirim; dan saat menerima pesan, proses mengambil nilai maksimum setiap komponen lalu menaikkan penghitung lokalnya. Untuk dua vector clock A dan B, A terjadi-sebelum B jika setiap komponen A tidak lebih besar dari komponen B dan setidaknya satu komponennya lebih kecil. Jika tidak ada hubungan terjadi-sebelum dalam kedua arah, peristiwanya konkuren.

### Thread, race condition, dan mutual exclusion

Thread memungkinkan beberapa alur kerja berjalan secara konkuren dalam satu proses. Ketika beberapa thread membaca dan mengubah data bersama tanpa sinkronisasi yang tepat, hasilnya dapat bergantung pada urutan penjadwalan; keadaan ini disebut race condition. Lock atau mutex memberikan mutual exclusion: hanya satu thread pada satu waktu yang dapat menjalankan bagian kritis yang dilindungi lock.

### Deadlock

Deadlock adalah keadaan ketika beberapa thread saling menunggu sumber daya yang sedang dipegang thread lain sehingga tidak ada yang dapat melanjutkan. Deadlock dapat terjadi ketika kondisi seperti mutual exclusion, hold-and-wait, tidak ada preemption, dan circular wait muncul bersamaan. Strategi pencegahan antara lain mengatur urutan pengambilan lock secara konsisten atau tidak menahan satu lock ketika meminta lock berikutnya.

### Algoritma konsensus Raft

Raft mengoordinasikan beberapa node melalui pemilihan pemimpin dan replikasi log. Node dapat berstatus **follower**, **candidate**, atau **leader**. Ketika follower tidak menerima heartbeat dalam batas waktu pemilihan, node dapat menjadi candidate dan meminta suara. Candidate yang memperoleh mayoritas menjadi leader; leader mengirim heartbeat dan mengelola entri log. Dalam implementasi Raft yang lengkap, aturan term, pemungutan suara, replikasi, dan komit log menjaga konsistensi meskipun ada kegagalan node.

Diagram berikut menggambarkan tahapan pemilihan dan koordinasi node yang menjadi konteks pembahasan Raft.

![Gambar 1. Diagram konseptual pertukaran pesan dan pemilihan leader pada beberapa node.](Source%20Code/02_Raft.jpeg)

*Pembahasan 1: Ikuti arah panah untuk melihat pertukaran pesan antar-node. Proses dimulai ketika sebuah node mengumumkan diri sebagai candidate, dilanjutkan dengan pengiriman dan pemeriksaan suara; setelah mayoritas tercapai, leader dipilih dan informasi leader diperbarui pada node lain. Diagram ini membantu merangkum urutan koordinasi yang menjadi gagasan dasar pemilihan pemimpin pada Raft.*

## Pembahasan Langkah Praktikum

### 1. Instalasi dan sinkronisasi waktu dengan NetTime

NetTime digunakan sebagai layanan sinkronisasi waktu berbasis server waktu jaringan. Ikuti wizard instalasi, periksa konfigurasi server, lalu amati status sinkronisasi.

![Gambar 2. Halaman awal wizard instalasi NetTime.](Source%20Code/01_Install_Nettime.png)

*Pembahasan 2: Jalankan installer NetTime hingga halaman sambutan ini tampil. Baca informasi awal, lalu klik **Next** untuk memulai wizard instalasi; pilih **Cancel** hanya jika ingin membatalkan proses. Halaman ini menjadi langkah pertama sebelum menentukan lokasi dan opsi pemasangan.*

![Gambar 3. Pemilihan lokasi instalasi NetTime.](Source%20Code/02_Install_Nettime.png)

*Pembahasan 3: Pada langkah pemilihan lokasi, periksa folder tujuan yang ditawarkan installer, yaitu `C:\Program Files (x86)\NetTime`. Gunakan **Browse** jika ingin memilih folder lain, lalu klik **Next** untuk melanjutkan. Pastikan ruang penyimpanan mencukupi sebelum memasang aplikasi.*

![Gambar 4. Pemilihan folder Start Menu.](Source%20Code/03_Install_Nettime.png)

*Pembahasan 4: Tentukan folder yang akan digunakan untuk pintasan program pada Start Menu. Nama bawaan yang ditampilkan adalah **NetTime**; nama ini dapat dipertahankan atau diubah sesuai kebutuhan. Klik **Next** setelah menentukan pilihan.*

![Gambar 5. Pemilihan tugas tambahan instalasi.](Source%20Code/04_Install_Nettime.png)

*Pembahasan 5: Periksa tugas tambahan yang akan dilakukan installer. Opsi **Install as Service (Recommended)** terlihat dipilih agar NetTime dapat berjalan sebagai layanan Windows; biarkan aktif untuk mengikuti konfigurasi yang direkomendasikan. Klik **Next** untuk menuju ringkasan instalasi.*

![Gambar 6. Ringkasan konfigurasi sebelum instalasi.](Source%20Code/05_Install_Nettime.png)

*Pembahasan 6: Sebelum memasang, tinjau kembali ringkasan lokasi tujuan, folder Start Menu, dan opsi layanan. Jika ada pengaturan yang perlu diubah, kembali ke langkah sebelumnya; jika sudah sesuai, klik **Install**. Langkah ini memastikan konfigurasi yang dipilih benar sebelum file program dipasang.*

![Gambar 7. Instalasi NetTime selesai.](Source%20Code/06_Install_Nettime.png)

*Pembahasan 7: Tunggu hingga wizard menyatakan instalasi NetTime telah selesai. Opsi **Start NetTime now** dicentang pada tangkapan layar, sehingga aplikasi akan dijalankan setelah tombol **Finish** ditekan. Klik **Finish** untuk menutup wizard dan melanjutkan ke konfigurasi aplikasi.*

![Gambar 8. Konfigurasi server dan interval NetTime.](Source%20Code/07_Sinkronisasi_Nettime.png)

*Pembahasan 8: Buka pengaturan NetTime dan tinjau daftar server waktu yang akan digunakan, protokol **SNTP**, dan port **123**. Periksa juga interval pembaruan dan percobaan ulang; opsi layanan saat komputer dinyalakan dapat dibiarkan aktif agar sinkronisasi berjalan otomatis. Setelah pengaturan server dan jadwal diperiksa, simpan pilihan dengan **OK**.*

![Gambar 9. Status sinkronisasi waktu NetTime.](Source%20Code/08_Sinkronisasi_Nettime.png)

*Pembahasan 9: Setelah konfigurasi diterapkan, buka jendela status untuk memeriksa waktu sistem, percobaan terakhir, dan hasil sinkronisasi. Pada tangkapan layar, aplikasi menyatakan waktu telah tersinkronisasi; satu server berstatus **Good** dengan offset +25 ms, sedangkan server lain belum digunakan atau gagal. Nilai tersebut adalah hasil pada saat gambar diambil, sehingga hasil pada komputer lain dapat berbeda.*

### 2. Vector clock

Program `vclocks.py` membuat tiga vector clock untuk proses P0, P1, dan P2. Peristiwa lokal menaikkan komponen proses terkait. Pengiriman dan penerimaan pesan menyebarkan informasi kausal sehingga proses penerima dapat menggabungkan jam logisnya.

![Gambar 10. Implementasi kelas VectorClock dan skenario pengiriman pesan.](Source%20Code/10_vclocks.png)

*Pembahasan 10: Implementasi dimulai dengan membuat daftar penghitung bernilai nol untuk seluruh proses. `increment()` menaikkan komponen lokal, `send_message()` menaikkan jam sebelum mengirim salinannya, dan `receive_message()` menggabungkan nilai yang diterima dengan mengambil maksimum tiap komponen lalu menaikkan jam lokal. Di bagian akhir, `happens_before()` membandingkan dua vector clock, sedangkan `is_concurrent()` menyatakan konkuren jika tidak ada hubungan kausal dalam kedua arah; skenario di bawah kelas menjalankan operasi-operasi tersebut.*

![Gambar 11. Keluaran simulasi vector clock.](Source%20Code/11_Output_Vclocks.png)

*Pembahasan 11: Baca keluaran dari atas ke bawah: mula-mula jam ketiga proses bernilai nol, lalu P0 menaikkan komponen lokalnya dan kembali menaikkannya saat menyiapkan pesan. P1 menggabungkan nilai pesan dan menaikkan komponen sendiri; kemudian P2 melakukan peristiwa lokal dan menerima pesan dari P1. Baris pemeriksaan di bagian akhir menunjukkan arah hubungan happens-before dan apakah pasangan yang diuji konkuren.*

![Gambar 12. Program utama untuk menguji vector clock.](Source%20Code/12_Main_vclocks.png)

*Pembahasan 12: Program utama mengimpor kelas `VectorClock`, lalu membuat objek untuk P0, P1, dan P2 dengan jumlah proses yang sama. P0 mencatat satu peristiwa lokal dan menyiapkan pesan; P1 menerima pesan tersebut sehingga jamnya digabungkan dengan jam P0. Terakhir, program mencetak ketiga jam untuk membandingkan proses pengirim, penerima, dan proses yang belum menerima pesan.*

![Gambar 13. Keluaran pengujian utama vector clock.](Source%20Code/13_Output_Main_Vclock.png)

*Pembahasan 13: Jalankan program utama dan amati perubahan nilai: P0 bertambah ketika melakukan peristiwa dan mengirim pesan, sementara P1 menggabungkan pesan lalu menaikkan komponen lokalnya. P2 tetap menunjukkan jam lokalnya karena tidak terlibat dalam pertukaran pada skrip utama ini. Pada keluaran program lengkap, hasil `happens before` dan `is concurrent` mencerminkan urutan kejadian yang dibentuk skenario, bukan urutan waktu dinding.*

### 3. Thread

Contoh berikut menjalankan lima tugas dengan thread terpisah. Pemanggilan `start()` memulai setiap tugas, sedangkan `join()` membuat program menunggu hingga seluruh tugas selesai.

![Gambar 14. Pembuatan, pemanggilan, dan penantian lima thread.](Source%20Code/14_multithreads-example.png)

*Pembahasan 14: Fungsi `task` mencetak pesan mulai, menunggu selama durasi yang diberikan, lalu mencetak pesan selesai. Program membuat lima objek thread A–E dengan fungsi dan jeda lima detik yang sama. Seluruh thread dimulai menggunakan `start()` sebelum `join()` dipanggil satu per satu; karena itu tugas dapat berjalan konkuren, tetapi program utama tetap menunggu semuanya selesai.*

![Gambar 15. Keluaran eksekusi lima thread.](Source%20Code/15_Output_multithreads-example.png)

*Pembahasan 15: Pada keluaran terminal, perintah untuk memulai A sampai E tampak lebih dahulu karena semua thread sudah dijalankan sebelum program menunggu. Setelah jeda, pesan selesai muncul dengan urutan yang dapat berubah sesuai penjadwalan sistem operasi. Pesan **All tasks completed** tampil paling akhir karena program baru mencetaknya setelah semua pemanggilan `join()` selesai.*

### 4. Race condition dan penggunaan lock

Pada percobaan pertama, dua thread mencoba menarik Rp80 dari saldo bersama Rp100. Pemeriksaan saldo dan pengurangan saldo bukan satu operasi atomik, sehingga kedua thread dapat sama-sama lolos pemeriksaan sebelum salah satunya memperbarui saldo.

![Gambar 16. Kode penarikan saldo tanpa sinkronisasi.](Source%20Code/16_Race_Conditions-01.png)

*Pembahasan 16: Program menetapkan saldo bersama sebesar 100 dan membuat fungsi `withdraw` untuk memeriksa apakah saldo cukup sebelum melakukan pengurangan. Jeda `sleep(0.01)` berada setelah pemeriksaan, sehingga thread lain berpeluang membaca saldo lama sebelum pengurangan pertama tersimpan. Dua thread kemudian dimulai bersamaan dan keduanya ditunggu dengan `join()`; bagian pemeriksaan hingga pengurangan belum dilindungi lock.*

![Gambar 17. Hasil race condition pada saldo.](Source%20Code/17_Output_Race_Condition-01.png)

*Pembahasan 17: Jalankan program beberapa kali dan amati pesan hasil penarikan beserta saldo akhirnya. Pada keluaran ini kedua thread sama-sama lolos pemeriksaan saldo Rp100, lalu masing-masing mengurangi Rp80 sehingga saldo menjadi -Rp60. Hasil tersebut mencontohkan race condition: langkah membaca, memeriksa, dan mengubah saldo seharusnya diperlakukan sebagai satu bagian kritis.*

![Gambar 18. Ilustrasi race condition pada variabel bersama.](Source%20Code/18_2_Data_Race_Condition.jpeg)

*Pembahasan 18: Ikuti dua kolom thread pada ilustrasi: keduanya membaca nilai awal `counter = 0`, menghitung nilai baru dengan menambah satu, lalu menulis hasil masing-masing ke memori. Jika pembacaan dilakukan sebelum salah satu penulisan terlihat oleh thread lain, keduanya dapat menulis nilai 1, padahal hasil penjumlahan dua operasi seharusnya 2. Ini menunjukkan bagaimana akses bersamaan terhadap variabel bersama dapat kehilangan pembaruan.*

Pada percobaan kedua, lock dipasang untuk melindungi pemeriksaan dan perubahan saldo sebagai satu bagian kritis. Thread yang lain menunggu hingga lock dilepas.

![Gambar 19. Kode penarikan saldo dengan lock.](Source%20Code/19_Race_Conditions-2.png)

*Pembahasan 19: Program membuat satu objek `Lock` bersama yang dipakai oleh kedua thread. Di dalam blok `with counter_lock`, thread melakukan pemeriksaan saldo, jeda, pengurangan, dan pencetakan hasil; thread lain harus menunggu hingga blok tersebut selesai dan lock dilepas otomatis. Dengan demikian, pemeriksaan dan perubahan saldo menjadi satu bagian kritis yang tidak disela oleh penarikan lain.*

![Gambar 20. Hasil penarikan saldo setelah memakai lock.](Source%20Code/20_Output_Race_Condition-02.png)

*Pembahasan 20: Jalankan versi yang memakai lock dan lihat hasil transaksi. Thread yang lebih dahulu memperoleh lock memeriksa saldo Rp100, menarik Rp80, dan menyisakan Rp20; setelah lock dilepas, thread berikutnya memeriksa saldo terbaru dan tidak melakukan penarikan karena dana kurang. Saldo tidak menjadi negatif karena transaksi berlangsung secara bergiliran.*

### 5. Deadlock

Percobaan pertama menggunakan dua lock dengan urutan pengambilan yang berlawanan. Thread pertama memegang A dan menunggu B, sedangkan thread kedua memegang B dan menunggu A. Keduanya dapat saling menunggu tanpa batas waktu.

![Gambar 21. Kode yang berpotensi mengalami deadlock.](Source%20Code/21_Deadlock-01.png)

*Pembahasan 21: Periksa fungsi pertama: Thread 1 masuk ke `lock_a`, berhenti sejenak, lalu mencoba masuk ke `lock_b` tanpa melepas A. Fungsi kedua mengambil B terlebih dahulu, berhenti, lalu mencoba meminta A. Ketika kedua jeda berakhir pada waktu yang berdekatan, setiap thread dapat memegang satu lock sambil menunggu lock yang dipegang thread lainnya, membentuk siklus tunggu.*

![Gambar 22. Keluaran ketika kedua thread saling menunggu.](Source%20Code/22_Output_Deadlock-01.png)

*Pembahasan 22: Setelah menjalankan program, terminal mencetak bahwa Thread 1 telah mengunci A dan menunggu B, sementara Thread 2 telah mengunci B dan menunggu A. Karena kedua lock masih dipegang, tidak ada thread yang dapat mencapai pesan berhasil mengunci keduanya atau menyelesaikan fungsi. Pemanggilan `join()` ikut menunggu, sehingga proses tampak berhenti pada keluaran ini.*

![Gambar 23. Ilustrasi alokasi dan permintaan sumber daya.](Source%20Code/23_2-Deadlock-01.jpeg)

*Pembahasan 23: Identifikasi bentuk oval sebagai proses dan kotak sebagai sumber daya, lalu ikuti arah panah antara keduanya. Panah dari sumber daya ke proses menggambarkan alokasi, sedangkan panah dari proses ke sumber daya menunjukkan permintaan yang masih menunggu. Periksa apakah rangkaian panah membentuk siklus; siklus menandakan potensi deadlock, terutama ketika setiap sumber daya hanya dapat dimiliki satu proses pada satu waktu.*

Percobaan berikutnya mengubah urutan kerja: thread melepas lock pertama sebelum meminta lock kedua. Dengan tidak menahan lock pertama selama menunggu lock lain, pola hold-and-wait pada contoh ini dihindari.

![Gambar 24. Kode alternatif untuk menghindari saling menunggu lock.](Source%20Code/24_Deadlock-02.png)

*Pembahasan 24: Setiap thread mencoba memperoleh lock pertamanya dengan batas tunggu lima detik. Setelah pekerjaan singkat, blok `finally` melepaskan lock tersebut sebelum thread meminta lock kedua; karena tidak menahan lock pertama saat menunggu, pola saling menunggu pada contoh sebelumnya diputus. Akuisisi kedua juga memakai timeout dan setiap lock yang berhasil diperoleh dilepas kembali dalam `finally`.*

![Gambar 25. Keluaran program deadlock alternatif.](Source%20Code/25_Output_Deadlock-02.png)

*Pembahasan 25: Amati urutan terminal: Thread 1 memperoleh A dan Thread 2 memperoleh B, lalu keduanya mengumumkan sedang menunggu lock berikutnya. Karena lock awal sudah dilepas, masing-masing thread dapat memperoleh lock lainnya secara bergantian dan melepaskannya. Program kemudian mencetak **Execution Finished**, menunjukkan bahwa kedua thread dan pemanggilan `join()` telah selesai.*

### 6. Simulasi konsensus Raft

Simulasi pertama memodelkan tiga node dan menampilkan status node, term, serta panjang log pada setiap langkah. Timeout pemilihan dibuat acak sehingga node yang terpilih pada simulasi dapat berbeda.

![Gambar 26. Implementasi simulasi node Raft.](Source%20Code/26_Raft_py.png)

*Pembahasan 26: Implementasi menetapkan tiga status node melalui enum, lalu menginisialisasi identitas node, term, suara, log, indeks commit, dan timeout pemilihan. `on_heartbeat()` memperbarui term dan mengembalikan node ke follower jika heartbeat diterima; `start_election()` menaikkan term dan menjalankan pemilihan sederhana. `append_entry()` menambah entri saat node berstatus leader, sedangkan `tick()` memeriksa timeout; fungsi simulasi kemudian membuat tiga node dan menampilkan statusnya pada setiap langkah.*

![Gambar 27. Keluaran simulasi Raft, langkah awal.](Source%20Code/27_1_Output_Raft.png)

*Pembahasan 27: Jalankan simulasi dan ikuti status tiga node pada langkah-langkah awal; semuanya mula-mula berstatus follower pada term 0. Ketika timeout salah satu node tercapai, node tersebut menjadi candidate dan dalam simulasi memperoleh suara mayoritas sehingga menjadi leader pada term 1. Pada bagian keluaran ini Node 3 terpilih dan kemudian menambahkan `command-5` ke log lokalnya.*

![Gambar 28. Keluaran simulasi Raft, langkah lanjutan.](Source%20Code/27_2_Output_Raft.png)

*Pembahasan 28: Lanjutkan membaca keluaran langkah demi langkah: heartbeat dari leader memperbarui term follower dan mempertahankan status mereka sebagai follower. Pada langkah yang dipilih oleh kondisi program, Node 3 menambahkan perintah dan panjang log lokalnya naik; pada langkah lain panjang log tidak berubah. Keluaran memperlihatkan status dan panjang log, bukan isi log follower.*

![Gambar 29. Keluaran simulasi Raft, langkah akhir.](Source%20Code/27_3_Output_Raft.png)

*Pembahasan 29: Bagian akhir menampilkan status node hingga langkah ke-20. Node 3 tetap tercatat sebagai leader, sedangkan Node 1 dan Node 2 berstatus follower; tiga perintah yang ditambahkan menghasilkan panjang log lokal Node 3 sebesar tiga. Follower tetap memiliki log kosong karena simulasi ini tidak menerapkan replikasi entri.*

Program juga memisahkan fungsi simulasi utama dari kelas node Raft ke dalam modul Python.

![Gambar 30. Program utama yang menggunakan modul Raft.](Source%20Code/28_Main_Raft.png)

*Pembahasan 30: Program utama mengimpor `RaftNode` dan `State` dari modul, lalu membuat tiga node dengan ID 1–3. Pemilihan leader dimulai secara eksplisit pada Node 1; di dalam loop 20 langkah, program memilih leader yang ditemukan, mengirim heartbeat kepada node lain, menambahkan perintah pada langkah genap, dan mencetak status, term, serta panjang log setiap node.*

![Gambar 31. Modul kelas dan status node Raft.](Source%20Code/29_Raft_Module.png)

*Pembahasan 31: Modul mendefinisikan enum status dan kelas `RaftNode` sehingga logika node terpisah dari program simulasi utama. Konstruktor mengatur keadaan awal dan timeout acak; metode heartbeat memperbarui keadaan follower, sedangkan metode pemilihan menaikkan term dan menetapkan leader menurut perhitungan suara sederhana. Metode `append_entry()` hanya menambahkan entri jika node adalah leader, dan `tick()` memeriksa timeout pemilihan.*

![Gambar 32. Keluaran program utama Raft, bagian awal.](Source%20Code/30_1_Output_Main_Raft.png)

*Pembahasan 32: Jalankan `main_raft.py` dari folder yang sama dengan `raft_module.py` agar modul dapat diimpor. Keluaran mengonfirmasi tiga node dibuat dan Node 1 dipilih sebagai leader pada term 1; pada langkah pertama, leader menambahkan `command-0`. Baris status berikutnya menunjukkan term dan panjang log leader serta dua follower setelah heartbeat dikirim.*

![Gambar 33. Keluaran program utama Raft, bagian tengah.](Source%20Code/30_2_Output_Main_Raft.png)

*Pembahasan 33: Lanjutkan mengamati langkah-langkah tengah. Node 1 tetap berstatus leader dan Node 2 serta Node 3 tetap follower pada term yang sama setelah menerima heartbeat. Setiap kali kondisi langkah genap terpenuhi, program menambahkan command ke log Node 1 sehingga panjang log bertambah satu; log kedua follower tetap nol.*

![Gambar 34. Keluaran program utama Raft, bagian akhir.](Source%20Code/30_3_Output_Main_Raft.png)

*Pembahasan 34: Pada bagian akhir loop, status ketiga node masih dicetak untuk setiap langkah. Setelah perintah ditambahkan pada langkah-langkah genap mulai dari indeks 0, log lokal Node 1 mencapai sepuluh entri; Node 2 dan Node 3 tetap memiliki log kosong. Perbedaan ini memperlihatkan bahwa contoh memodelkan penambahan log oleh leader, tetapi belum mengimplementasikan replikasi Raft ke follower.*

> **Batasan simulasi Raft:** Program ini merupakan demonstrasi konsep, bukan implementasi Raft lengkap. Suara node lain diasumsikan diberikan tanpa pertukaran pesan voting, heartbeat dan replikasi log follower belum benar-benar diimplementasikan, dan entri hanya ditambahkan ke log lokal leader. Karena itu, hasilnya tidak membuktikan konsensus atau toleransi kegagalan pada sistem nyata.

## Kesimpulan

Praktikum menunjukkan bahwa sinkronisasi waktu fisik melalui NTP berbeda dari pengurutan kausal melalui vector clock. Eksekusi thread secara konkuren dapat menimbulkan race condition bila data bersama tidak dilindungi; penggunaan lock pada bagian kritis menjaga saldo tetap konsisten. Pengambilan beberapa lock dengan urutan yang berlawanan dapat menyebabkan deadlock, sedangkan pelepasan lock sebelum menunggu lock lain membantu menghindari pola tunggu tersebut. Simulasi Raft memperkenalkan status node, term, pemilihan leader, heartbeat, dan log, tetapi penyederhanaan implementasinya perlu diperhatikan sebelum konsep tersebut diterapkan pada sistem terdistribusi nyata.