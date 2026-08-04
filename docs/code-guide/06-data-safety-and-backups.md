# 6. Data Safety, Backups and Deployment Notes

## Short answer to give in a meeting

“The official data is stored in SQLite. Before every confirmed Excel import, the system creates a safe SQLite backup. The database file and the uploaded-files folder must both be backed up, because attachment metadata and attachment files are stored separately.”

## SQLite backup mechanism

The import process calls SQLite’s built-in `backup()` API before it begins to write imported data. This creates a consistent copy of the database in `backend/backups/` by default.

This is safer than simply copying the `.db` file while it might be in use, because the SQLite backup API produces a consistent snapshot.

The backup name follows this pattern:

`ipc-before-import-YYYYMMDD-HHMMSS.db`

The created backup path is saved in `import_history`, so the import can be traced to its safety copy.

## What must be backed up

| Item | Why it matters |
| --- | --- |
| SQLite database (`ipc.db`) | Official records, users, approvals, notifications, configuration and attachment metadata. |
| Upload directory (`uploads/`) | The actual attachment files. |
| Backup directory (`backups/`) | Automatic pre-import recovery points. |
| Environment settings | Production secret key and persistent storage paths. Keep them protected; do not put secrets in Git. |

Restoring only the database without `uploads/` leaves attachment records that point to missing files. Restoring only `uploads/` without the database loses the link between files and records. Restore them together from matching backups.

## Safe import behaviour

- A backup is created before the import transaction begins.
- Database changes use a transaction: either all successful import changes commit together, or the database transaction rolls back.
- The original Excel source is never modified.
- The temporary import file is removed after completion; old temporary files are cleaned automatically.

## Deploying from one laptop or as a website

The application can run on one office laptop, but then users need network access to that laptop and it must remain running. For a shared website, deploy the Flask application to a server with persistent storage and point these settings to that storage:

- `IPC_DB_PATH` for the SQLite database;
- `IPC_UPLOAD_DIR` for attachments;
- `IPC_BACKUP_DIR` for database backups.

SQLite supports multiple people reading at the same time and handles writes safely through locking. The provided production setup runs one application process with worker threads. For one office/team this is appropriate. Do not run multiple separate application copies that write to the same SQLite file; use a single application instance with one shared persistent disk.

For a much larger installation with frequent simultaneous writes or multiple server instances, migrate from SQLite to a server database such as PostgreSQL.

## Windows package for a non-technical office

The repository includes `windows_server.py` and a GitHub Actions workflow that
builds `IPC_Yonetim_Sistemi_Windows.zip` on a real Windows runner. The package
contains a standalone `.exe`, so department laptops do not need Python.

The executable uses Waitress as its Windows-compatible production server, listens
on the private LAN, prints the address for other laptops, and keeps the database,
uploads, backups and session secret together in a persistent `data` directory
beside the executable. See `WINDOWS_KURULUM.md` for the non-technical instructions.

## Code locations

| Behaviour | Code |
| --- | --- |
| Database, upload and backup paths | `backend/app.py` → `DB_PATH`, `UPLOAD_DIR`, `BACKUP_DIR` |
| Safe SQLite backup | `backend/app.py` → `_create_import_backup()` |
| Import transaction | `backend/app.py` → `veri_aktar_onayla()` |
| Production command | `Procfile` |
| Windows standalone launcher | `windows_server.py` |
| Windows executable build | `.github/workflows/build-windows.yml` |
| Deployment configuration notes | `BENIOKU.md` and `.env.example` |

## Demonstration sentence

“Before Excel changes the live records, the system creates a SQLite-consistent backup. For a full recovery we keep the database and uploaded-files folder together.”
