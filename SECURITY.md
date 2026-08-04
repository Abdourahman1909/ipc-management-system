# Security and Data-Safety Policy

## Public repository rule

This repository must never receive real institutional records. Do not commit or
attach production Excel workbooks, SQLite databases, `.env` files, passwords,
session secrets, uploaded documents, database backups, or screenshots containing
identifiable records.

The `.gitignore` file is a safety layer, not permission to place sensitive files
inside the repository directory. Operational data belongs only on the authorised
server laptop and its protected backups.

## Reporting a vulnerability

Do not open a public issue containing exploit details or real data. Contact the
repository maintainer privately at `zaynmohamed063@gmail.com` with:

- the affected version or commit;
- steps to reproduce using synthetic data;
- the expected and observed behaviour; and
- the potential impact.

No real record is required to demonstrate a vulnerability.

## Deployment scope

The standalone Windows configuration is intended for a trusted private
institutional network. It must not be exposed directly to the public internet.
Public-internet deployment requires a production security review, HTTPS, a
managed reverse proxy, protected persistent storage, monitoring, and an
appropriate database deployment.
