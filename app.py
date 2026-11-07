from flask import Flask, request, session, redirect, url_for, render_template_string
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "habib_arch_studio_online_final_2026"

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect("habib_studio.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    """)
    
    cursor.execute("DELETE FROM admin")
    cursor.execute("INSERT INTO admin (id, username, password) VALUES (1, 'Rizwan Habib', '010700')")
    
    default_settings = [
        ("whatsapp", "6283148073635"),
        ("phone", "+62 831-5435-097"),
        ("instagram", "https://www.instagram.com/habib_arch_studio0107"),
        ("maps", "https://maps.app.goo.gl/46UqnKYGG1J3GgRb6"),
        ("tagline", "Wujudkan Ruang Impian Bersama Muh Rizwan Habib"),
        ("about", "Habib Arch Studio berfokus pada perancangan bangunan berkualitas tinggi yang mengutamakan kenyamanan, estetika visual modern, serta ketepatan anggaran konstruksi."),
        ("profile_img", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=600&auto=format&fit=crop"),
        ("bg_img", "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1920&auto=format&fit=crop"),
        ("bio_detail", "Arsitek profesional spesialis hunian modern, tata ruang interior estetik, dan perencanaan konstruksi efisien.")
    ]
    for key, val in default_settings:
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, val))
        
    conn.commit()
    conn.close()

init_db()

def get_settings():
    conn = sqlite3.connect("habib_studio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM settings")
    data = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return data

