# LAPORAN PRAKTIKUM CLOUD COMPUTING
## Pengenalan XaaS dan Deployment Aplikasi Flask dengan Container

## 1. Tujuan Praktikum

1. Memahami perbedaan tanggung jawab pengguna dan penyedia pada model SaaS, PaaS, dan IaaS.
2. Mengidentifikasi contoh layanan dan service yang disediakan pada setiap model XaaS.
3. Menjalankan aplikasi Flask secara lokal menggunakan lingkungan Python terisolasi.
4. Membuat image dan menjalankan aplikasi Flask menggunakan Docker dan Podman.
5. Mengamati hubungan antara aplikasi, container, image, port, dan browser.

## 2. Dasar Teori

### 2.1 Cloud Computing dan XaaS

Cloud computing adalah penyediaan sumber daya komputasi melalui jaringan sesuai kebutuhan. Pengguna dapat memanfaatkan aplikasi, platform pengembangan, atau infrastruktur tanpa harus mengelola seluruh perangkat fisik sendiri. Sumber daya umumnya dapat diakses melalui internet, dikelola oleh penyedia, dan ditagihkan berdasarkan paket atau pemakaian.

XaaS (*Anything/Everything as a Service*) adalah istilah umum untuk layanan yang disediakan sebagai service. Tiga model yang dibahas dalam praktikum ini adalah:

| Model | Kepanjangan | Service utama | Tanggung jawab pengguna | Tanggung jawab penyedia |
|---|---|---|---|---|
| SaaS | *Software as a Service* | Aplikasi siap digunakan melalui web atau aplikasi klien | Menggunakan aplikasi dan mengelola konten/konfigurasi akun | Aplikasi, runtime, middleware, sistem operasi, virtualisasi, server, storage, dan jaringan |
| PaaS | *Platform as a Service* | Lingkungan untuk membangun, menjalankan, dan mengelola aplikasi | Aplikasi dan biasanya data serta konfigurasi aplikasinya | Runtime, middleware, sistem operasi, virtualisasi, server, storage, dan jaringan |
| IaaS | *Infrastructure as a Service* | Sumber daya komputasi virtual seperti mesin virtual, jaringan, dan storage | Sistem operasi, middleware, runtime, aplikasi, dan data | Perangkat fisik, virtualisasi, server, storage, dan jaringan |

Pembagian tersebut merupakan gambaran umum. Batas tanggung jawab dapat berbeda menurut produk, konfigurasi, dan layanan tambahan yang dipilih. Pada ketiga model, pengguna tetap bertanggung jawab menggunakan layanan dengan aman, termasuk mengatur akses dan melindungi data.

### 2.2 Contoh Vendor dan Service

Contoh berikut selaras dengan kategori pada Gambar 01.

| Kategori | Contoh vendor/layanan | Service yang diberikan |
|---|---|---|
| SaaS | Google Workspace | Aplikasi produktivitas siap pakai, seperti Gmail, Google Drive, Docs, Sheets, Meet, dan Calendar. Pengguna mengakses aplikasi dan mengelola dokumen tanpa mengelola server atau sistem operasi yang menjalankannya. |
| PaaS | Heroku | Platform untuk men-deploy dan menjalankan aplikasi. Pengembang mengirimkan kode serta konfigurasi aplikasi, sedangkan platform menyediakan lingkungan runtime dan mengelola infrastruktur dasar. |
| IaaS | Amazon Web Services (AWS) EC2 | Kapasitas komputasi berupa instance/mesin virtual yang dapat dikonfigurasi. Pengguna mengelola sistem operasi dan perangkat lunak di dalam instance; AWS mengelola infrastruktur fisik dan lapisan virtualisasinya. |

### 2.3 Arsitektur Umum XaaS

![Gambar 01. Pembagian tanggung jawab pada IaaS, PaaS, dan SaaS](images/01_Gambar%20arsitektur%20XaaS.jpeg)

*Gambar 01. Pembagian tanggung jawab pada IaaS, PaaS, dan SaaS.*

**Pembahasan:** Gambar memperlihatkan lapisan aplikasi dan infrastruktur serta pihak yang bertanggung jawab. Huruf **P** berarti pengguna/pelanggan, sedangkan **V** berarti vendor/penyedia. Urutan lapisan dari atas ke bawah adalah aplikasi, data, runtime, middleware, sistem operasi, virtualisasi, server, storage, dan jaringan. Pada IaaS, penyedia mengelola lapisan fisik dan virtualisasi; pelanggan mengelola sistem operasi sampai aplikasi. Pada PaaS, penyedia juga mengelola sistem operasi dan runtime/platform, sementara pelanggan berfokus pada aplikasi dan data. Pada SaaS, penyedia mengoperasikan hampir seluruh tumpukan layanan sehingga pengguna berinteraksi langsung dengan aplikasi.

