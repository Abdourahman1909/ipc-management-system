# İPC Management System

[![Windows build](https://github.com/Abdourahman1909/ipc-management-system/actions/workflows/build-windows.yml/badge.svg)](https://github.com/Abdourahman1909/ipc-management-system/actions/workflows/build-windows.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A multi-user administrative penalty record system developed during a 2026
computer-engineering internship for the **Kocaeli Provincial Directorate of
Industry and Technology** (*Kocaeli İl Sanayi ve Teknoloji Müdürlüğü*).

> **Public-data notice:** this repository contains application source code and
> synthetic demonstration material only. It contains no real institutional
> workbooks, database records, accounts, attachments, or backups.

## Real-world context

The department's historical administrative penalty workflow was held in a
large, multi-year Excel workbook. The project turned that workflow into one
application for importing, finding, updating, approving, attaching documents
to, and reporting official records.

The solution was designed for the office's actual constraint: one Windows
laptop runs the application as a local server, while authorised staff on the
same private network connect through their browsers. No Python installation is
required on staff computers.

The completed system was presented to the provincial director, department
management, and personnel on **30 July 2026**.

![The three computer-engineering interns who developed the project](docs/images/intern-team.jpg)

*The three internship project contributors.*

![Presentation of the working system to the provincial director and department personnel](docs/images/project-presentation.jpg)

*Presentation of the working İPC Management System at the Kocaeli Provincial
Directorate of Industry and Technology — 30 July 2026.*

## What the system does

- Imports historical `.xlsx` and `.xlsm` workbooks through a safe preview and
  confirmation workflow.
- Distinguishes genuine business records from pre-filled Excel template rows.
- Supports record creation, editing, deletion, attachments, personnel accounts,
  approval requests, notifications, and password management.
- Filters records and produces management, collection, objection, and complete
  record reports in PDF and Excel formats.
- Creates a SQLite backup before a confirmed workbook import and rolls back a
  failed transaction.
- Builds a portable Windows server package and supports concurrent use over a
  trusted private LAN.

## Architecture

```text
Browser clients on the private LAN
                │
                ▼
        Flask + Waitress server
                │
       ┌────────┼─────────┐
       ▼        ▼         ▼
    SQLite   uploads/   backups/
```

| Area | Technologies |
| --- | --- |
| Backend | Python, Flask, SQLite, Waitress |
| Excel | openpyxl |
| Reports | ReportLab, openpyxl, DejaVu fonts |
| Frontend | Jinja2, HTML, CSS, JavaScript, Bootstrap, Chart.js |
| Windows delivery | PyInstaller, GitHub Actions |
| Testing | Python `unittest`, synthetic Excel workbooks |

## Run locally

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

export IPC_INITIAL_ADMIN_EMAIL="admin@example.local"
export IPC_INITIAL_ADMIN_PASSWORD="choose-a-strong-demo-password"

python backend/app.py
```

Open <http://127.0.0.1:5000>. There is no hard-coded default password.

To load synthetic demonstration records:

```bash
export IPC_INITIAL_ADMIN_PASSWORD="choose-a-strong-demo-password"
python backend/ornek_veri.py
```

To generate a fictional workbook for testing the Excel import screen:

```bash
python backend/demo_workbook.py
```

The generated workbook is ignored by Git and must never be replaced with an
institutional source file inside the repository.

## Windows and private-LAN delivery

The workflow in `.github/workflows/build-windows.yml` produces a portable
`IPC_Yonetim_Sistemi.exe`. On its first start, the launcher asks for a new
administrator password. Runtime data is created beside the executable under
`data/` and is excluded from version control.

See [WINDOWS_KURULUM.md](WINDOWS_KURULUM.md) for the server-laptop, private
firewall, connection, backup, and troubleshooting instructions.

## Testing

```bash
cd backend
python -m unittest discover -s tests -v
```

The import tests build fictional workbooks in temporary directories; they do
not require or contain departmental data.

## Contributors

- **[Abdourahman Mohamed Ismail](https://github.com/Abdourahman1909)** — Excel
  import, Windows/LAN packaging, repository and release preparation, and
  frontend design collaboration.
- **[Jasmin Jandaulyet](https://github.com/jasemino)** — frontend implementation
  and UI/UX collaboration.
- **[Bokang Daniel Klaas](https://github.com/bokangklaas11-code)** — backend
  implementation and testing collaboration.

Repository preparation is managed by Abdourahman Mohamed Ismail. The project
was developed collaboratively; detailed attribution is recorded in
[AUTHORS.md](AUTHORS.md).

## Institutional project supervision

**[Hakan Albay](https://github.com/H-Albay)** — Project Supervisor, İPC Unit.
He guided the project from the department's İPC workflow and software
perspective and coordinated its institutional use.

## Documentation

- [Windows server setup](WINDOWS_KURULUM.md)
- [ER diagram](docs/er-diagram/README.md)
- [Contributor statement](AUTHORS.md)
- [Security policy](SECURITY.md)

## Responsible use and data safety

Never commit real workbooks, databases, `.env` files, account information,
uploads, backups, or `.ipc-secret`. Do not post real records in public issues.
See [SECURITY.md](SECURITY.md) before reporting a vulnerability or data-safety
problem.

## Licence

Original project software is released under the [MIT Licence](LICENSE).
Institutional names and emblems, presentation photographs, fonts, and other
third-party assets remain subject to their respective owners' rights and are
not relicensed by the MIT Licence. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

AI-assisted development tools were used under the contributors' direction and
review. The contributors remain responsible for the final project decisions and
delivered code.
