# README.md TK PBP C11

# Daftar Anggota Kelompok TK-PBP C11
- Dhea Anggrayningsih Syah Rony 2406437262 - Modul Review
- Gregorius Ega Aditama Sudjali 2406434153 - Modul Authentication
- kanayra maritza sanika adeeva 2406437880 - Modul Wishlist
- Kalfin Jefwin Setiawan Gultom 2406360256 - Modul Trainer Booking
- Fadhil Daffa Putra Irawan 2406438271 - Modul Places
- Marvel Irawan 2406421346 - Modul Search

## 1. Deskripsi Aplikasi 
🏋️‍♂️ FitMatrix
FitMatrix adalah aplikasi yang membantu khalayak untuk menemukan rekomendasi tempat olahraga 🏟️ di wilayah Jabodetabek, baik yang berbayar 💳 maupun gratis 🎉dan memungkinkan mereka untuk menyimpan tempat favorit sesuai preferensi mereka dari rekomendasi
yang ada ke dalam wishlist serta memberi review setelah merasakan pengalaman berolahraga langsung di tempat. Selain itu, FitMatrix juga membantu user untuk menemukan rekomendasi personal trainer/ coach dan membooking sesi bersama mereka.

👥 Jenis Pengguna
1. User(biasa) – ditargetkan pada sebagian besar Sport Enthusiast.
User ini ditargetkan pada sebagian besar Sport Enthusiast yang butuh referensi tempat yang bervariasi, baik yang berbayar maupun gratis. Mereka bisa memanfaatkan fitur-fitur di aplikasi kami:
- 🎯 Filter berdasarkan cabang olahraga
- 📍 Filter berdasarkan lokasi
- ⭐ Menyimpan tempat olahraga ke wishlist
- 👍 Melakukan review tempat olahraga
- 🔥 Mendapatkan rekomendsi Trending Coordinates
- 🤝 Melakukan booking appointment Personal trainer/Coach

2. Admin
Admin bertugas mengelola data di aplikasi:
- ➕ Menambah lokasi spot olahraga & personal trainer/coach di Jabodetabek
- ✏️ Mengedit dan menghapus data spot olahraga & trainer
- ❌ Cancel appointment PT/Coach

## 2. Daftar Modul / Fitur (sesuai diagram)

1.  Auth & Profile (Modul Autentikasi dan Profil Pengguna)
Fungsi: Modul ini mengelola registrasi, login, dan profil pengguna. Pengguna dapat mengelola data pribadi mereka, serta mengakses fitur-fitur lain seperti wishlist dan review.

Fitur Utama:
- Registrasi, login, dan pengelolaan akun.
- Mengelola profile pengguna (nama, foto profile, password)
- Menyimpan riwayat aktivitas pengguna (seperti appointment saat itu, histori appointments, wishlist, rating).

Integrasi: Terkoneksi dengan modul Wishlist, Review, dan Appointment.


2. Search (Modul Pencarian)
Fungsi: Menyediakan fitur pencarian untuk menemukan tempat olahraga berdasarkan kategori olahraga, lokasi, berbayar/gratis.

Fitur Utama:
- Pencarian berdasarkan kata kunci.
- Filter berdasarkan olahraga, lokasi, dan harga (berbayar atau gratis).
- Menyortir hasil pencarian berdasarkan likes terbanyak.
  
Integrasi: Terkoneksi dengan modul Place dan Hot Deals.


3. Place (Modul Tempat Olahraga)
Fungsi: Mengelola data tempat olahraga seperti gym, lapangan futsal, atau track lari, dan menampilkan rincian informasi tempat.

Fitur Utama:
- Menyimpan data tempat olahraga (lokasi, isFree(tempat ini berbayar atau gratis), fasilitas, deskripsi, harga jika berbayar).
- Menyediakan peta lokasi dan jam operasional (range waktu dari buka sampe tutup).
- Menampilkan tempat olahraga yang paling populer berdasarkan rating rata-rata dan likes terbanyak.
- Tempat dengan rating tertinggi dan likes terbanyak ditampilkan sebagai Hot Places.
- Filter berdasarkan rating dan menampilkan tempat populer.

Integrasi: Terkoneksi dengan Search, Wishlist, dan Review, Place, Search, dan Hot Deals.


4. Wishlist (Modul Daftar Favorit)
Fungsi: Mengizinkan pengguna untuk menyimpan tempat olahraga favorit mereka agar dapat dengan mudah diakses di kemudian hari.

Fitur Utama:
- Menyimpan dan menghapus tempat dari wishlist.
- Menampilkan daftar tempat yang telah disimpan oleh pengguna.
  
Integrasi: Terkoneksi dengan Place dan Auth & Profile.


5. Review (Modul Ulasan dan Rating)
Fungsi: Pengguna dapat memberikan rating dan review pada tempat olahraga yang mereka kunjungi untuk membantu pengguna lain dalam memilih tempat terbaik.

Fitur Utama:
- Memberikan rating (1-5) dan komentar untuk tempat olahraga.
- Menampilkan review dan rating dari pengguna lain.
- Admin dapat mengelola review yang tidak sesuai.

Integrasi: Terkoneksi dengan Place dan Auth & Profile.


6. Trainer Booking (Modul Pemesanan Trainer)

Fungsi:
Memungkinkan pengguna untuk melihat daftar trainer, melakukan booking sesi olahraga, dan mengelola jadwal sesi. Admin dapat memonitor dan mengatur booking serta jadwal trainer.

Fitur utama per role dalam modul Trainer Booking
A. User (Pengguna Biasa)
- Melihat daftar trainer beserta spesialisasi, rating, dan jadwal tersedia.
- Memilih tanggal, jam, durasi, dan jenis latihan untuk sesi training.
- Membuat, mengubah, atau membatalkan booking sesi mereka sendiri.
- Menyimpan riwayat booking (status: pending, selesai, dibatalkan).
- Memberikan review dan rating untuk trainer setelah sesi selesai.

B. Admin
- Melihat seluruh booking yang dibuat oleh user.
- Mengatur jadwal trainer (menambah slot baru, mengubah atau menonaktifkan slot).
- Membatalkan booking jika ada konflik atau masalah.
- Memantau dan mengelola review yang diberikan user.

Integrasi
Auth & Profile: untuk identifikasi pengguna dan akses sesuai role.
Review: untuk menampilkan dan mengelola rating/trainer feedback.
Place / Search: jika sesi dilakukan di lokasi tertentu (misal gym atau lapangan tertentu).



Link Figma: 
https://www.figma.com/design/vXSH1mwzy0O4ozmXNNKxCT/FitMatrix?node-id=0-1&t=0LneyTAaBzi1ylCE-1
password: olahega

Link deployment PWS:
https://fadhil-daffa-fitmatrix.pbp.cs.ui.ac.id/

Initial dataset: 
https://huggingface.co/datasets/Shiowo2/Initial-Data-FitMatrix
https://commons.wikimedia.org/w/index.php?search=lapangan+indonesia&title=Special%3AMediaSearch&type=image WikiMedia, keyword: lapangan Indonesia
https://commons.wikimedia.org/w/index.php?search=headshot&title=Special%3AMediaSearch&type=image WikiMedia, keyword: headshot (profile trainer)
