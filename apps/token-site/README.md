# POLITIK RIUH — Situs Peluncuran Token (Fase 1)

HTML/CSS/JS statis murni. **Tanpa dependensi**: tanpa package manager, tanpa build step, tanpa webfont, tanpa permintaan eksternal saat runtime. Hanya system font stack.

**Identitas:** POLITIK RIUH mempersembahkan **REFORMASI** — nama token REFORMASI sudah disetujui founder (issue #1, 2026-11-09); simbol yang diusulkan REFORMASI menunggu pemeriksaan kompatibilitas teknis. Seluruh salinan peserta berbahasa Indonesia (`lang="id"`).

## File

| File | Isinya |
|---|---|
| `index.html` | `/` — landing: identitas, status, token sekilas, pilar, pratinjau transparansi, pengungkapan risiko |
| `about.html` | Tujuan, posisi independen, risiko dan batasan |
| `token.html` | Gambaran token dan tabel fakta |
| `launch.html` | Status peluncuran ("Belum diluncurkan"), lima gate mainnet, dan penjelasan whitelist |
| `transparency.html` | Pengungkapan alokasi / treasury / dompet (semuanya belum tersedia) |
| `roadmap.html` | Milestone dengan label status yang didukung bukti repositori |
| `styles.css` | Sistem desain bersama (lihat di bawah) |
| `main.js` | Satu perilaku saja: toggle navigasi mobile (progressive enhancement) |
| `checks.sh` | Checks lokal yang dapat direproduksi (rute, HTML, salinan, JS, kontras) |
| `screenshots.sh` | Refresh screenshot dengan headless Chrome |
| `nav-toggle-test.py` | Uji fungsional toggle navigasi via Chrome DevTools Protocol (stdlib saja) |
| `evidence/` | Screenshot dari checks di bawah |

## Sistem desain

Basis nyaris-hitam `#0A0A0B`, permukaan `#121214`, border tipis `#26262A`, aksen merah secukupnya `#E5484D` (tombol utama memakai `#C93338` yang lebih gelap agar teks putih lolos WCAG AA), teks abu-abu redup `#9A9AA0`, micro-label monospace, headline editorial yang kuat, glow ambient secukupnya. HTML semantik, navigasi keyboard, fokus yang terlihat, dukungan `prefers-reduced-motion`. Responsive-first; mobile adalah layout utama.

## Setup lokal

```sh
cd apps/token-site
python3 -m http.server 8000 --bind 127.0.0.1
# buka http://127.0.0.1:8000/index.html
```

Tanpa build, tanpa install, tanpa environment variable.

## Checks yang dijalankan (2026-11-09, lokal, PR-013)

Perintah yang dapat direproduksi:

```sh
cd apps/token-site
bash checks.sh            # exit 0 = semua checks lolos
bash screenshots.sh       # exit 0 = semua screenshot ter-refresh
python3 nav-toggle-test.py  # exit 0 = toggle navigasi berfungsi
```

| Check | Hasil |
|---|---|
| Route smoke test (`curl`, server lokal) | **8/8 HTTP 200 + konten yang diharapkan per route**: `index/about/token/launch/transparency/roadmap.html`, `styles.css`, `main.js` — server memakai port dinamis yang dialokasikan bebas, readiness polling 15 detik, dan PID server terverifikasi memiliki listener (bukan port tetap 8000) |
| HTML parse (python `html.parser`) | **6/6 halaman, tanpa error**; `lang="id"`; tepat satu `<h1>` per halaman; landmark `header/nav/main/footer` di setiap halaman; tanpa ID duplikat |
| Tautan internal | Semua target `href`/`src` resolve di disk (diperiksa per halaman) |
| Disiplin salinan | Tanpa nama kandidat lama (NENGOK/GORENG/DER); tanpa sisa salinan Inggris yang menghadap peserta; identitas REFORMASI ada; status "Belum diluncurkan" ada; `launch.html` menyatakan whitelist belum dibuka |
| Regresi negatif (PR-013) | **Tidak ada**: tanpa elemen `.wallet-status` / frasa "Koneksi baca-saja direncanakan", tanpa nama personal founder di salinan publik, tanpa estimasi "0,02 SOL", tanpa klaim newsroom present-tense, Gate 01 hanya "Nama token disetujui" |
| Form / fetch / storage / dompet | **Tidak ada**: tanpa `<form>`, `fetch()`/XHR, `localStorage`, kode wallet/signing, atau pola secret di source situs |
| Sintaks JS | `node --check main.js` — lolos |
| Kontras (spot-check lima pasangan palet) | Teks redup di bg **7,07:1**; headline **18,96:1**; aksen merah di bg **5,06:1**; tombol utama putih di `#C93338` **5,23:1**; hover **5,79:1** — lima pasangan yang diuji lolos AA untuk teks normal (4,5:1); ini bukan audit semua kombinasi warna halaman |
| Uji fungsional nav toggle (headless Chrome via CDP, lebar 390px) | GitHub Actions run #42547368159 pada head PR #4 `873ca5685803211a6324d75764a392c12ae94708`: **3/3** run berhasil; `NAV-OPEN=true ARIA=true LABEL=Tutup menu`; port HTTP + CDP dinamis, PID listener terverifikasi, profil Chrome unik per run. |
| Screenshot (headless Chrome 157) | **12/12** desktop + mobile berhasil dibuat dan dimensi PNG divalidasi pada run #42547368159; visual spot-check independen: landing mobile, launch mobile, About mobile, dan roadmap desktop tampil tanpa overflow yang tampak. Screenshot adalah render lokal, bukan bukti deployment. |
| Validasi PR (GitHub Actions, non-deploy) | Workflow `.github/workflows/token-site-pr.yml` merged to `main` via PR #6 (`a480bb4`) and path filter corrected via PR #7 (`81463aff`): PRs/pushes run only when `apps/token-site/**` changes; workflow-only PRs are intentionally skipped. Run #42547368159 at earlier PR #4 head `873ca568` completed **success** (checks, nav 3/3, screenshots 12/12). PR #6 bootstrap run #42547411041 failed only because its workflow-only branch had no site files; the trigger filter was corrected in PR #7. A fresh run is required for the latest PR #4 head before acceptance. No deploy, Pages, secrets, wallet, or `apps/web/`. |
| Sidecar bukti | `evidence/SHA256SUMS.txt` — hash SHA-256 untuk 12 screenshot, 3 log run, dan 3 script checks |

### Koreksi dari screenshot dan checks PR-013

1. **Angka kontras tombol utama di README Fase 1 salah hitung.** Nilai yang tercatat (5,01:1 dan 5,55:1) tidak cocok dengan perhitungan ulang dari palet CSS; nilai yang benar adalah **5,23:1** dan **5,79:1** (keduanya tetap lolos AA). Tabel di atas memakai nilai yang sudah dikoreksi; `checks.sh` menghitung ulang rasio ini setiap kali dijalankan.
2. **Pola pemindai secret `sk-` sempat false positive** pada `risk-heading` (mengandung substring `sk-`). Pola diperketat menjadi `sk-` + 20+ karakter alfanumerik di `checks.sh`.
3. **Uji nav-toggle sempat false fail (timeout CDP) di 2026-11-09.** Penyebab: `ws_recv_msg` membuang sisa byte dalam satu segmen TCP ketika Chrome menggabungkan beberapa frame WebSocket (event + respons) — frame respons yang sudah tiba ikut terbuang, lalu recv berikutnya menunggu sampai timeout. Diperbaiki: sisa byte disimpan antar panggilan (juga untuk handshake). Uji kini lolos 3/3 run berurutan.

### Bug yang ditemukan screenshot dan diperbaiki (Fase 1)

1. **Hero terdorong ke bawah ~480px (desktop + mobile).** Penyebab: `.hero > * { position: relative; }` mengalahkan `position: absolute` milik `.glow`, sehingga glow memakan ruang flow. Diperbaiki menjadi `.hero > .wrap`.
2. **Pill status dompet meluber dari viewport di mobile.** Penyebab: `white-space: nowrap` pada pill 44 karakter. Diperbaiki: membungkus ke dua baris di bawah 720px.
3. **Kontras tombol utama gagal AA (3,75:1).** Putih di `#E5484D` di bawah 4,5:1 untuk teks normal. Diperbaiki: latar tombol digelapkan ke `#C93338` (5,23:1); hover `#BE2E33` (5,79:1).

## Disiplin fakta (mengikat)

- **Suplai ditampilkan sebagai "Diusulkan — menunggu persetujuan founder" TANPA angka.** Dua usulan yang bertentangan masih ada: `docs/token-design.md` merancang 1.000.000.000 sementara `docs/website-launch-spec.md` §10 mencatat 10.000.000.000 sebagai usulan. Konflik itu (D-05a) adalah keputusan founder yang masih terbuka; situs tidak menyelesaikannya.
- **Nama token REFORMASI sudah disetujui founder; simbol yang diusulkan REFORMASI** menunggu pemeriksaan kompatibilitas teknis — situs tidak menyatakan simbol itu kompatibel. Tidak ada alamat kontrak/mint, tanggal peluncuran, jumlah holder, volume, harga, atau metrik reward di mana pun di situs — semuanya belum ada.
- Status peluncuran adalah "Belum diluncurkan" / "Mainnet belum diluncurkan", tanpa hitung mundur. Gate mainnet 01 (nama token REFORMASI disetujui) ditandai Selesai; parameter token lainnya tetap belum diputuskan dan gate 02–05 masih Menunggu.
- **Whitelist adalah alur pendaftaran dan peninjauan GRATIS, bukan penjualan whitelist atau alokasi yang dijamin — dan pendaftaran belum dibuka.** Belum ada backend, basis data, atau deployment yang disetujui; situs statis ini tidak mengumpulkan data pendaftar.
- Tanpa counter palsu, waitlist, CTA mati, atau tautan placeholder yang disajikan sebagai fungsional.

## Target deployment (diusulkan, belum dikonfigurasi)

**GitHub Pages (diusulkan)** — keputusan D-01 masih terbuka (technical and founder decisions). Catatan feasibility lengkap ada di `docs/DEPLOYMENT_FEASIBILITY_TOKEN_SITE_2026-11-09.md`: artifact source harus tepat `apps/token-site/` (bukan root repo), opsi workflow GitHub Actions vs branch, domain kustom, HTTPS, implikasi env/keamanan, dan rollback. Situs berada di subdirektori (`apps/token-site/`), jadi Pages membutuhkan workflow yang memublikasikan direktori itu (atau branch khusus). **Belum ada yang di-deploy; tidak ada setting repo yang diubah.**

## Keterbatasan yang diketahui

- **Tanpa koneksi dompet.** Ditunda sesuai `docs/frontend-stack-decision.md` §2 (opsional di spec; menambah package wallet-adapter akan memperkenalkan dependensi untuk fitur opsional). Tidak ada elemen status dompet di header atau di halaman mana pun (dihapus PR-013; `checks.sh` menegaskan ketidakhadirannya).
- **Tanpa backend, tanpa form, tanpa analitik.** Kanal kontak / pelaporan belum dikonfigurasi (dinyatakan sebagai teks biasa di footer).
- **Fakta token yang masih menunggu keputusan founder:** pemeriksaan kompatibilitas simbol, suplai (konflik 1B vs 10B), desimal, alokasi, venue (D-04), tanggal peluncuran, domain resmi, dan tautan sosial terverifikasi.
- **Whitelist belum diimplementasikan.** Situs saat ini tanpa form, backend, basis data, dasbor applicant, atau panel admin. Jangan kumpulkan data applicant nyata sampai arsitektur di `docs/whitelist-spec.md` disetujui.
- **Dukungan reduced-motion diverifikasi lewat inspeksi kode** (media query `prefers-reduced-motion` ada dan menonaktifkan transisi); belum diuji terhadap pengaturan reduced-motion di level OS yang live.
- **Screenshot adalah render lokal** (headless Chrome 157 terhadap server lokal), bukan tangkapan situs yang sudah di-deploy.
- Screenshot mobile founder dari Elysium **tidak ada** di repo dan tidak dipakai; desain bekerja dari deskripsi tertulis atas referensi saja, dan tidak mengkloning referensi mana pun.
