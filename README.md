# QA Automation - EDOT Project

Automation testing untuk aplikasi EDOT menggunakan **Selenium Python**, **Pytest**, dan **Allure Report**.  


---

## 1. Requirements

- Python >= 3.10
- Pip
- Browser Chrome / Firefox (terbaru)
- ChromeDriver / GeckoDriver sesuai versi browser
- Library Python:
  - selenium
  - pytest
  - allure-pytest
  - pytest-html (opsional)
  - webdriver-manager (opsional untuk auto-download driver)
- Allure Commandline

---

## 2. Cara Install Requirement

### 2.1 Install Python
- **Windows / Mac / Linux:** [Download Python](https://www.python.org/downloads/)

### 2.2 Install pip (jika belum ada)
```bash python -m ensurepip --upgrade

2.3 Install Virtual Environment (opsional tapi direkomendasikan)
python -m venv venv


Aktifkan virtual environment:

Windows:

venv\Scripts\activate


Mac / Linux:

source venv/bin/activate

2.4 Install library Python
pip install -r requirements.txt


Contoh requirements.txt:

selenium>=4.14.0
pytest>=9.0.0
allure-pytest>=2.0.0
pytest-html>=5.0.0
webdriver-manager>=3.8.0

2.5 Install Allure Commandline
MacOS (Homebrew)
brew install allure

Windows (Scoop / Chocolatey)
choco install allure

Linux (Ubuntu/Debian)
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure


Cek versi:

allure --version

3. Cara Menjalankan Test

Dari root project:

pytest tests/ --alluredir=allure-results


tests/ → folder tempat test case

--alluredir=allure-results → folder sementara hasil test yang akan dibaca Allure

4. Cara Membuka dan Menyimpan Report
4.1 Menampilkan report sementara
allure serve allure-results


Akan generate report dari folder allure-results dan membuka di browser.

Setiap run baru akan menimpa hasil sebelumnya.

4.2 Menyimpan report permanen
allure generate allure-results -o allure-report --clean


Folder allure-report/ bisa dibuka kapan saja:

open allure-report/index.html


Semua milestone screenshot dan screenshot saat test gagal akan tampil di report.

5. Tips

Pastikan driver (ChromeDriver / GeckoDriver) sesuai versi browser.

Gunakan virtual environment untuk menghindari konflik dependency.

Gunakan milestone screenshot di TCS untuk report lebih rapi.

conftest.py sudah menambahkan screenshot otomatis saat test gagal.


6. Struktur Project

project-root/
│
├─ base/
│   └─ base_page.py
│   └─ base_test.py
│
├─ pages/
│   ├─ login_page.py
│   ├─ dashboard.py
│   ├─ form_add_company.py
│   └─ company_detail.py
│
├─ tests/
│   └─ test_open_browser.py
│
├─ helper/
│   └─ data_faker.py
│   └─ custom_command.py
│
├─ conftest.py
├─ requirements.txt
└─ README.md
