from app.ai.autonomous.quality.sanitizer import sanitizer


class QualityFixer:


    def fix_class(
        self,
        module,
        layer
    ):

        name = sanitizer.class_name(
            module + "_" + layer
        )


        return f"class {name}:\n    pass\n"



fixer = QualityFixer()
