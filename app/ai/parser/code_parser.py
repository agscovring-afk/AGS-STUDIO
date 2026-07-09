class CodeParser:

    def extract_python(self,text):

        if "`python" in text:

            return text.split("`python")[1].split("`")[0].strip()

        return text.strip()


    def extract_sql(self,text):

        if "`sql" in text:

            return text.split("`sql")[1].split("`")[0].strip()

        return text.strip()


    def extract_markdown(self,text):

        if "`markdown" in text:

            return text.split("`markdown")[1].split("`")[0].strip()

        return text.strip()
