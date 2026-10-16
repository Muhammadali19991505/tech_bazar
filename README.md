# 📊 O'zbekiston Elektronika Chakana Savdosi va Marketing Tahlili (2023–2024)

Ushbu repozitoriy O'zbekistonning 5 ta yirik hududidagi elektronika va gadjetlar savdosi, marketing xarajatlari, narx siyosati hamda mijozlar baholarini o'z ichiga olgan ma'lumotlar to'plami (`dataset.csv`) va uning tahliliga bag'ishlangan. Ma'lumotlar **Data Analysis (EDA)**, **Data Cleaning** hamda **Machine Learning (Regressiya / Savdo prognozi)** loyihalari uchun mo'ljallangan.

---

## 📁 Ma'lumotlar to'plami haqida qisqacha

* **Fayl nomi:** `dataset.csv`
* **Qatorlar soni:** 2,400 ta yozuv
* **Ustunlar soni:** 15 ta xususiyat (feature)
* **Vaqt oralig'i:** 2023-yil yanvardan – 2024-yil dekabrgacha (24 oy)
* **Hududlar (5 ta):** Toshkent (`Tashkent`), Samarqand (`Samarkand`), Buxoro (`Bukhara`), Andijon (`Andijan`), Namangan (`Namangan`)
* **Savdo kanallari (3 ta):** `offline`, `online`, `both` (gibrid)
* **Mahsulot toifalari (10 ta):** `smartphones`, `laptops`, `tablets`, `wireless_audio`, `gaming`, `smart_home`, `wearables`, `cameras`, `storage_devices`, `cables_chargers`

---

## 📋 Ustunlar tavsifi (Data Dictionary)

| Ustun nomi | Ma'lumot turi | Tavsifi | Qiymatlar oralig'i / Namuna |
| :--- | :--- | :--- | :--- |
| `product_id` | `string` (`object`) | Mahsulot yoki yozuvning unikal identifikatori | `P1001`, `P1002` ... |
| `category` | `string` (`object`) | Mahsulot toifasi | 10 ta toifa (`smartphones`, `laptops` va b.) |
| `region` | `string` (`object`) | Savdo amalga oshirilgan hudud (viloyat/shahar) | `Tashkent`, `Samarkand`, `Bukhara`, `Andijan`, `Namangan` |
| `store_type` | `string` (`object`) | Do'kon yoki savdo kanali turi | `offline`, `online`, `both` |
| `year` | `int64` | Hisobot yili | `2023`, `2024` |
| `month` | `int64` | Hisobot oyi | `1` – `12` |
| `avg_unit_price` | `float64` | Mahsulotning o'rtacha dona narxi ($) | `11.35` – `884.17` (O'rtacha: `268.43`) |
| `units_sold` | `int64` | Oy davomida sotilgan mahsulotlar soni (dona) | `27` – `1,896` (O'rtacha: `238`) |
| `returns` | `int64` | Qaytarilgan mahsulotlar soni (dona) | `-5` – `113` *(Anomaliya mavjud)* |
| `discount_pct` | `float64` | Taqdim etilgan chegirma foizi (%) | `0.0%` – `35.0%` (O'rtacha: `9.08%`) |
| `promo_active` | `boolean` (`object`) | Promo-aksiya faolligi | `True`, `False` |
| `customer_rating` | `float64` | Mijozlarning o'rtacha bahosi (5 ballik tizimda) | `3.0` – `5.0` (O'rtacha: `4.11`) |
| `competitor_price_index` | `float64` | Raqobatchilar narx indeksi (`<1` raqobatchida arzon, `>1` qimmat) | `0.85` – `1.20` (O'rtacha: `1.03`) |
| `marketing_spend` | `float64` | Oylik marketing va reklama xarajatlari ($) | `49.55` – `24,229.63` (O'rtacha: `2,228.12`) |
| `monthly_revenue` | `float64` | **Target (Maqsadli ustun):** Oylik umumiy daromad ($) | `1,626.53` – `1,278,254.00` (O'rtacha: `39,109.45`) |

---

## ⚠️ Ma'lumotlar sifati va Tozalash (Data Cleaning) eslatmalari

Ma'lumotlar to'plamida real hayotdagi xatoliklarni simulyatsiya qiluvchi kamchiliklar mavjud. Modellashtirishdan oldin quyidagi bosqichlarni bajarish tavsiya etiladi:

1. **Tushirib qoldirilgan qiymatlar (Missing Values):**
   * `promo_active`: **96 ta** (`4.0%`) bo'sh qiymat.
   * `customer_rating`: **72 ta** (`3.0%`) bo'sh qiymat.
   * `competitor_price_index`: **48 ta** (`2.0%`) bo'sh qiymat.
2. **Mantiqiy anomaliyalar (Invalid Values):**
   * `returns` ustunida **3 ta manfiy qiymat** (`-3`, `-4`, `-5` — `P1160`, `P1378`, `P3271` ID-larda) mavjud. Ularni `0` ga yoki musbat qiymatiga (`abs()`) o'zgartirish lozim.
3. **Takroriy ID-lar (Duplicates):**
   * `product_id` ustunida 2,398 ta unikal qiymat bor: `P1935` va `P1475` identifikatorlari ikki martadan turli toifa va hududlarda takrorlangan.

---

## 🚀 Loyihani ishga tushirish

### 1. Rep
