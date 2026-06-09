# 📄 Smart Line Breaker

A simple and efficient tool for splitting and merging text files, built with Python and PySide6.

---

## ✨ Features

- **File Splitting:** Splits `.txt` and `.json` files into chunks with a user-defined number of lines
- **Configurable Chunk Size:** Set the number of lines per chunk directly from the UI (default: 500)
- **File Merging:** Reassembles split parts back together in the correct order
- **Multi-language Support:** Translation system based on JSON files in the `locales/` folder
- **Drag & Drop:** Drag a file or folder directly onto the app window
- **Light / Dark Theme:** Toggle with a single click
- **RTL Support:** Full right-to-left layout for Persian, Arabic, and Hebrew

---

## 🛠️ Requirements

- Python 3.9+
- PySide6

### Install PySide6

```bash
pip install PySide6
```

If you have multiple Python versions installed:

```bash
py -m pip install PySide6
```

---

## 🚀 Run

```bash
python main.py
```

---

## 📁 Project Structure

```
project/
│
├── main.py               # Main application file
│
└── locales/              # Translation files
    ├── fa.json           # Persian
    ├── en.json           # English
    └── ...               # Other languages
```

---

## ⚙️ How It Works

### Splitting
- Reads the input file line by line
- Uses the value from the **"Lines per chunk"** field in the UI
- Saves output files in a folder named `<filename>_parts/`
- Output naming: `filename_part_001.txt`, `filename_part_002.txt`, ...

### Merging
- Scans the selected folder for part files
- Identifies files matching the pattern `*_part_XXX.txt` or `*_part_XXX.json`
- Sorts by part number and merges them in order
- Saves the result as `Merged_Result.txt` (or `.json`) in the same folder

---

## 🌐 Adding a New Language

make a issue or do this:

1. Create a JSON file with the language code in the `locales/` folder (e.g. `de.json`)
2. Define the following keys:

```json
{
  "lang_name": "Deutsch",
  "app_title": "...",
  "tab_extract": "...",
  "tab_replace": "...",
  "split_title": "...",
  "split_desc": "...",
  "merge_title": "...",
  "merge_desc": "...",
  "open_file_btn": "...",
  "open_dir_btn": "...",
  "process_split_btn": "...",
  "process_merge_btn": "...",
  "split_placeholder": "...",
  "merge_placeholder": "...",
  "chunk_size_label": "...",
  "warning_title": "...",
  "success_title": "...",
  "error_title": "...",
  "no_file": "...",
  "no_dir": "...",
  "no_parts_found": "...",
  "reading_part": "...",
  "split_done": "...",
  "merge_done": "...",
  "error_msg": "..."
}
```

3. Restart the app — the new language will appear automatically in the language selector.

> **Note:** The `chunk_size_label` key was added in the latest version. Make sure to add it to all existing translation files.

---

## 📝 Technical Notes

- All files are read and written using **UTF-8** encoding, suitable for all languages including Persian
- Switching to Persian/Arabic/Hebrew automatically flips the UI to right-to-left layout
- Files without the `_part_XXX` pattern are ignored during merging
- Chunk size can be set between **1 and 100,000** lines

---

## 📄 License

MIT License

---
---

# 📄 اسمارت لاین بریکر

یک ابزار ساده و کارآمد برای تقسیم و ادغام فایل‌های متنی، ساخته‌شده با Python و PySide6.

---

## ✨ ویژگی‌ها

- **تقسیم فایل (Split):** فایل‌های `.txt` و `.json` را به قطعات با تعداد خط دلخواه تقسیم می‌کند
- **تعداد خط قابل تنظیم:** کاربر می‌تواند تعداد خطوط هر قطعه را مستقیم از رابط برنامه تعیین کند (پیش‌فرض: ۵۰۰)
- **ادغام فایل (Merge):** قطعات تقسیم‌شده را به ترتیب صحیح به هم می‌چسباند
- **پشتیبانی از چند زبان:** سیستم ترجمه مبتنی بر فایل‌های JSON در پوشه `locales/`
- **پشتیبانی از Drag & Drop:** می‌توانید فایل یا پوشه را مستقیم روی برنامه بکشید
- **تم روشن / تاریک:** قابل تغییر با یک کلیک
- **پشتیبانی RTL:** رابط کاربری کامل راست‌به‌چپ برای فارسی، عربی و عبری