@app.route("/")
def index():
    settings = get_settings()
    conn = sqlite3.connect("habib_studio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, image_url FROM portfolios ORDER BY id DESC")
    portfolios = cursor.fetchall()
    conn.close()
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Habib Arch Studio — Professional Architecture & Design</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0f172a; color: #f8fafc; }
        .glass-nav { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(12px); }
        .hero-bg {
            background: linear-gradient(rgba(15, 23, 42, 0.78), rgba(15, 23, 42, 0.92)), url('{{ settings.bg_img }}');
            background-size: cover; background-position: center;
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased selection:bg-amber-500 selection:text-slate-950">

    <!-- Floating WhatsApp Button -->
    <a href="https://wa.me/{{ settings.whatsapp }}?text=Halo%20Habib%20Arch%20Studio,%20saya%20tertarik%20berkonsultasi%20mengenai%20desain%20arsitektur." target="_blank" class="fixed bottom-6 right-6 z-50 bg-emerald-500 hover:bg-emerald-600 text-white p-4 rounded-full shadow-2xl flex items-center justify-center transition-all duration-300 hover:scale-110 group" aria-label="WhatsApp Chat">
        <i class="fa-brands fa-whatsapp text-2xl"></i>
        <span class="max-w-0 overflow-hidden whitespace-nowrap group-hover:max-w-xs transition-all duration-500 ease-in-out text-sm font-semibold px-0 group-hover:px-2">Konsultasi WA</span>
    </a>

    <!-- Navbar -->
    <nav class="fixed top-0 left-0 w-full z-40 glass-nav border-b border-slate-800">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="#" class="text-base md:text-xl font-extrabold tracking-wider text-white uppercase flex items-center gap-2">
                <i class="fa-solid fa-compass-drafting text-amber-500"></i> Habib Arch Studio
            </a>
            <div class="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
                <a href="#tentang" class="hover:text-amber-400 transition">Tentang</a>
                <a href="#layanan" class="hover:text-amber-400 transition">Layanan</a>
                <a href="#portofolio" class="hover:text-amber-400 transition">Portofolio</a>
                <a href="#kalkulator" class="hover:text-amber-400 transition">Kalkulator</a>
                <a href="#konsultasi" class="hover:text-amber-400 transition">Form Order</a>
                <button onclick="shareWebsite()" class="bg-amber-500/10 border border-amber-500/40 text-amber-400 hover:bg-amber-500 hover:text-slate-950 px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5">
                    <i class="fa-solid fa-share-nodes"></i> Bagikan Tautan
                </button>
                <a href="/admin" class="text-xs bg-slate-800 hover:bg-slate-700 text-amber-400 border border-amber-500/40 px-3 py-2 rounded-lg transition"><i class="fa-solid fa-lock"></i> Admin</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-bg min-h-screen flex items-center justify-center text-center px-6 pt-24 pb-16">
        <div class="max-w-3xl mx-auto space-y-6">
            <div class="flex justify-center">
                <div class="relative p-1.5 rounded-full bg-gradient-to-tr from-amber-500 to-amber-200 shadow-2xl">
                    <img src="{{ settings.profile_img }}" alt="Muh Rizwan Habib" class="w-32 h-32 md:w-40 md:h-40 rounded-full object-cover border-4 border-slate-900 shadow-inner">
                </div>
            </div>
            
            <div class="flex items-center justify-center gap-2">
                <span class="inline-block bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-widest"><i class="fa-solid fa-circle text-[8px] mr-1.5 animate-pulse"></i> Studio Buka Hari Ini</span>
            </div>

            <h1 class="text-3xl md:text-6xl font-extrabold tracking-tight text-white leading-tight">
                {{ settings.tagline }}
            </h1>
            <p class="text-slate-300 text-base md:text-lg max-w-2xl mx-auto font-light">
                {{ settings.bio_detail }}
            </p>
            <div class="pt-4 flex flex-col sm:flex-row justify-center gap-4">
                <a href="https://wa.me/{{ settings.whatsapp }}" target="_blank" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-8 py-4 rounded-xl shadow-lg transition-all text-center">Chat WhatsApp Langsung</a>
                <button onclick="shareWebsite()" class="bg-slate-800 hover:bg-slate-700 text-white font-semibold px-6 py-4 rounded-xl border border-slate-700 transition-all text-center flex items-center justify-center gap-2">
                    <i class="fa-solid fa-share-nodes"></i> Bagikan Tautan
                </button>
            </div>
        </div>
    </section>

    <!-- Tentang / Kontak Studio -->
    <section id="tentang" class="py-24 px-6 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div class="space-y-6">
            <h2 class="text-amber-500 font-bold tracking-widest uppercase text-sm">Arsitek Utama</h2>
            <h3 class="text-3xl md:text-4xl font-extrabold text-white">Muh Rizwan Habib</h3>
            <p class="text-slate-300 leading-relaxed font-light">
                {{ settings.about }}
            </p>
            <div class="grid grid-cols-3 gap-4 pt-2">
                <div class="border-l-4 border-amber-500 pl-4"><p class="text-2xl font-bold text-white">100+</p><p class="text-xs text-slate-400">Proyek Selesai</p></div>
                <div class="border-l-4 border-amber-500 pl-4"><p class="text-2xl font-bold text-white">100%</p><p class="text-xs text-slate-400">Puas & Rapi</p></div>
                <div class="border-l-4 border-amber-500 pl-4"><p class="text-2xl font-bold text-white">K.35</p><p class="text-xs text-slate-400">Start Tarif</p></div>
            </div>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl space-y-4">
            <h4 class="text-xl font-bold text-white border-b border-slate-800 pb-3">Informasi Kontak & Studio</h4>
            <ul class="space-y-4 text-slate-300 text-sm">
                <li class="flex items-center gap-3"><i class="fa-solid fa-phone text-amber-500 w-5"></i> <span>{{ settings.phone }} (Telp)</span></li>
                <li class="flex items-center gap-3"><i class="fa-brands fa-whatsapp text-emerald-500 w-5"></i> <a href="https://wa.me/{{ settings.whatsapp }}" class="hover:underline">+{{ settings.whatsapp }} (WhatsApp)</a></li>
                <li class="flex items-center gap-3"><i class="fa-brands fa-instagram text-pink-500 w-5"></i> <a href="{{ settings.instagram }}" target="_blank" class="hover:underline">Instagram Resmi (@habib_arch_studio0107)</a></li>
                <li class="flex items-center gap-3"><i class="fa-solid fa-location-dot text-red-500 w-5"></i> <a href="{{ settings.maps }}" target="_blank" class="hover:underline text-amber-400">Buka Lokasi Google Maps</a></li>
            </ul>
            <div class="pt-2">
                <button onclick="downloadVCard()" class="w-full bg-slate-800 hover:bg-slate-700 text-amber-400 font-bold py-3 rounded-xl border border-slate-700 text-xs transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-address-book"></i> Simpan Kontak Arsitek ke HP
                </button>
            </div>
        </div>
    </section>

    <!-- Layanan & Harga -->
    <section id="layanan" class="py-24 px-6 bg-slate-900/50 border-y border-slate-800/80">
        <div class="max-w-7xl mx-auto space-y-12">
            <div class="text-center space-y-4 max-w-2xl mx-auto">
                <h2 class="text-amber-500 font-bold tracking-widest uppercase text-sm">Layanan Profesional</h2>
                <h3 class="text-3xl md:text-4xl font-extrabold text-white">Cakupan Jasa Arsitektur</h3>
                <p class="text-slate-400 text-sm">Tarif jasa profesional <span class="text-amber-400 font-bold">start from K.35</span></p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-3 hover:border-amber-500/40 transition-all"><div class="text-amber-400 text-xl font-bold"><i class="fa-solid fa-comments"></i></div><h4 class="text-lg font-bold text-white">1. Konsultasi Arsitektur</h4><p class="text-slate-400 text-sm">Diskusi awal konsep tata letak dan gaya bangunan.</p></div>
                <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-3 hover:border-amber-500/40 transition-all"><div class="text-amber-400 text-xl font-bold"><i class="fa-solid fa-file-lines"></i></div><h4 class="text-lg font-bold text-white">2. Gambar Kerja</h4><p class="text-slate-400 text-sm">Dokumen teknis lengkap siap bangun untuk tukang.</p></div>
                <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-3 hover:border-amber-500/40 transition-all"><div class="text-amber-400 text-xl font-bold"><i class="fa-solid fa-couch"></i></div><h4 class="text-lg font-bold text-white">3. Desain Interior</h4><p class="text-slate-400 text-sm">Penataan tata letak dan estetika ruang dalam.</p></div>
                <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-3 hover:border-amber-500/40 transition-all"><div class="text-amber-400 text-xl font-bold"><i class="fa-solid fa-tree"></i></div><h4 class="text-lg font-bold text-white">4. Desain Landscape</h4><p class="text-slate-400 text-sm">Perancangan taman, carport, dan area hijau luar.</p></div>
                <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-3 hover:border-amber-500/40 transition-all"><div class="text-amber-400 text-xl font-bold"><i class="fa-solid fa-helmet-safety"></i></div><h4 class="text-lg font-bold text-white">5. Pengawasan Proyek</h4><p class="text-slate-400 text-sm">Inspeksi berkala konstruksi fisik di lapangan.</p></div>
                <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-3 hover:border-amber-500/40 transition-all"><div class="text-amber-400 text-xl font-bold"><i class="fa-solid fa-calculator"></i></div><h4 class="text-lg font-bold text-white">6. Perencanaan & RAB</h4><p class="text-slate-400 text-sm">Penyusunan Rencana Anggaran Biaya terperinci.</p></div>
            </div>
        </div>
    </section>

    <!-- Kalkulator Estimasi Biaya -->
    <section id="kalkulator" class="py-24 px-6 max-w-4xl mx-auto space-y-8">
        <div class="text-center space-y-3">
            <h2 class="text-amber-500 font-bold tracking-widest uppercase text-sm">Estimasi Biaya</h2>
            <h3 class="text-3xl font-extrabold text-white">Kalkulator Biaya Desain Awal</h3>
            <p class="text-xs text-slate-400">Hitung estimasi awal budget desain berdasarkan luas tanah / bangunan Anda.</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl space-y-6 shadow-xl">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="text-xs text-slate-400">Luas Bangunan / Tanah (m²)</label>
                    <input type="number" id="calcArea" placeholder="Contoh: 100" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white" oninput="calculateCost()">
                </div>
                <div>
                    <label class="text-xs text-slate-400">Paket Layanan</label>
                    <select id="calcPackage" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white" onchange="calculateCost()">
                        <option value="35000">Desain Standar (Start Rp 35.000 / m²)</option>
                        <option value="50000">Desain Lengkap + RAB (Rp 50.000 / m²)</option>
                        <option value="75000">Desain Eksklusif + 3D Interior (Rp 75.000 / m²)</option>
                    </select>
                </div>
            </div>
            <div class="bg-slate-950 p-6 rounded-2xl border border-slate-800 text-center space-y-2">
                <span class="text-xs text-slate-400 uppercase tracking-widest font-semibold">Estimasi Total Biaya Desain</span>
                <p id="totalCost" class="text-3xl md:text-4xl font-extrabold text-amber-400">Rp 0</p>
                <p class="text-[10px] text-slate-500">*Harga pasti disesuaikan dengan tingkat kesulitan dan diskusi saat konsultasi.</p>
            </div>
        </div>
    </section>

    <!-- Portofolio -->
    <section id="portofolio" class="py-24 px-6 max-w-7xl mx-auto space-y-12">
        <div class="text-center space-y-4 max-w-2xl mx-auto">
            <h2 class="text-amber-500 font-bold tracking-widest uppercase text-sm">Galeri Karya</h2>
            <h3 class="text-3xl md:text-4xl font-extrabold text-white">Portofolio Pilihan Studio</h3>
            
            <div class="flex flex-wrap justify-center gap-2 pt-4">
                <button onclick="filterPortfolio('all')" class="filter-btn active bg-amber-500 text-slate-950 px-4 py-1.5 rounded-full text-xs font-bold transition">Semua</button>
                <button onclick="filterPortfolio('residential')" class="filter-btn bg-slate-800 text-slate-300 hover:bg-slate-700 px-4 py-1.5 rounded-full text-xs font-bold transition">Residential</button>
                <button onclick="filterPortfolio('commercial')" class="filter-btn bg-slate-800 text-slate-300 hover:bg-slate-700 px-4 py-1.5 rounded-full text-xs font-bold transition">Commercial</button>
                <button onclick="filterPortfolio('interior')" class="filter-btn bg-slate-800 text-slate-300 hover:bg-slate-700 px-4 py-1.5 rounded-full text-xs font-bold transition">Interior</button>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {% for item in portfolios %}
            <div class="portfolio-item group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900" data-category="{{ item[2]|lower }}">
                <img src="{{ item[3] }}" alt="{{ item[1] }}" class="w-full h-72 object-cover group-hover:scale-105 transition duration-500 cursor-pointer" onclick="openLightbox('{{ item[3] }}')">
                <div class="p-6 space-y-2">
                    <span class="text-xs text-amber-400 font-semibold uppercase">{{ item[2] }}</span>
                    <h4 class="text-xl font-bold text-white">{{ item[1] }}</h4>
                </div>
            </div>
            {% else %}
            <p class="text-center col-span-3 text-slate-500">Belum ada portofolio yang diunggah. Silakan tambahkan lewat Panel Admin.</p>
            {% endfor %}
        </div>
    </section>

    <!-- Form Konsultasi Interaktif WhatsApp -->
    <section id="konsultasi" class="py-24 px-6 bg-slate-900/40 border-t border-slate-800">
        <div class="max-w-2xl mx-auto bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl space-y-6">
            <div class="text-center space-y-2">
                <h3 class="text-2xl font-extrabold text-white">Mulai Konsultasi Proyek</h3>
                <p class="text-xs text-slate-400">Isi data singkat di bawah ini, pesan akan langsung terhubung ke WhatsApp Muh Rizwan Habib.</p>
            </div>
            <form onsubmit="sendWhatsApp(event)" class="space-y-4">
                <div><label class="text-xs text-slate-400">Nama Lengkap Anda</label><input type="text" id="clientName" required class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white" placeholder="Contoh: Budi Santoso"></div>
                <div><label class="text-xs text-slate-400">Jenis Layanan yang Dibutuhkan</label><select id="clientService" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"><option>Konsultasi Arsitektur</option><option>Gambar Kerja</option><option>Desain Interior</option><option>Desain Landscape</option><option>Pengawasan Proyek</option><option>Perencanaan & RAB</option></select></div>
                <div><label class="text-xs text-slate-400">Pesan / Keterangan Kebutuhan Ruang</label><textarea id="clientMsg" rows="3" required class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white" placeholder="Contoh: Saya ingin merancang rumah 2 lantai di lahan 10x15 meter..."></textarea></div>
                <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3.5 rounded-xl text-sm transition shadow-lg flex items-center justify-center gap-2"><i class="fa-brands fa-whatsapp text-lg"></i> Kirim Pesan Order via WhatsApp</button>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-slate-900 border-t border-slate-800 py-12 px-6 text-center space-y-4">
        <p class="text-sm text-slate-400">&copy; 2026 Habib Arch Studio • Muh Rizwan Habib. All Rights Reserved.</p>
        <div class="flex justify-center gap-4 text-xs">
            <button onclick="shareWebsite()" class="text-amber-400 hover:underline"><i class="fa-solid fa-share-nodes"></i> Bagikan Tautan Web</button> | 
            <a href="/admin" class="text-slate-500 hover:text-amber-400 underline">Masuk ke Panel Pengelola Admin</a>
        </div>
    </footer>

    <!-- Modal Lightbox Preview Image -->
    <div id="lightboxModal" class="fixed inset-0 z-50 bg-black/90 hidden items-center justify-center p-4" onclick="closeLightbox()">
        <img id="lightboxImg" src="" class="max-w-full max-h-[90vh] rounded-2xl shadow-2xl border border-slate-800">
    </div>

    <script>
        function sendWhatsApp(e) {
            e.preventDefault();
            let name = document.getElementById('clientName').value;
            let service = document.getElementById('clientService').value;
            let msg = document.getElementById('clientMsg').value;
            let phone = "{{ settings.whatsapp }}";
            let text = `Halo Habib Arch Studio,%0A%0ASaya *${name}*%0AIngin berkonsultasi mengenai layanan: *${service}*%0A%0ADetail Kebutuhan:%0A${msg}`;
            window.open(`https://wa.me/${phone}?text=${text}`, '_blank');
        }

        function filterPortfolio(category) {
            let items = document.querySelectorAll('.portfolio-item');
            items.forEach(item => {
                if (category === 'all' || item.getAttribute('data-category').includes(category)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function calculateCost() {
            let area = document.getElementById('calcArea').value || 0;
            let price = document.getElementById('calcPackage').value || 0;
            let total = area * price;
            document.getElementById('totalCost').innerText = 'Rp ' + total.toLocaleString('id-ID');
        }

        function shareWebsite() {
            let currentUrl = window.location.href;
            if (navigator.share) {
                navigator.share({
                    title: 'Habib Arch Studio',
                    text: 'Jasa Arsitektur & Perencanaan Bangunan Profesional Muh Rizwan Habib',
                    url: currentUrl
                });
            } else {
                navigator.clipboard.writeText(currentUrl);
                alert('Tautan Website Habib Arch Studio berhasil disalin!');
            }
        }

        function downloadVCard() {
            let vcard = "BEGIN:VCARD\\nVERSION:3.0\\nFN:Muh Rizwan Habib\\nORG:Habib Arch Studio\\nTEL;TYPE=CELL:{{ settings.phone }}\\nTEL;TYPE=WA:{{ settings.whatsapp }}\\nEND:VCARD";
            let blob = new Blob([vcard], { type: "text/vcard" });
            let link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = "Muh_Rizwan_Habib_Arsitek.vcf";
            link.click();
        }

        function openLightbox(url) {
            document.getElementById('lightboxImg').src = url;
            document.getElementById('lightboxModal').classList.remove('hidden');
            document.getElementById('lightboxModal').classList.add('flex');
        }

        function closeLightbox() {
            document.getElementById('lightboxModal').classList.remove('flex');
            document.getElementById('lightboxModal').classList.add('hidden');
        }
    </script>
</body>
</html>
    """, settings=settings, portfolios=portfolios)

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect("habib_studio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Username atau Password salah!"
            
    return render_template_string("""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8"><title>Login Admin — Habib Arch Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex items-center justify-center min-h-screen p-6">
    <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl max-w-md w-full space-y-6 shadow-2xl">
        <h2 class="text-2xl font-extrabold text-amber-400 text-center">🔑 Login Admin Studio</h2>
        <p class="text-xs text-slate-400 text-center">Username: <strong>Rizwan Habib</strong> & Password: <strong>010700</strong></p>
        {% if error %}<div class="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded-lg text-xs text-center">{{ error }}</div>{% endif %}
        <form method="POST" class="space-y-4">
            <div><label class="text-xs text-slate-400">Username</label><input type="text" name="username" required value="Rizwan Habib" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
            <div><label class="text-xs text-slate-400">Password</label><input type="password" name="password" required value="010700" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
            <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-3 rounded-xl transition">Masuk Panel</button>
        </form>
        <div class="text-center"><a href="/" class="text-xs text-slate-400 hover:underline">← Kembali ke Website Utama</a></div>
    </div>
</body>
</html>
    """, error=error)

@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    
    conn = sqlite3.connect("habib_studio.db")
    cursor = conn.cursor()
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "add_portfolio":
            title = request.form.get("title")
            category = request.form.get("category")
            file = request.files.get("portfolio_file")
            image_url = request.form.get("image_url")
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = f"/{filepath}"
            
            if image_url:
                cursor.execute("INSERT INTO portfolios (title, category, image_url) VALUES (?, ?, ?)", (title, category, image_url))
                conn.commit()
                
        elif action == "delete_portfolio":
            pid = request.form.get("id")
            cursor.execute("DELETE FROM portfolios WHERE id = ?", (pid,))
            conn.commit()
            
        elif action == "update_settings":
            profile_file = request.files.get("profile_file")
            if profile_file and allowed_file(profile_file.filename):
                p_filename = secure_filename(profile_file.filename)
                p_path = os.path.join(app.config['UPLOAD_FOLDER'], p_filename)
                profile_file.save(p_path)
                cursor.execute("UPDATE settings SET value = ? WHERE key = 'profile_img'", (f"/{p_path}",))
            
            bg_file = request.files.get("bg_file")
            if bg_file and allowed_file(bg_file.filename):
                b_filename = secure_filename(bg_file.filename)
                b_path = os.path.join(app.config['UPLOAD_FOLDER'], b_filename)
                bg_file.save(b_path)
                cursor.execute("UPDATE settings SET value = ? WHERE key = 'bg_img'", (f"/{b_path}",))
                
            for key in ["whatsapp", "phone", "instagram", "maps", "tagline", "about", "bio_detail"]:
                val = request.form.get(key)
                if val:
                    cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (val, key))
            conn.commit()
            
    cursor.execute("SELECT id, title, category, image_url FROM portfolios ORDER BY id DESC")
    portfolios = cursor.fetchall()
    settings = get_settings()
    conn.close()
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8"><title>Panel Pengelola — Habib Arch Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 p-6 md:p-12">
    <div class="max-w-4xl mx-auto space-y-10">
        <div class="flex justify-between items-center border-b border-slate-800 pb-6">
            <div>
                <h1 class="text-2xl font-extrabold text-white">⚙️ Panel Admin Habib Arch Studio</h1>
                <p class="text-xs text-slate-400">Masuk sebagai: <span class="text-amber-400 font-bold">Rizwan Habib</span></p>
            </div>
            <div class="flex gap-3">
                <a href="/" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-xs px-4 py-2 rounded-xl border border-slate-700">Lihat Web</a>
                <a href="/admin/logout" class="bg-red-500/20 text-red-400 border border-red-500/40 text-xs px-4 py-2 rounded-xl">Keluar</a>
            </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
            <h2 class="text-lg font-bold text-amber-400">Pengaturan Bio, Profil & Background (Upload dari Galeri)</h2>
            <form method="POST" enctype="multipart/form-data" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input type="hidden" name="action" value="update_settings">
                
                <div>
                    <label class="text-xs text-slate-400">Upload Foto Profil Bulat (Galeri HP/PC)</label>
                    <input type="file" name="profile_file" accept="image/*" class="w-full bg-slate-950 border border-slate-800 p-2.5 rounded-xl mt-1 text-xs text-slate-300">
                </div>
                <div>
                    <label class="text-xs text-slate-400">Upload Background Hero (Galeri HP/PC)</label>
                    <input type="file" name="bg_file" accept="image/*" class="w-full bg-slate-950 border border-slate-800 p-2.5 rounded-xl mt-1 text-xs text-slate-300">
                </div>

                <div><label class="text-xs text-slate-400">Nomor WhatsApp (Format: 628...)</label><input type="text" name="whatsapp" value="{{ settings.whatsapp }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                <div><label class="text-xs text-slate-400">Nomor Telepon Biasa</label><input type="text" name="phone" value="{{ settings.phone }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                <div><label class="text-xs text-slate-400">Link Instagram</label><input type="text" name="instagram" value="{{ settings.instagram }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                <div><label class="text-xs text-slate-400">Link Google Maps</label><input type="text" name="maps" value="{{ settings.maps }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                
                <div class="md:col-span-2"><label class="text-xs text-slate-400">Tagline Utama Hero Web</label><input type="text" name="tagline" value="{{ settings.tagline }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                <div class="md:col-span-2"><label class="text-xs text-slate-400">Bio Singkat di Bawah Tagline (Hero Bio)</label><textarea name="bio_detail" rows="2" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white">{{ settings.bio_detail }}</textarea></div>
                <div class="md:col-span-2"><label class="text-xs text-slate-400">Deskripsi Lengkap Tentang Arsitek</label><textarea name="about" rows="2" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white">{{ settings.about }}</textarea></div>
                
                <div><button type="submit" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-6 py-3 rounded-xl text-sm transition">Simpan Perubahan Bio & Foto</button></div>
            </form>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
            <h2 class="text-lg font-bold text-amber-400">Tambah Foto Portofolio Baru (Upload Galeri)</h2>
            <form method="POST" enctype="multipart/form-data" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input type="hidden" name="action" value="add_portfolio">
                <div><label class="text-xs text-slate-400">Judul Proyek</label><input type="text" name="title" required placeholder="Contoh: Modern Tropical House" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                <div><label class="text-xs text-slate-400">Kategori</label><input type="text" name="category" required placeholder="Residential / Interior" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl mt-1 text-sm text-white"></div>
                <div><label class="text-xs text-slate-400">Pilih Foto dari Galeri</label><input type="file" name="portfolio_file" accept="image/*" required class="w-full bg-slate-950 border border-slate-800 p-2.5 rounded-xl mt-1 text-xs text-slate-300"></div>
                <div class="md:col-span-3"><button type="submit" class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-6 py-3 rounded-xl text-sm transition">Unggah & Tambah Portofolio</button></div>
            </form>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
            <h2 class="text-lg font-bold text-amber-400">Daftar Portofolio Aktif</h2>
            <div class="space-y-3">
                {% for item in portfolios %}
                <div class="flex justify-between items-center bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <div class="flex items-center gap-4">
                        <img src="{{ item[3] }}" class="w-16 h-12 object-cover rounded-lg">
                        <div>
                            <p class="font-bold text-sm text-white">{{ item[1] }}</p>
                            <p class="text-xs text-amber-400 uppercase">{{ item[2] }}</p>
                        </div>
                    </div>
                    <form method="POST">
                        <input type="hidden" name="action" value="delete_portfolio">
                        <input type="hidden" name="id" value="{{ item[0] }}">
                        <button type="submit" class="bg-red-500/20 text-red-400 hover:bg-red-500/30 px-3 py-1.5 rounded-lg text-xs font-semibold">Hapus</button>
                    </form>
                </div>
                {% else %}
                <p class="text-sm text-slate-500">Belum ada portofolio yang diunggah.</p>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
    """, portfolios=portfolios, settings=settings)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)