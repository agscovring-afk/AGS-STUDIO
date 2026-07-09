from app.ai.code_generation.generator import AICodeGenerator
from app.ai.writers.code_writer import CodeWriter
from app.ai.parser.code_parser import CodeParser


class AIProjectBuilder:

    def __init__(self):

        self.generator = AICodeGenerator()
        self.writer = CodeWriter()
        self.parser = CodeParser()


    def build(self,module):

        result=self.generator.generate(module)

        files=[]

        mapping={

            "architecture":("docs","md","extract_markdown"),

            "database":("database","sql","extract_sql"),

            "backend":("services","py","extract_python"),

            "ui":("ui","py","extract_python"),

            "testing":("tests","py","extract_python"),

            "documentation":("docs","md","extract_markdown")

        }


        for section,(folder,ext,method) in mapping.items():

            raw=result[section]["ai"]["response"]

            content=getattr(self.parser,method)(raw)

            files.append(

                self.writer.write(

                    module,

                    folder,

                    content,

                    ext

                )

            )

        return {

            "status":"success",

            "module":module,

            "files":files

        }
