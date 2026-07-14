import re


class CodeSanitizer:


    def class_name(self, value):

        value = value.replace(
            "/",
            "_"
        )


        value = re.sub(
            r'[^a-zA-Z0-9_]',
            '',
            value
        )


        parts = value.split("_")


        return "".join(
            x.title()
            for x in parts
            if x
        )



sanitizer = CodeSanitizer()
