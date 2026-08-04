# IPC System — Simple Code Guide

These notes explain the most important system behaviours in plain English. They are written for a project presentation or a question-and-answer meeting: each file explains what the user sees, what the system really does, and where that behaviour lives in the code.

## Start here

| If someone asks about | Read this file |
| --- | --- |
| How **Excel Verisini Aktar** works | [01-excel-import.md](01-excel-import.md) |
| Why the real count is 2,308 and not 2,453 | [02-real-numbers-and-sira-no.md](02-real-numbers-and-sira-no.md) |
| How attachments are stored and approved | [03-attachments.md](03-attachments.md) |
| How reports, totals, Excel and PDF are generated | [04-reports-and-totals.md](04-reports-and-totals.md) |
| Who can create, approve, edit or delete a record | [05-users-approvals-and-data.md](05-users-approvals-and-data.md) |
| How data is protected, backed up and restored | [06-data-safety-and-backups.md](06-data-safety-and-backups.md) |
| Which libraries and technologies the system uses | [07-technologies-and-libraries.md](07-technologies-and-libraries.md) |

## One-minute project explanation

The application is a Flask web application with a SQLite database. It keeps one IPC record per `Sıra No`; each record stores the official fields in JSON, while the database keeps the record number, dates, audit information, users, pending approvals, notifications and file metadata in separate tables.

Administrators can import a verified Excel file directly. Personnel can request a new record, an edit or a deletion, but an administrator must approve it before the official record changes. Reports always use the currently stored and filtered database records, not manually typed summary values.

## Important terms

| Interface term | Meaning in this project |
| --- | --- |
| `Sıra No` | The permanent record identifier. It comes from the Excel source during import; for a new record SQLite assigns the next identifier. |
| `Sorumlu Personel` | The logged-in person responsible for a new record. It is filled automatically and is not typed again. |
| `Gerçek kayıt` | A source row containing at least one meaningful IPC evidence value, such as a company/person, penalty amount, instrument, report number or process information. |
| `Boş şablon satırı` | A row that has generated or repeated basic values but no meaningful IPC evidence. It is not imported as a record. |
| `Bekleyen talep` | A personnel action that has not yet changed the official record. |

## Primary code files

| File | Responsibility |
| --- | --- |
| `backend/app.py` | Routes, database operations, validation, approval flow, attachments, reports and exports. |
| `backend/importer.py` | Read-only Excel parsing, cleaning, record validation and import preview calculations. |
| `frontend/templates/` | The HTML screens users see. |
| `backend/tests/` | Automated tests for the Excel importer and import workflow. |

The detailed guides describe the current code as it exists in this project; they are not separate system rules.
