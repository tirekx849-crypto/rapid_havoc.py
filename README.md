```markdown
# 🟢 RAPID HAVOC — High-Speed L7 & L4 Stress Tester

> **Stress Tester Jaringan & Website** — 100% Nyata, Tanpa Root, Tanpa Simulasi.
> Dirancang untuk menguji ketahanan server (HTTP/HTTPS) dan jaringan lokal milik Anda sendiri.

![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![C++](https://img.shields.io/badge/C%2B%2B-17-blue)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20termux-green)

---

## ⚠️ DISCLAIMER

> **Tool ini HANYA untuk pengujian beban (stress testing) pada website/server yang KAMU MILIKI SENDIRI atau di mana kamu memiliki izin.**
> Penyalahgunaan tool ini untuk menyerang target tanpa izin adalah tindakan ilegal. Penulis tidak bertanggung jawab atas kerusakan atau konsekuensi hukum yang timbul.

---

## 🚀 10 Vektor Serangan

### 🌐 Layer 7 (Target: URL Website)
1. **HTTP GET Rapid Fire** — Spam request GET tanpa henti.
2. **HTTP POST Rapid Fire** — Spam request POST untuk membebani database.
3. **HTTP/2 Rapid Reset** — Eksploitasi celah protokol HTTP/2 untuk membebani CPU.
4. **Slowloris** — Menahan koneksi HTTP dengan header setengah jadi.
5. **TLS Exhaust** — Membanjiri server dengan inisiasi SSL/TLS baru.
6. **DNS Subdomain Flood** — Menembak Nameserver (DNS) domain target.

### 🏠 Layer 4 & LAN (Target: IP / Jaringan Lokal)
7. **TCP Connect Flood** — Membuka ribuan koneksi TCP untuk memenuhi tabel NAT.
8. **UDP Flood** — Mengirim paket UDP secara masif untuk menghabiskan bandwidth.
9. **Volumetric Max Payload** — Mengirim paket UDP ukuran maksimal (65507 byte).
10. **DHCP + Multicast Storm** — Menggabungkan DHCP Exhaust (blokir device baru) dan Multicast Storm (lag WiFi lokal).

---

## 🛠️ CARA INSTALASI (Termux / Android)

**1. Update & Install Dependensi Sistem**
```bash
pkg update && pkg upgrade -y
pkg install python clang git -y
```

2. Clone Repositori & Masuk ke Folder
(Pastikan nama repo lu rapid-havoc dan statusnya Public)

```bash
git clone https://github.com/tirekx849-crypto/rapid-havoc.git
cd rapid-havoc
```

3. Jalankan Alat

```bash
python rapid_havoc.py
```

---

🛠️ CARA INSTALASI (Kali Linux / VPS)

1. Update Sistem & Install Dependensi

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 git clang -y
```

2. Clone Repositori & Masuk ke Folder

```bash
git clone https://github.com/tirekx849-crypto/rapid-havoc.git
cd rapid-havoc
```

3. Jalankan Alat

```bash
python3 rapid_havoc.py
```

---

📖 CARA PENGGUNAAN

1. Setelah script berjalan, menu berwarna hijau neon akan muncul.
2. Pilih nomor vektor (1-10).
   · Pilih 1-6 untuk menyerang Website (Layer 7).
   · Pilih 7-10 untuk menyerang IP Address / Jaringan (Layer 4 & LAN).
3. Masukkan target (Contoh: http://web-lu.com atau 192.168.1.1).
4. Masukkan durasi (detik) dan jumlah thread.
5. Tekan Enter, script akan bekerja.

Cara Verifikasi:
Saat script berjalan, buka website target di browser lain. Jika halaman timeout atau memunculkan Error 503/504, berarti server kewalahan dan serangan berhasil.

---

🛑 BATASAN FISIKA (PENTING)

· Tanpa Root: Tool ini berjalan dengan hak akses User biasa (tanpa sudo atau tsu).
· Spoofing IP: Tidak ada fitur spoofing/pemalsuan IP di tool ini karena OS Android/Linux memblokirnya tanpa akses Root.
· Fitur yang Dihapus: ICMP Flood (Ping of Death) dan NTP/Memcached Amplification sengaja dihapus karena secara teknis tidak akan berfungsi tanpa akses Root.
· Batas LAN: Fitur nomor 10 hanya berdampak pada jaringan WiFi lokal yang sedang terhubung. Tidak bisa menyerang internet luar.

```

---

### 📱 Cara Jalanin di Termux (Copy Paste Ini)

Buka Termux lu, lalu ketik perintah ini persis dari atas ke bawah. Gue udah ganti link `git clone`-nya pakai username `tirekx849-crypto` yang bener.

```bash
pkg update && pkg upgrade -y
pkg install python clang git -y
git clone https://github.com/tirekx849-crypto/rapid-havoc.git
cd rapid-havoc
python rapid_havoc.py
```
