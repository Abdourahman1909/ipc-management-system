# 3. Attachments (`Ek Dosyalar`)

## Short answer to give in a meeting

“Users can select multiple attachments in one operation. The system validates every file before saving it, gives each file a random safe disk name, and keeps the original display name and file metadata in the database.”

## What the system accepts

- Up to **10 files** in one create/edit operation.
- Maximum **100 MB per file**.
- Maximum **300 MB for the whole web request**.
- Documents, spreadsheets, presentations, archives, images and videos from the approved extension list.
- Executables, HTML and SVG are not accepted.

The interface shows selected file names and sizes before the form is saved. A user can add more files to the current selection or remove a selected file.

## How files are stored

The original filename is used only for display and downloading. The physical disk filename is a new random UUID-based name, such as `a1b2...c3.pdf`. This prevents one file from overwriting another and prevents a user-supplied filename from becoming a server path.

The database table `attachments` stores the connection to the record, original filename, generated filename, MIME type, size, uploader and creation time. The actual file is stored in `backend/uploads/` by default, or in the path configured by `IPC_UPLOAD_DIR`.

## Approval behaviour

| Who performs the action | Where the attachment is linked first | What happens later |
| --- | --- | --- |
| Administrator | Directly to the official IPC record | It remains attached to that record. |
| Personnel | To a pending action | On approval it moves to the official record; on rejection it is deleted. |

When an official IPC record is deleted, its linked attachments are deleted from the database and then from disk. If saving a record fails, newly written files are removed so that no orphan attachment remains.

## Access control

- A file already attached to an official IPC record can be opened by logged-in users.
- A file attached to a pending request can be opened by an administrator or the person who made that request.
- Only an administrator can delete an attachment.
- Download responses use safe headers; inline preview is restricted to approved previewable types.

## Code locations

| Behaviour | Code |
| --- | --- |
| File limits and allowed extensions | `backend/app.py` → constants near the top of the file |
| Validation before writing files | `backend/app.py` → `_prepare_attachments()` |
| Secure disk save and database metadata | `backend/app.py` → `_save_prepared_attachments()` |
| Safe delete | `backend/app.py` → `_delete_stored_files()` and `attachment_delete()` |
| Download/preview permission check | `backend/app.py` → `attachment_file()` |
| Create/edit form upload use | `backend/app.py` → `sirket_ekle()` and `sirket_duzenle()` |

## Demonstration sentence

“The original file name is preserved for the user, but the server stores a random internal name. That makes collisions and path manipulation much safer.”
