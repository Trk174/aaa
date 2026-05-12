# 🤖 Site Bot

Bot care simulează un vizitator real pe site-ul tău. Rulează automat **în fiecare zi** via GitHub Actions și stă pe site un timp random între **6 și 18 ore**.

---

## ⚙️ Setup (2 pași)

### 1. Adaugă URL-ul ca Secret în GitHub

1. Mergi la repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Nume: `SITE_URL`
4. Valoare: `https://site-ul-tau.ro`
5. Click **Add secret**

### 2. Gata! ✅

GitHub Actions va rula botul automat **în fiecare zi la 08:00 UTC**.

---

## 🚀 Rulare manuală

Poți porni botul oricând din GitHub:

**Actions** → **Daily Site Bot** → **Run workflow**

---

## 🏠 Rulare locală

```bash
python site_bot.py --url https://site-ul-tau.ro
python site_bot.py --url https://site-ul-tau.ro --min-hours 4 --max-hours 10
```

---

## 📋 Ce face

| Funcție | Detalii |
|---|---|
| ⏱️ Durată | Random între 6–18 ore pe zi |
| 💤 Pauze | 45 sec – 8 min (distribuție naturală) |
| 🖥️ User-Agent | Rotează Chrome / Safari / Firefox / iPhone |
| 📡 Zero dependențe | Doar Python standard (3.x) |

---

## 📁 Structura proiectului

```
site-bot/
├── .github/
│   └── workflows/
│       └── daily_bot.yml   ← GitHub Actions (rulare zilnică)
├── site_bot.py             ← scriptul principal
└── README.md
```
