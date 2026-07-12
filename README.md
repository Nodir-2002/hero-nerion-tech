# 🤖 Hero Nerion Tech — Avtomatlashtirilgan AI/Tech Kontent Tizimi

Telegram kanal uchun to'liq avtomatik, multi-agent arxitekturasiga asoslangan kontent generatsiya va nashr qilish tizimi. GitHub Actions orqali bulutda ishlaydi, foydalanuvchi ishtirokisiz kuniga bir necha marta sifatli AI/texnologiya mavzusidagi postlar yaratadi va nashr qiladi.

## 🎯 Loyiha maqsadi

AI/texnologiya sohasida O'zbek tilida sifatli, muntazam kontent ishlab chiqaruvchi, to'liq avtonom tizim yaratish — inson aralashuvisiz ishlaydigan multi-agent arxitektura namunasi sifatida.

## 🏗️ Arxitektura

Tizim bir nechta mustaqil "agent"lardan iborat, har biri o'z vazifasini bajaradi:
Script Writer Agent → Image Generator Agent → Telegram Publisher Agent
↓
GitHub Actions (Scheduler)

- **Script Writer Agent** (`script_writer.py`) — mavzu bo'yicha matn generatsiya qiladi (Claude API bilan integratsiyaga tayyor, hozircha fakt-bazasi asosida mock rejimda ishlaydi)
- **Image Generator Agent** (`local_image_generator.py`) — Pillow yordamida mavzuga mos, brendlashtirilgan vizual kontent yaratadi
- **Telegram Publisher Agent** (`telegram_publisher.py`) — tayyor kontentni Telegram kanalga nashr qiladi
- **Orchestrator** (`main.py`) — barcha agentlarni birlashtiradi, kunlik mavzu tanlaydi
- **Scheduler** (GitHub Actions) — kuniga bir necha marta avtomatik ishga tushiradi, xatolik yuz bersa xabar yuboradi

## 🛠️ Texnologiyalar

- Python 3.11
- Anthropic Claude API (matn generatsiyasi uchun tayyor integratsiya)
- python-telegram-bot
- Pillow (dinamik rasm generatsiyasi)
- GitHub Actions (CI/CD, cron-based scheduling)

## ✨ Asosiy xususiyatlar

- To'liq serversiz (serverless) avtomatlashtirish — GitHub Actions orqali bulutda ishlaydi
- Kuniga bir necha marta, turli vaqt oralig'ida avtomatik nashr
- Dinamik, mavzuga mos vizual kontent generatsiyasi (statik rasmlarsiz)
- Xatolik yuz berganda avtomatik ogohlantirish tizimi
- Modulli arxitektura — har bir komponent mustaqil test qilinadi va almashtiriladi
- "Mock/Real" rejim tizimi — tashqi pullik API'lar mavjud bo'lmaganda ham to'liq test qilish imkoniyati

## 📂 Loyiha tuzilishi
├── main.py                    # Asosiy orkestrator
├── script_writer.py           # Kontent generatsiya agenti
├── local_image_generator.py   # Vizual kontent generatsiya agenti
├── telegram_publisher.py      # Telegram nashr agenti
├── icons/                     # Dizayn uchun ikonkalar
└── .github/workflows/         # Avtomatlashtirish konfiguratsiyasi
## 🚀 Kelajakdagi rejalar

- YouTube Shorts uchun video generatsiya pipeline'ini qo'shish
- Claude API bilan to'liq integratsiya (real-time kontent)
- Analytics agent — post samaradorligini kuzatish

## 👤 Muallif

Nodir — Python/AI dasturchi, O'zbekiston
