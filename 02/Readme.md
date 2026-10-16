# Laporan Praktikum: Pengelolaan Python dengan `uv` dan GraphQL

## 1. Tujuan

Praktikum ini membahas pengelolaan Python menggunakan `uv`, mulai dari instalasi, pemilihan versi Python, pembuatan lingkungan virtual, hingga pemasangan paket. Lingkungan tersebut kemudian digunakan untuk membuat server GraphQL sederhana dengan Strawberry, menjalankan query melalui GraphiQL, dan menguji query menggunakan program klien Python. Screenshot Task Manager dan pengelolaan proses Steam juga dijelaskan sebagai kegiatan tambahan.

## 2. Pembahasan Screenshot

### 2.1 Mengelola proses melalui Task Manager

Task Manager menampilkan beberapa proses Visual Studio Code yang sedang berjalan. Menu konteks pada grup Visual Studio Code menyediakan opsi **End task** untuk menghentikan aplikasi. Opsi ini dapat digunakan jika aplikasi tidak merespons, tetapi pekerjaan yang belum disimpan dapat hilang.

![01.1 - Menu proses Visual Studio Code di Task Manager](./images/01-01-task-manager-end-vscode-task.png)

Sebelum proses dihentikan, penggunaan memori pada screenshot berada di sekitar 95%. Task Manager membantu mengidentifikasi aplikasi yang menggunakan sumber daya sistem.

![01.2 - Penggunaan sumber daya sebelum Visual Studio Code ditutup](./images/01-02-task-manager-vscode-resource-usage.png)

Setelah Visual Studio Code ditutup, aplikasi tersebut tidak lagi terlihat pada daftar aplikasi dan penggunaan memori pada screenshot turun menjadi sekitar 78%. Angka penggunaan dapat berubah sesuai kondisi komputer.

![01.3 - Task Manager setelah Visual Studio Code ditutup](./images/01-03-task-manager-after-vscode-closed.png)

![01.2 - Perintah PowerShell untuk memulai ulang Steam](./images/04-01-steam-restart-command.png)

Screenshot kedua memperlihatkan rangkaian perintah yang sama dalam tampilan terminal yang berbeda.

![01.3 - Rangkaian penghentian dan pembukaan kembali Steam](./images/04-02-steam-restart-sequence.png)

### 2.2 Memasang dan menyiapkan Python dengan `uv`

#### 2.2.1 Memasang dan memeriksa `uv`

Skrip instalasi dijalankan melalui PowerShell. Output menunjukkan bahwa program `uv`, `uvx`, dan `uvw` telah dipasang ke direktori lokal pengguna.

![02.1 - Memasang uv pada Windows melalui PowerShell](./images/02-01-install-uv-windows.png)

Perintah `uv --version` memastikan bahwa `uv` dapat ditemukan dan dijalankan dari terminal. Screenshot menampilkan versi `0.13.1` untuk Windows 64-bit.

![02.2 - Memeriksa versi uv](./images/02-02-check-uv-version.png)

Perintah `uv self update` memeriksa pembaruan program. Pesan hasil pada screenshot menyatakan versi `0.13.1` sudah merupakan versi terbaru saat pemeriksaan.

![02.3 - Memeriksa pembaruan uv](./images/02-03-update-uv.png)

#### 2.2.2 Menyiapkan direktori proyek dan versi Python

Perintah `uv python list` menampilkan versi Python yang dapat dikelola oleh `uv` dan instalasi yang sudah ditemukan di komputer. Versi yang bertanda `<download available>` dapat diunduh apabila dibutuhkan.

![02.4 - Melihat versi Python yang tersedia](./images/02-04-list-python-versions.png)

Perintah `mkdir workspace-01` membuat folder proyek. Pastikan folder tersebut belum ada sebelum menjalankan perintah yang sama kembali.

![02.5 - Membuat folder workspace-01](./images/02-05-create-workspace-folder.png)

Perintah `cd workspace-01` berpindah ke folder proyek. Prompt PowerShell menunjukkan direktori aktif setelah perpindahan.

![02.6 - Berpindah ke folder workspace-01](./images/02-06-change-to-workspace-folder.png)

Perintah `uv python pin cpython-3.14.5-windows-x86_64-none` menetapkan CPython 3.14.5 sebagai versi proyek. Screenshot menunjukkan proses pengunduhan interpreter untuk Windows 64-bit.

![02.7 - Mengunduh dan menetapkan versi Python proyek](./images/02-07-pin-python-version.png)

Screenshot ini menunjukkan percobaan menggunakan path `/home/bdpd/.local/bin/python3.14`, yang merupakan format path Linux. Terminal memperingatkan bahwa interpreter tidak ditemukan. Pada Windows, gunakan versi Python yang tersedia melalui `uv python list` atau path interpreter Windows yang sesuai.

![02.8 - Peringatan path interpreter Linux di Windows](./images/02-08-interpreter-path-warning.png)

#### 2.2.3 Membuat lingkungan virtual dan memasang paket

Perintah `uv venv` membuat lingkungan virtual pada folder `.venv`. Screenshot melaporkan penggunaan Python 3.14.8. Karena langkah sebelumnya mencoba menetapkan Python 3.14.5, periksa kembali versi yang digunakan lingkungan virtual agar sesuai dengan versi proyek yang diinginkan.

![02.9 - Membuat lingkungan virtual](./images/02-09-create-virtual-environment.png)

Perintah `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` mengubah kebijakan eksekusi PowerShell untuk akun saat ini. Pengaturan ini memungkinkan skrip aktivasi lokal dijalankan. Ubah kebijakan hanya jika diperlukan dan pahami cakupannya.