Secara ringkas, alur layanan dapat dibayangkan sebagai berikut:

```text
Pengguna
   │ mengakses aplikasi / mengirim kode / mengelola mesin virtual
   ▼
Service cloud: SaaS          PaaS                 IaaS
             aplikasi siap   platform aplikasi   komputasi virtual
   ▼
Lapisan yang dikelola vendor: runtime, middleware, OS, virtualisasi,
                              server, storage, jaringan
   ▼
Infrastruktur pusat data penyedia cloud
```

Ilustrasi ini menyederhanakan pembagian pada Gambar 01: bagian infrastruktur fisik dan jaringan berada di bawah layanan cloud, sementara tingkat kendali pelanggan bertambah dari SaaS ke PaaS lalu IaaS.

### 2.4 Lingkungan Python dan Container

*Virtual environment* Python mengisolasi paket proyek agar tidak bercampur dengan paket sistem atau proyek lain. Pada praktikum, `uv venv` membuat lingkungan tersebut, kemudian `uv pip install -e .` memasang proyek dalam mode editable beserta dependensinya.

Container mengemas aplikasi dan dependensi ke dalam image agar aplikasi dapat dijalankan dalam lingkungan yang konsisten. Docker dan Podman sama-sama dapat membangun image dari Dockerfile serta menjalankan container. Port container perlu dipetakan ke port host agar aplikasi dapat diakses dari browser. Container bukan dengan sendirinya layanan cloud publik: praktik ini menjalankan container di mesin lokal, tetapi konsep pengemasan yang sama dapat menjadi bagian dari deployment cloud.

## 3. Langkah Kerja dan Pembahasan Gambar

### A. Menyiapkan dan Menjalankan Flask secara Lokal

#### Langkah 1 — Mengunduh source code

![Gambar 02. Mengkloning repositori Flask](images/02_git%20clone.png)

*Gambar 02. Mengkloning repositori Flask.*

**Pembahasan:** Perintah `git clone https://github.com/pallets/flask` mengambil source code Flask dari GitHub ke direktori lokal. Source code ini menjadi sumber contoh tutorial yang digunakan pada langkah berikutnya.

#### Langkah 2 — Menyalin aplikasi tutorial

![Gambar 03. Menyalin direktori tutorial](images/03_tutorial%20flask-app.png)

*Gambar 03. Menyalin direktori tutorial.*

**Pembahasan:** Perintah `cp -R` menyalin direktori `examples/tutorial` menjadi `flask-app`, kemudian terminal berpindah ke direktori tersebut. Dengan demikian, percobaan dilakukan pada salinan tutorial, bukan dengan mengubah direktori sumber Flask.

#### Langkah 3 — Memeriksa isi proyek

![Gambar 04. Memeriksa file dan direktori proyek](images/04_ls%20-la.png)

*Gambar 04. Memeriksa file dan direktori proyek.*

**Pembahasan:** Perintah `ls -la` menampilkan file tersembunyi dan isi proyek. Terlihat file konfigurasi proyek, direktori `flaskr`, `instance`, `tests`, dan `.venv`. Pemeriksaan ini memastikan terminal berada pada direktori aplikasi yang benar sebelum instalasi dan eksekusi.

#### Langkah 4 — Membuat virtual environment

![Gambar 05. Membuat virtual environment dengan uv](images/05_Pembuatan%20uv%20venv%20.png)

*Gambar 05. Membuat virtual environment dengan uv.*

**Pembahasan:** Perintah `uv venv --python 3.14.4` membuat lingkungan virtual `.venv` menggunakan interpreter Python 3.14.4. Terminal juga menampilkan perintah aktivasi yang dapat digunakan.

#### Langkah 5 — Mengaktifkan virtual environment

![Gambar 06. Mengaktifkan virtual environment](images/06_Mengaktifkan%20uv%20venv.png)

*Gambar 06. Mengaktifkan virtual environment.*

**Pembahasan:** Perintah `source .venv/bin/activate` mengaktifkan lingkungan virtual pada shell Linux. Penanda `(flask-app)` di prompt menunjukkan lingkungan aktif. Perintah ini khusus untuk shell Unix/Linux; pada Windows, cara aktivasi berbeda.

#### Langkah 6 — Memasang dependensi proyek

![Gambar 07. Memasang proyek dalam mode editable](images/07_uv%20pip%20install%20-e%20.png)

*Gambar 07. Memasang proyek dalam mode editable.*

**Pembahasan:** Perintah `uv pip install -e .` memasang proyek dari direktori saat ini dalam mode editable. Output memperlihatkan Flask dan dependensi seperti Werkzeug, Jinja, dan Click berhasil dipasang pada lingkungan proyek.

