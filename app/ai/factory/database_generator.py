class Generator:

    name="DATABASE_GENERATOR"

    def generate(self,module):
        return {
            "generator":self.name,
            "module":module,
            "status":"CREATED"
        }


generator=Generator()
