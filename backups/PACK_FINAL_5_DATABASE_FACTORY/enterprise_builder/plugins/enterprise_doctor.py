from enterprise_builder.core.enterprise_validator import EnterpriseValidator
from enterprise_builder.core.enterprise_report import EnterpriseReport


class EnterpriseDoctor:


    def run(self):

        validator = EnterpriseValidator()

        report = EnterpriseReport()


        result = validator.validate()


        return report.generate(result)