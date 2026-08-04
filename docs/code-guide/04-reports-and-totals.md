# 4. Reports, Totals and Exports

## Short answer to give in a meeting

“A report is generated from the live database after the selected filters are applied. Its record count and total penalty amount are calculated from those same included records, so the preview, PDF and Excel use the same scope.”

## Report flow

1. The user chooses a report type: summary, full record, collection or objection report.
2. The user can narrow the scope by company/report number, a single year or an inclusive start-year/end-year range, status, legal basis or advanced field filters.
3. The application loads official IPC records from the database and applies those filters.
4. It sorts the result by year and `Sıra No`.
5. It calculates the report summary: record count, total penalty amount, active deadline count, expired deadline count and paid count.
6. The user previews the result or downloads it as PDF or Excel.

Pending requests are not included in reports. A personnel request becomes reportable only after administrator approval changes the official record.

## Why the report total is trustworthy

The total is not typed into the screen or stored as a separate editable number. The code loops through the exact filtered records and adds each record’s `ceza_tutari`.

That means:

- selecting one year only totals that year;
- selecting a legal basis only totals that legal basis;
- changing a saved record changes the next generated report;
- the report count and total use the same records.

## PDF versus Excel

| Output | Behaviour |
| --- | --- |
| **Excel** | Keeps every selected column. It adds a title, period, creation date, record count and total penalty amount. It includes filters, frozen headers, wrapped cells and print settings. |
| **Short PDF reports** | Use a compact landscape table. |
| **Full Record PDF** | Does not squeeze all 28 columns into one unreadable table. It prints each IPC record in readable sections and hides empty values. |

The PDF’s visible layout can be different from Excel, but both outputs use the same selected records and fields.

## Dashboard numbers

The dashboard uses all official IPC records. It shows:

- total record count;
- total penalty amount;
- collected amount (`doğrudan yatırılan` plus `vergi tahsil tutarı`);
- count for the current year;
- deadline warnings and status breakdowns;
- charts grouped by year and legal basis.

## Code locations

| Behaviour | Code |
| --- | --- |
| Filter and sort records | `backend/app.py` → `_apply_company_filters()` and `report_companies()` |
| Create report summary | `backend/app.py` → `_report_summary()` |
| Render report page | `backend/app.py` → `rapor()` and `frontend/templates/rapor.html` |
| Create Excel file | `backend/app.py` → `build_excel()` |
| Create PDF file | `backend/app.py` → `build_pdf()` |
| Download routes | `backend/app.py` → `rapor_pdf()` and `rapor_excel()` |
| Dashboard calculations | `backend/app.py` → `dashboard()` |

## Demonstration sentence

“First I choose the filter and preview the report. The number of records and the total are recalculated from exactly that filtered list, then the same list is exported to PDF or Excel.”
