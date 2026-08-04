# İPC Management System — ER Diagram

This folder contains the database relationship diagram derived from the
application's actual SQLite schema.

## Files

- `ipc-er-diagram.svg`: Main scalable diagram; best for browser viewing and zooming.
- `ipc-er-diagram.png`: High-resolution image for presentations and documents.
- `ipc-er-diagram.pdf`: Printable single-page version.
- `ipc-er-diagram.dot`: Editable Graphviz source.

## Diagram notation

- **PK**: Primary key.
- **UQ**: Unique field or unique index.
- **REF**: A column used as a logical reference by the application.
- **Dashed `1:N` connector**: One parent record can be associated with many child
  records.

The diagram now shows this explicitly in its legend as `1 - - - - N`. The
following dashed relationships appear between the table cards:

- `users (1) → (N) notifications`
- `users (1) → (N) pending_actions`
- `users (1) → (N) attachments`
- `users (1) → (N) import_history`
- `companies (1) → (N) pending_actions`
- `companies (1) → (N) attachments`
- `pending_actions (1) → (N) attachments`

## Important schema notes

The current SQLite schema does not declare any `FOREIGN KEY` constraints. The
dashed relationships were derived from application queries and column usage.
They are shown as logical relationships rather than physical foreign keys so
the diagram does not imply stronger database enforcement than actually exists.

The `companies.data` column stores the 28 Excel fields and measuring-instrument
items as JSON. `pending_actions.data` stores the proposed record state awaiting
approval, and `notifications.metadata` stores optional notification details.

`companies.created_by` is a historical text audit field, not a user ID. Numeric
columns that logically refer to a user or another record are marked as `REF`.

## Regenerating the diagram

With Graphviz installed, run these commands from this folder:

```bash
dot -Tsvg ipc-er-diagram.dot -o ipc-er-diagram.svg
dot -Tpng -Gdpi=180 ipc-er-diagram.dot -o ipc-er-diagram.png
dot -Tpdf ipc-er-diagram.dot -o ipc-er-diagram.pdf
```
