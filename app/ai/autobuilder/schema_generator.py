class SchemaGenerator:

    def generate(self, request):

        if "tender" in request.lower():

            return {
                "module": "tenders",
                "tables": [
                    "tenders",
                    "tender_documents",
                    "boq_items",
                    "supplier_quotes",
                    "tender_evaluations"
                ]
            }

        return {
            "module": "custom_module",
            "tables": []
        }


schema_generator = SchemaGenerator()