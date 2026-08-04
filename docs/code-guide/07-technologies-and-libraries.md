# 7. Technologies and Libraries

## Short answer to give in a meeting

“The system is built with Python and Flask. SQLite stores the data, `openpyxl` reads and creates Excel files, and ReportLab creates PDF reports. Bootstrap provides the responsive interface, while Chart.js draws the dashboard charts.”

## Backend libraries

| Technology / library | Why it is used in this project | Where it is used |
| --- | --- | --- |
| **Python** | Main programming language for the server-side application. | `backend/app.py`, `backend/importer.py` |
| **Flask** | Web framework: routes, HTML rendering, form requests, sessions, downloads and error handling. | Throughout `backend/app.py` |
| **Jinja2** | HTML template engine included with Flask. It puts records and calculated values into the screens. | `frontend/templates/*.html` |
| **SQLite** | Lightweight relational database stored in one database file (`ipc.db`). | `sqlite3` use and `init_db()` in `backend/app.py` |
| **openpyxl** | Opens Excel files in read-only mode for import and produces styled `.xlsx` report files. | `backend/importer.py` → `load_workbook()`; `backend/app.py` → `build_excel()` |
| **ReportLab** | Creates downloadable PDF reports, including Turkish character support and the readable Full Record layout. | `backend/app.py` → `build_pdf()` |
| **Werkzeug** | Flask’s HTTP utilities: secure password hashing, safe file delivery and request handling. | `backend/app.py` → `generate_password_hash()`, `check_password_hash()`, `send_from_directory()` |
| **itsdangerous** | Creates signed, time-limited password-reset tokens. | `backend/app.py` → `URLSafeTimedSerializer` |
| **Gunicorn** | Production web server used to run Flask outside local development. | `Procfile` |
| **Waitress** | Windows-compatible production web server used by the standalone LAN executable. | `windows_server.py` |
| **PyInstaller** | Build-time tool that packages Python, the application and its libraries into a Windows `.exe`. It is used by GitHub Actions and is not required on department laptops. | `.github/workflows/build-windows.yml` |

## Frontend libraries

| Technology / library | Why it is used in this project | Where it is used |
| --- | --- | --- |
| **HTML, CSS and JavaScript** | The browser interface, interactions, validation feedback and file-selection display. | `frontend/templates/`, `frontend/static/` |
| **Bootstrap 5.3.3** | Responsive layout, forms, modals, alerts, buttons and toast notifications. | Loaded from the CDN in `frontend/templates/base.html` and authentication templates |
| **Bootstrap Icons 1.11.3** | The icons used across menus, buttons and messages. | Loaded from the CDN in `frontend/templates/base.html` and authentication templates |
| **Chart.js 4.4.3** | Dashboard charts for annual records/amounts, legal basis and status. | `frontend/templates/dashboard.html` and `frontend/static/js/dashboard.js` |

## Built-in Python components

These are part of Python itself, so they do not need a separate installation package:

| Component | Use in this project |
| --- | --- |
| `sqlite3` | SQLite database connection, transactions and safe backup API. |
| `json` | Stores flexible IPC form fields as JSON inside each official record. |
| `hashlib` | Creates the SHA-256 fingerprint used to identify the exact imported Excel file. |
| `datetime` | Dates, deadlines, report dates and import backup timestamps. |
| `uuid` | Random secure internal filenames for attachments and temporary import tokens. |
| `unittest` | Automated tests for the importer and import workflow. |

## Extra resources used by PDF generation

PDF reports use the local `DejaVuSans.ttf` and `DejaVuSans-Bold.ttf` font files in `backend/fonts/`. They are registered by ReportLab so Turkish characters such as `İ`, `Ş`, `Ğ` and `Ç` render correctly.

## Installation

The server-side packages are listed in [backend/requirements.txt](../../backend/requirements.txt):

```text
Flask
gunicorn
waitress
Werkzeug
itsdangerous
openpyxl
reportlab
```

For local development:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The frontend libraries are currently loaded from the jsDelivr CDN. If the system will be used on a network without internet access, Bootstrap, Bootstrap Icons and Chart.js should be downloaded into `frontend/static/` and referenced locally.

## Demonstration sentence

“We did not create PDF or Excel manually. We use established libraries: `openpyxl` makes the Excel output reliable, and ReportLab generates official PDF documents with the correct Turkish font.”