---

## 🛠️ پیش‌نیازها

- Python 3.9+
- PySide6

### نصب PySide6

```bash
pip install PySide6
```

اگر چند نسخه Python دارید:

```bash
py -m pip install PySide6
```

---

## 🚀 اجرا

```bash
python main.py
```

---

## 📁 ساختار پروژه

```
project/
│
├── main.py               # فایل اصلی برنامه
│
└── locales/              # فایل‌های ترجمه
    ├── fa.json           # فارسی
    ├── en.json           # انگلیسی
    └── ...               # سایر زبان‌ها
```

---

## ⚙️ نحوه عملکرد

### تقسیم فایل
- فایل ورودی را خط‌به‌خط می‌خواند
- تعداد خطوط هر قطعه را از فیلد **«تعداد خطوط هر قطعه»** در رابط برنامه می‌گیرد
- فایل‌های خروجی را در پوشه‌ای با نام `<نام_فایل>_parts/` ذخیره می‌کند
- نام‌گذاری خروجی: `filename_part_001.txt`, `filename_part_002.txt`, ...

### ادغام فایل
- پوشه حاوی قطعات را اسکن می‌کند
- فایل‌هایی با الگوی `*_part_XXX.txt` یا `*_part_XXX.json` را شناسایی می‌کند
- بر اساس شماره قطعه مرتب و ادغام می‌کند
- نتیجه را در فایل `Merged_Result.txt` (یا `.json`) در همان پوشه ذخیره می‌کند

---

## 🌐 افزودن زبان جدید

یک درخواست ثبت کنید یا:

۱. یک فایل JSON با کد زبان در پوشه `locales/` بسازید (مثلاً `de.json`)
۲. کلیدهای زیر را تعریف کنید:

```json
{
  "lang_name": "Deutsch",
  "app_title": "...",
  "tab_extract": "...",
  "tab_replace": "...",
  "split_title": "...",
  "split_desc": "...",
  "merge_title": "...",
  "merge_desc": "...",
  "open_file_btn": "...",
  "open_dir_btn": "...",
  "process_split_btn": "...",
  "process_merge_btn": "...",
  "split_placeholder": "...",
  "merge_placeholder": "...",
  "chunk_size_label": "...",
  "warning_title": "...",
  "success_title": "...",
  "error_title": "...",
  "no_file": "...",
  "no_dir": "...",
  "no_parts_found": "...",
  "reading_part": "...",
  "split_done": "...",
  "merge_done": "...",
  "error_msg": "..."
}
```

۳. برنامه را ریستارت کنید — زبان جدید به‌صورت خودکار در منوی انتخاب زبان ظاهر می‌شود.

> **نکته:** کلید `chunk_size_label` نسبت به نسخه قبل اضافه شده و باید در تمام فایل‌های ترجمه موجود هم اضافه شود.

---

## 📝 نکات فنی

- برنامه از encoding **UTF-8** استفاده می‌کند؛ مناسب برای تمام زبان‌ها از جمله فارسی
- تغییر زبان به فارسی/عربی/عبری به‌صورت خودکار جهت رابط را به راست‌به‌چپ تغییر می‌دهد
- فایل‌های بدون الگوی `_part_XXX` در فرآیند ادغام نادیده گرفته می‌شوند
- مقدار تعداد خطوط بین **۱ تا ۱۰۰٬۰۰۰** قابل تنظیم است

---

## 📄 لایسنس

MIT License
