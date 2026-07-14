class PromptFactory:

    def model(self,module):

        return f"""
Generate ONLY valid Python code.

Create SQLAlchemy model for ERP module {module}.

Requirements:

- class name {module.capitalize()}
- id
- code
- name
- description
- created_at
- updated_at

Return ONLY python code.
"""


    def service(self,module):

        return f"""
Generate ONLY Python CRUD Service.

Module:

{module}

Return ONLY python code.
"""


    def api(self,module):

        return f"""
Generate ONLY FastAPI router.

Module:

{module}

Return ONLY python code.
"""


    def ui(self,module):

        return f"""
Generate ONLY PySide6 Window.

Module:

{module}

Return ONLY python code.
"""


    def database(self,module):

        return f"""
Generate ONLY SQLite CREATE TABLE script.

Module:

{module}

Return ONLY SQL.
"""