#### Langkah 7 — Menginisialisasi database

![Gambar 08. Menginisialisasi database Flaskr](images/08_flask%20--app%20flaskr%20run.png)

*Gambar 08. Menginisialisasi database Flaskr.*

**Pembahasan:** Perintah `flask --app flaskr init-db` menyiapkan database awal untuk aplikasi tutorial Flaskr. Inisialisasi dilakukan sebelum server dijalankan agar aplikasi memiliki struktur database yang diperlukan.

#### Langkah 8 — Menjalankan server Flask lokal

![Gambar 09. Menjalankan server Flask](images/09_Flask%20run.png)

*Gambar 09. Menjalankan server Flask.*

**Pembahasan:** Perintah `flask --app flaskr run` menjalankan server pengembangan Flask pada `127.0.0.1:5000`. Log menunjukkan permintaan halaman utama dan stylesheet mendapat respons HTTP 200. Permintaan favicon mendapat 404; ini tidak menghalangi halaman utama tampil, tetapi menunjukkan berkas favicon tidak tersedia. Flask juga memperingatkan bahwa server bawaan ini ditujukan untuk pengembangan, bukan produksi.

#### Langkah 9 — Memeriksa aplikasi di browser

![Gambar 10. Aplikasi Flaskr pada browser lokal](images/10_Cek%20Browser.png)

*Gambar 10. Aplikasi Flaskr pada browser lokal.*

**Pembahasan:** Browser membuka `localhost:5000` dan menampilkan halaman Flaskr. Terlihat navigasi **Register** dan **Log In** serta bagian **Posts**. Tampilan ini memverifikasi bahwa server lokal dapat diakses melalui browser.

### B. Membangun dan Menjalankan dengan Docker

#### Langkah 10 — Membuat Dockerfile

![Gambar 11. Isi Dockerfile aplikasi](images/11_Buat%20Dockerfile.png)

*Gambar 11. Isi Dockerfile aplikasi.*

**Pembahasan:** Dockerfile menggunakan image dasar `python:3.14`, menyalin berkas proyek ke `/app`, memasang proyek, menginisialisasi database, mendeklarasikan port 5000, lalu menjalankan Flask pada `0.0.0.0:5000`. Opsi `0.0.0.0` membuat server dapat menerima koneksi yang diteruskan ke container, bukan hanya koneksi loopback container.

#### Langkah 11 — Membangun image Docker

![Gambar 12. Proses build image Docker](images/12_docker%20build%20-f%20Dockerfile%20-t%20flaskr.png)

*Gambar 12. Proses build image Docker.*

**Pembahasan:** Perintah `docker build -f Dockerfile -t flaskr:1.0.0 .` membangun image dari Dockerfile dan memberi nama/tag `flaskr:1.0.0`. Output menunjukkan tahap-tahap build selesai, termasuk instalasi dependensi dan inisialisasi database.

#### Langkah 12 — Memeriksa image Docker

![Gambar 13. Daftar image lokal Docker](images/13_docker%20image%20ls.png)

*Gambar 13. Daftar image lokal Docker.*

**Pembahasan:** Perintah `docker image ls` menampilkan image yang tersedia secara lokal, termasuk `flaskr:1.0.0`. Daftar juga berisi image lain pada mesin; image-image tersebut bukan bagian dari aplikasi Flaskr.

#### Langkah 13 — Menghapus image yang tidak digunakan

![Gambar 14. Menghapus image Docker tertentu](images/14_docker%20rmi.png)

*Gambar 14. Menghapus image Docker tertentu.*

**Pembahasan:** Perintah `docker rmi` menghapus image berdasarkan ID yang ditentukan. Pada screenshot, yang dihapus adalah image `docker/welcome-to-docker` dan `postgres`, bukan image `flaskr`. Penghapusan image dapat gagal jika masih digunakan container; periksa nama/ID dan dampaknya sebelum menjalankan perintah serupa.

#### Langkah 14 — Menjalankan container Docker dan memetakan port

![Gambar 15. Menjalankan container dengan port mapping](images/15_docker%20run%20-p.png)

*Gambar 15. Menjalankan container dengan port mapping.*

**Pembahasan:** Perintah `docker run -p 5001:5000 flaskr:1.0.0` menjalankan container dari image Flaskr. Pemetaan tersebut menghubungkan port 5001 pada host ke port 5000 di container. Log menunjukkan Flask berjalan pada semua alamat container.

#### Langkah 15 — Memeriksa aplikasi Docker

![Gambar 16. Aplikasi yang berjalan melalui Docker](images/16_Cek%20Browser.png)

*Gambar 16. Aplikasi yang berjalan melalui Docker.*

