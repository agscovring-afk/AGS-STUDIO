# AGS ERP V2 - AGS-STUDIO
ERP Enterprise for Aluminium, Glass and Construction Management.
Desktop ERP for construction/facade companies.

See `docs/` for project requirements and design.

Quick start:

1. Create a virtualenv

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app (CLI helpers):

Initialize the database:

```bash
python -m app.main init-db
```

Create a sample company:

```bash
python -m app.main create-company --legal-name "Legal Ltd" --commercial-name "Legal" --code COM-00001
```
