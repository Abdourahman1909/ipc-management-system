# 1. Excel Import (`Excel Verisini Aktar`)

## Short answer to give in a meeting

“The Excel file is checked first; nothing is written to the database during that check. The system shows the real record count, the skipped template rows, warnings, column mapping and total penalty amount. Only after an administrator confirms does it create a SQLite backup and import the records.”

## What happens step by step

1. Only an administrator can open **Excel Verisini Aktar**.
2. The user selects an `.xlsx` or `.xlsm` file.
3. The file is copied to a protected temporary location and parsed in read-only mode. The original Excel file is never edited.
4. The importer finds the worksheet and header row, matches the recognised columns, cleans values and separates real records from template rows.
5. The preview shows record count, source rows, skipped rows, warnings, year counts, total penalty amount and any duplicate `Sıra No` values already in the database.
6. The administrator chooses what to do with duplicate `Sıra No` values: keep the existing database record (`skip`) or update it from Excel (`update`).
7. On confirmation, the application uses SQLite’s backup operation to create a full database backup, starts one database transaction, imports the data, writes an `import_history` audit entry, then commits everything together.
8. If an error happens during the transaction, the transaction is rolled back. The prior database state remains unchanged.

## Why the preview is safe

The preview is intentionally not an import. `parse_workbook()` only reads the Excel file. The database write happens later in the separate confirmation route.

The file is also checked twice: the system keeps a SHA-256 fingerprint of the previewed file and refuses the import if the temporary file has changed before confirmation.

## How invalid source values are handled

- Valid dates are converted to `GG.AA.YYYY`.
- Valid monetary amounts are converted to numeric values.
- An unreadable non-empty date or amount is not silently lost: it becomes a warning and the original value is preserved in `Kaynak Notu / Uyarısı`.
- An Excel source with duplicate `Sıra No` values is rejected. The user must fix the source first.
- Extra non-empty cells without a recognised header are preserved in `Kaynak Notu / Uyarısı`.

## Important implementation details

| Question | Answer |
| --- | --- |
| Does it overwrite Excel? | No. It opens the workbook read-only and never saves it. |
| Does preview change the database? | No. Preview only reads and calculates. |
| Can it import the same `Sıra No` twice? | Not as a second official row. The administrator chooses to skip it or update the existing row. |
| Is there a history? | Yes. File name, SHA-256 fingerprint, counts, warnings, choice, backup path, user and time are saved in `import_history`. |
| What happens to temporary Excel files? | They are removed after import and expired temporary files are cleaned after two hours. |

## Code locations

| Behaviour | Code |
| --- | --- |
| Excel parsing and real-record decision | `backend/importer.py` → `parse_workbook()` |
| Preview upload route | `backend/app.py` → `veri_aktar()` |
| Preview confirmation/import route | `backend/app.py` → `veri_aktar_onayla()` |
| Safe SQLite backup | `backend/app.py` → `_create_import_backup()` |
| Import screen | `frontend/templates/veri_aktar.html` |

## Demonstration sentence

“I can show the preview first. It explains exactly how many rows are real records, which rows were skipped, and why. The **Yedeği Al ve Aktar** button is the only point that writes to the database.”