**Pembahasan:** Browser membuka `localhost:5001`, yaitu port host yang dipetakan pada langkah sebelumnya. Halaman menampilkan Flaskr dalam keadaan pengguna sudah masuk dan sebuah postingan; ini memverifikasi jalur browser → port host → container → aplikasi.

#### Langkah 16 — Membersihkan container yang berhenti

![Gambar 17. Membersihkan container Docker yang berhenti](images/17_Docker%20Container.png)

*Gambar 17. Membersihkan container Docker yang berhenti.*

**Pembahasan:** Perintah `docker container prune` menghapus **semua container yang sedang berhenti** dan meminta konfirmasi. Output menyatakan ruang yang berhasil dibebaskan. Ini merupakan langkah pembersihan opsional, bukan syarat menjalankan Flaskr; periksa container yang akan terdampak sebelum menyetujui karena container berhenti lain di mesin juga dapat terhapus.

### C. Membangun dan Menjalankan dengan Podman

#### Langkah 17 — Memulai build image Podman

![Gambar 18. Proses awal build image dengan Podman](images/18_Podman%20build%20-f%20Dockerfile%20-t%20flaskr.png)

*Gambar 18. Proses awal build image dengan Podman.*

**Pembahasan:** Perintah `podman build -f Dockerfile -t flaskr:1.0.0 .` menggunakan Dockerfile yang sama untuk membangun image dengan Podman. Output menunjukkan Podman mengambil image dasar Python. Peringatan bahwa direktori bukan shared mount berkaitan dengan konfigurasi lingkungan container rootless; proses build tetap berlanjut pada screenshot.

#### Langkah 18 — Menyelesaikan build image Podman

![Gambar 19. Penyelesaian build image Podman](images/19_Podman%20build%20-f%20Dockerfile%20-t%20flaskr.png)

*Gambar 19. Penyelesaian build image Podman.*

**Pembahasan:** Bagian ini melanjutkan output build dari Gambar 18. Dependensi Flaskr berhasil dipasang, database diinisialisasi, dan image diberi tag `localhost/flaskr:1.0.0`. Ini menunjukkan Dockerfile dapat digunakan oleh Podman untuk menghasilkan image aplikasi.

#### Langkah 19 — Memeriksa image Podman

![Gambar 20. Daftar image lokal Podman](images/20_Podman%20Image.png)

*Gambar 20. Daftar image lokal Podman.*

**Pembahasan:** Perintah `podman image ls` menampilkan image `localhost/flaskr:1.0.0` dan image dasar `python:3.14`. Daftar ini mengonfirmasi image hasil build tersimpan di penyimpanan image Podman.

#### Langkah 20 — Menjalankan container Podman

![Gambar 21. Menjalankan Flaskr dengan Podman](images/21_podman%20run%20--network%20slirp4netns%20-p.png)

*Gambar 21. Menjalankan Flaskr dengan Podman.*

**Pembahasan:** Perintah `podman run -p 5001:5000 flaskr:1.0.0` menjalankan aplikasi dan memetakan port host 5001 ke port 5000 container. Opsi `--network slirp4netns` menggunakan jaringan rootless yang ditentukan pada praktikum. Log menunjukkan aplikasi siap menerima koneksi.

#### Langkah 21 — Memeriksa aplikasi Podman

![Gambar 22. Aplikasi Flaskr yang berjalan melalui Podman](images/22_Tes%20Browser.png)

*Gambar 22. Aplikasi Flaskr yang berjalan melalui Podman.*

**Pembahasan:** Browser membuka `localhost:5001` dan menampilkan aplikasi Flaskr beserta postingan. Hasil ini memverifikasi bahwa container hasil build Podman dapat diakses melalui pemetaan port. Data/tampilan aplikasi pada container ini tidak harus sama dengan sesi Docker sebelumnya, karena masing-masing container dapat menggunakan lingkungan dan data yang berbeda.

## 4. Kesimpulan

Praktikum memperkenalkan model layanan SaaS, PaaS, dan IaaS serta pembagian tanggung jawab antara pengguna dan vendor. Google Workspace, Heroku, dan AWS EC2 masing-masing menjadi contoh SaaS, PaaS, dan IaaS dengan tingkat pengelolaan pelanggan yang berbeda. Melalui tutorial Flaskr, aplikasi berhasil dijalankan secara lokal, kemudian dikemas menjadi image dan dijalankan menggunakan Docker maupun Podman. Hasil browser dan pemetaan port membuktikan aplikasi di dalam container dapat diakses dari host. Container meningkatkan portabilitas aplikasi, sementara pemilihan model XaaS menentukan seberapa banyak infrastruktur yang dikelola penyedia dibandingkan pengguna.
