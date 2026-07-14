import json
from pathlib import Path
from datetime import datetime

from app.ai.self_developer.compiler.validator import CodeValidator
from app.ai.self_developer.compiler.error_reader import ErrorReader
from app.ai.self_developer.compiler.auto_fix import AutoFix



class CompilerRunner:


    def __init__(self):

        self.validator = CodeValidator()
        self.errors = ErrorReader()
        self.fix = AutoFix()



    def save_report(self, data):

        folder = Path(
            "build_reports"
        )

        folder.mkdir(
            exist_ok=True
        )


        name = (
            data["module"]
            + "_report.json"
        )


        (folder / name).write_text(

            json.dumps(
                data,
                indent=4,
                default=str
            ),

            encoding="utf8"
        )



    def run(self, folder, module="unknown"):


        results = self.validator.validate_folder(
            folder
        )


        fixed = []


        for item in results:


            if item["status"] == "error":


                error = self.errors.format(
                    item["error"]
                )


                result = self.fix.fix(
                    item["file"],
                    error
                )


                fixed.append(
                    result
                )



        report = {

            "status":"completed",

            "module":module,

            "time":datetime.now(),

            "validated":results,

            "fixed":fixed

        }


        self.save_report(
            report
        )


        return report
