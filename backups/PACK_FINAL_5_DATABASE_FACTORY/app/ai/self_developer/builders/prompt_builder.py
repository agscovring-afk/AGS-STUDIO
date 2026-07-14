class PromptBuilder:

    def build(self,requirement):

        return f'''
Create complete ERP module.

Name:
{requirement.name}

Description:
{requirement.description}

Generate:

Database
Metadata
CRUD
API
Qt UI
Validators
Tests
Documentation
'''
