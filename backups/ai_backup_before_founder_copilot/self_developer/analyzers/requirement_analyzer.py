import re

from app.ai.self_developer.requirement import Requirement


class RequirementAnalyzer:


    def normalize_name(self, text):

        text = text.lower()


        mapping = {

            "factures fournisseurs": "supplier_invoices",
            "facture fournisseur": "supplier_invoice",
            "gestion des factures": "invoices",
            "clients": "clients",
            "customers": "customers",
            "stocks": "inventory",
            "stock": "inventory",
            "produits": "products",
            "commandes": "orders",
            "fournisseurs": "suppliers"

        }


        for key,value in mapping.items():

            if key in text:

                return value


        words = re.findall(
            r"[a-zA-Z0-9]+",
            text
        )


        return "_".join(words[:3])



    def analyze(self,text):

        name = self.normalize_name(
            text
        )


        return Requirement(

            name=name,

            description=text

        )