![02.10 - Mengatur kebijakan eksekusi PowerShell](./images/02-10-set-powershell-execution-policy.png)

Perintah `uv pip install pandas` memasang paket `pandas` beserta dependensinya. Screenshot menunjukkan `pandas`, `numpy`, `python-dateutil`, `six`, dan `tzdata` berhasil dipasang. Jalankan perintah saat lingkungan proyek yang dimaksud sudah aktif agar paket terpasang di lingkungan yang tepat.

![02.11 - Memasang pandas dan dependensinya](./images/02-11-install-pandas.png)

### 2.3 Membuat dan menjalankan server Strawberry GraphQL

#### 2.3.1 Memasang paket Strawberry GraphQL

Paket Strawberry GraphQL beserta fitur CLI dipasang dengan perintah berikut:

```powershell
uv pip install "strawberry-graphql[cli]"
```

Tanda kutip membantu PowerShell meneruskan bagian `[cli]` sebagai bagian dari nama paket. Output menunjukkan `uv` menyelesaikan dependensi dan memasang Strawberry GraphQL beserta paket pendukungnya.

![03.1 - Memasang Strawberry GraphQL dan dependensi CLI](./images/03-01-install-strawberry-graphql-cli.png)

Perintah `uv pip install strawberry-graphql[cli]` pada screenshot lain menunjukkan pemeriksaan paket selesai. Hasil ini melengkapi bukti pemasangan paket dan fitur CLI di lingkungan yang sedang digunakan.

![03.2 - Memeriksa paket Strawberry GraphQL](./images/03-02-verify-strawberry-package.png)

#### 2.3.2 Tugas 1: Membuat schema GraphQL

Buat file `schema.py` menggunakan Strawberry dengan ketentuan berikut:

1. Definisikan tipe GraphQL `Book` dengan field `title` dan `author`, keduanya bertipe teks.
2. Buat tipe `Query` yang menyediakan field `books` dan mengembalikan daftar objek `Book`.
3. Isi daftar dengan data buku contoh *The Great Gatsby* karya F. Scott Fitzgerald.
4. Buat schema Strawberry dengan `Query` sebagai root query.

**Hasil yang diharapkan:** schema dapat digunakan oleh server Strawberry dan menyediakan query `books` dengan informasi judul serta penulis.

![Tugas 1 - Membuat tipe Book, query books, dan schema GraphQL](./images/03-03-define-graphql-schema.png)

#### 2.3.3 Menjalankan server dan mencoba GraphiQL

Perintah pada screenshot mengaktifkan `.venv` lalu menjalankan `strawberry dev schema`. Server melaporkan alamat `http://0.0.0.0:8000/graphql`. Untuk mengaksesnya dari komputer yang sama, buka `http://127.0.0.1:8000/graphql` di browser.

![03.4 - Mengaktifkan lingkungan dan menjalankan server Strawberry](./images/03-04-run-strawberry-dev-server.png)

GraphiQL adalah antarmuka di browser untuk menulis, memvalidasi, dan mencoba query GraphQL. Screenshot berikut menunjukkan tampilan pengenalan editor GraphiQL.

![03.5 - Tampilan editor GraphiQL](./images/03-05-graphiql-query-editor.png)

Query berikut meminta field `title` dan `author` dari setiap item pada `books`:

```graphql
{
  books {
    title
    author
  }
}
```

Hasil pada GraphiQL menampilkan objek buku dengan judul *The Great Gatsby* dan penulis F. Scott Fitzgerald. Ini membuktikan query dapat membaca data yang disediakan schema.

![03.6 - Hasil query books di GraphiQL](./images/03-06-graphiql-query-result.png)

#### 2.3.4 Tugas 2: Membuat klien Python untuk menguji GraphQL

Buat file `client.py` untuk mengirim query GraphQL ke server Strawberry yang sedang berjalan. Klien harus meminta field `title` dan `author` dari query `books`, mengirim permintaan ke endpoint GraphQL lokal, lalu menampilkan data buku yang diterima dengan format yang mudah dibaca.

Jalankan server terlebih dahulu, pastikan lingkungan virtual aktif, kemudian uji klien dari terminal:

```powershell
py client.py
```

**Hasil yang diharapkan:** terminal menampilkan data dari server GraphQL, termasuk judul *The Great Gatsby* dan penulis F. Scott Fitzgerald. Hasil tersebut seharusnya sesuai dengan query yang dicoba melalui GraphiQL.

![Tugas 2 - Menjalankan klien Python dan menampilkan data dari server GraphQL](./images/03-07-run-python-graphql-client.png)

### 2.4 Menghentikan dan membuka kembali Steam

Kedua screenshot berikut menunjukkan kegiatan tambahan yang tidak terkait langsung dengan Python. Perintah `Get-Process steam* -ErrorAction SilentlyContinue | Stop-Process -Force` menghentikan proses Steam yang ditemukan. `Start-Sleep -Seconds 3` memberi jeda sebelum `Start-Process "steam://open/main"` meminta Steam membuka halaman utama kembali.

## 3. Kesimpulan

`uv` membantu memasang dan memeriksa Python, mengelola versi proyek, membuat lingkungan virtual, dan memasang dependensi. Setelah lingkungan siap, Strawberry GraphQL dapat digunakan untuk mendefinisikan schema, menjalankan server, dan menguji query melalui GraphiQL maupun klien Python. Pastikan interpreter yang dipakai sesuai sistem operasi serta lingkungan virtual yang aktif adalah lingkungan proyek yang benar.
