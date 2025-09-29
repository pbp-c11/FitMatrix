# README.md TK PBP C11

# Daftar Anggota Kelompok TK-PBP C11
List Nama:
- Dhea Anggrayningsih Syah Rony 2406437262
- Gregorius Ega Aditama Sudjali 2406434153
- kanayra maritza sanika adeeva 2406437880
- Kalfin Jefwin Setiawan Gultom 2406360256
- Fadhil Daffa Putra Irawan 2406438271
- Marvel Irawan 2406421346

## 1. Deskripsi Aplikasi dan jenis pengguna
Deskripsi Aplikasi: platform yang membantu pengguna menemukan rekomendasi tempat olahraga, baik yang berbayar maupun gratis (misalnya track lari, gym, atau lapangan olahraga) di wilayah Jabodetabek. Pengguna dapat memfilter tempat berdasarkan cabang olahraga dan lokasi, menyimpan tempat favorit ke wishlist, serta melihat tempat populer (Hot Places) dan promosi (Hot Deals). Tujuan aplikasi ini adalah mempermudah masyarakat untuk menemukan sarana olahraga sesuai kebutuhan dan preferensi mereka. 

Jenis pengguna: User – ditargetkan pada sebagian besar Sport Enthusiast.
User ini adalah individu yang tertarik dengan aktivitas olahraga dan ingin menemukan tempat olahraga di sekitar wilayah mereka. Mereka butuh referensi tempat yang bervariasi, baik yang berbayar maupun gratis, serta memanfaatkan fitur-fitur berikut untuk memilih lokasi olahraga yang sesuai dengan preferensi mereka:
- Filter berdasarkan cabang olahraga dan lokasi
- Menyimpan tempat favorit ke wishlist
- Memberikan review dan likes pada tempat olahraga
- Melihat tempat populer (Hot Places) dan promosi (Hot Deals)


## 2. Daftar Modul / Fitur (sesuai diagram)

### A. Browsing & Discovery

* **All Places**: daftar semua tempat (pagination).
* **Filter & Sort**
  Filter: `sport`, `region` (+ `area` opsional), `is_paid` (Free/Paid).
  Sort: terbaru / **likes terbanyak**.
* **Hot Places**: `Place.get_hot_places()` (annotate `likes_count`, order by `-likes_count`).
* **Hot Deals** (berbayar): daftar promo aktif di beranda (lihat `HotDeal.get_active_deals()`).

### B. Interaksi Pengguna (Login Required)

* **Likes**: relasi **ManyToMany** `Place <-> UserProfile`. Satu like per user per place.
  Helper: `user.has_liked(place)`.
* **Wishlist**: model penghubung `WishlistItem(user, place)`
  Helper: `user.get_wishlist_items()`, `WishlistItem.add_to_wishlist()`, `remove_from_wishlist()`.
* **Reviews**: `Review(user, place, rating 1–5, comment)`
  Helper: `Review.submit_review(form_data)`.

### C. Presentasi Data

* **Place Card**: `name`, `sport`, `location (region/area)`, **likes_count**, `price` (atau **Free**), `description`.

> ✅ **Acceptance Checklist*
>
> * [ ] Filter sport/region & sorting berjalan
> * [ ] Hot Places & Hot Deals tampil di Home
> * [ ] Like unik per user; counter tampil sebagai `likes_count`
> * [ ] Review CRUD (user hanya bisa ubah/hapus miliknya)
> * [ ] Wishlist page milik user

## 3. Initial Dataset (Seed)

> Simpan file di `/seed`. Untuk **likes** gunakan array `liked_by` (list user id); di runtime hitung `likes_count = len(liked_by)`.

### 3.1 Skema Ringkas (mengikuti diagram)

* **UserProfile**

  * `user` (OneToOne → Django User)
  * `location_preference` (choices: `Jakarta|Bogor|Depok|Tangerang|Bekasi`, blank=True)
  * `preferred_sports` (ArrayField/String list; contoh: `["Lari","Gym"]`, blank=True)
  * `created_at`, `updated_at` (timestamps)

* **Place**

  * `id` (AutoField, pk)
  * `name` (str, max 255, indexed)
  * `location.region` (choice: J/B/D/T/B, indexed)
  * `area` (str, optional)
  * `category` / `sport` (choice: `Running|Futsal|Basketball|Swimming|Badminton|Gym|Others`)
  * `is_paid` (bool), `price_min`, `price_max` (Decimal | null)
  * `description` (Text)
  * `image_url` (URLField/ImageField, optional)
  * `likes` (M2M → UserProfile, related name `liked_places`)
  * **Class/Query helpers**: `get_likes_count()`, `filter_by_location()`, `filter_by_category()`, `get_hot_places()`

* **WishlistItem**

  * `id` (AutoField)
  * `user` (FK → UserProfile, `related_name="wishlist_items"`)
  * `place` (FK → Place, `related_name="wishlisted_by"`)
  * `added_at` (DateTime)

* **Review**

  * `id` (AutoField)
  * `user` (FK → UserProfile)
  * `place` (FK → Place, `related_name="reviews"`)
  * `rating` (Integer 1..5, choices)
  * `comment` (Text)
  * `created_at` (DateTime)

* **HotDeal**

  * `id` (AutoField)
  * `place` (FK → Place, hanya untuk `is_paid=True`, `related_name="deals"`)



