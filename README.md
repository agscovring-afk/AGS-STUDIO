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

## Project layout

- `app/` - the ERP application (models, repositories, services, UI, AI engine)
- `ags/` - the AGS CLI / plugin runtime (`python ags.py`)
- `agents/`, `generators/`, `templates/` - code-generation agents and Jinja templates
- `generated/` - modules produced by the generators
- `data/` - project memory and analysis files read by the AI tools
- `scripts/` - one-off helper scripts (night builders, installers, demos)
- `tests/` - pytest suite (`python -m pytest`)
- `docs/` - requirements, vision and design documents

Generated outputs (`reports/`, `night_build/`, `night_worker/`, `*.db`, `__pycache__/`,
archives and `*_backup.py` files) are ignored by git. Create the local database with:

```bash
python -m app.database.run_migrations
```
