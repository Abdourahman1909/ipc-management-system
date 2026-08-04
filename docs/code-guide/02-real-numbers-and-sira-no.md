# 2. Real Numbers and `Sıra No`

## Short answer to give in a meeting

“The importer does not count every non-empty Excel row. It counts only rows
that contain evidence of a genuine İPC record. Template rows and formulas are
shown in the preview but are not stored as official records.”

## Why a worksheet row count can be misleading

Excel can report rows as used because they contain copied formulas, formatting,
or pre-filled template values. A physical worksheet-row count is therefore not
the same as a business-record count.

The importer treats a row as a real record only when it has a valid `Sıra No`
and at least one meaningful value from the project's evidence fields. Evidence
can include the person or company, penalty amount, tablet report number,
instrument information, dispatch or notification, payment, objection, or
collection information.

Rows that contain only template values—such as a sequence number, year,
institution, legal basis, or formulas—are classified as template rows and
skipped. The import preview shows the real-record count, the source rows, and
the skipped rows before the database is changed.

The public repository intentionally contains no production workbook or exact
institutional totals. Run `python backend/demo_workbook.py` to create a small
fictional workbook and observe the same decision process safely.

## What happens for a new record

`companies.sira_no` is an SQLite `INTEGER PRIMARY KEY AUTOINCREMENT` value. The
next new record follows the highest official record stored in the database.
Skipped template rows are never inserted, so they never reserve identifiers.

## Why totals are trustworthy

- **Import preview total:** the importer sums valid `ceza_tutari` values from
  the source rows classified as real records.
- **Dashboard and report total:** the application sums `ceza_tutari` from the
  official database records after applying the selected filters.

Recognised amounts are converted into numeric values before summing. Unreadable
non-empty source values produce a visible warning instead of disappearing.

## Other calculated values

| Value | Calculation |
| --- | --- |
| Total records | Number of official rows in `companies`; pending requests are excluded. |
| Total penalty amount | Sum of official `ceza_tutari` values. |
| Collected amount | Direct payment plus tax-office collection for each record. |
| Remaining time | Thirty days after notification unless a closing workflow event stops the timer. |
| Instrument count | Sum of quantities from all instrument items attached to the record. |

## Code locations

| Behaviour | Code |
| --- | --- |
| Evidence fields and template-row classification | `backend/importer.py` → `RECORD_EVIDENCE_KEYS` and `parse_workbook()` |
| Source total calculation | `backend/importer.py` → `parse_workbook()` |
| New record identifier | `backend/app.py` → `companies` table and `apply_company_action()` |
| Dashboard totals | `backend/app.py` → `dashboard()` |
| Report totals | `backend/app.py` → `_report_summary()` |
| Remaining time and status | `backend/app.py` → `kalan_sure()` and `company_status()` |

## Demonstration sentence

“The number is trustworthy because the importer counts valid business records,
not every row Excel happens to consider used, and it shows the classification
before anything is saved.”
