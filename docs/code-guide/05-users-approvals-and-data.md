# 5. Users, Approval and Official Data

## Short answer to give in a meeting

“The system separates a request from an official record. Administrators can change official IPC records immediately. Personnel submit add, edit or delete requests; these become official only after an administrator approves them.”

## Roles

| Role | Main permissions |
| --- | --- |
| Administrator (`admin`) | Manage users, import Excel, approve/reject requests, create/edit/delete official records, delete attachments. |
| Personnel (`personel`) | View official records and submit new-record, edit or delete requests. |

All protected routes require a logged-in user. Administrator-only actions have an additional role check.

## Creating a new IPC record

The system validates each required field before saving. It also validates dates, integer values, monetary values and selected-list values.

`Sorumlu Personel` is filled from the logged-in account name. The user does not type it again, because the same account is already known by the session. The legacy Excel label `Defter Sıra No` is presented in the application as `Sorumlu Personel`.

For multiple instruments, every item includes both a type and a positive quantity. The system keeps the item list and calculates two Excel-compatible summaries:

- `Ölçü Aleti Sayısı`: sum of all quantities;
- `Ölçü Aleti Cinsi`: paired summary such as `Taksimetre (3); Tanker sayacı (2)`.

## Approval flow

1. Personnel creates, edits or requests deletion.
2. The proposed action is saved in `pending_actions`; the official `companies` record is unchanged.
3. Administrators see it in **Onaylar** with the requester, proposed changes and pending attachments.
4. On approval, the requested operation is applied to the official record and the requester receives a notification.
5. On rejection, the official record remains unchanged, the reason is saved and the requester receives a notification.

For an approved personnel-created record, SQLite assigns the official next `Sıra No` at the time of approval.

## Where data is kept

| Data | Table |
| --- | --- |
| Official IPC records | `companies` |
| Accounts and roles | `users` |
| Pending requests | `pending_actions` |
| Notifications | `notifications` |
| Attachment metadata | `attachments` |
| Excel import audit history | `import_history` |
| Configurable fields | `form_fields` |

## Code locations

| Behaviour | Code |
| --- | --- |
| Authentication and administrator check | `backend/app.py` → `login_required()` and `admin_required()` |
| Form validation and multi-instrument checks | `backend/app.py` → `collect_form()` and `sync_instrument_data()` |
| New record flow | `backend/app.py` → `sirket_ekle()` |
| Edit/delete request flow | `backend/app.py` → `sirket_duzenle()` and `sirket_sil()` |
| Apply official change | `backend/app.py` → `apply_company_action()` |
| Administrator approval/rejection | `backend/app.py` → `onay_karar()` |
| Table definitions | `backend/app.py` → `init_db()` |

## Demonstration sentence

“Personnel cannot silently change the official database. Their request is stored separately, so an administrator can inspect and approve it first.”
