from .model_generator import ModelGenerator
from .repository_generator import RepositoryGenerator
from .service_generator import ServiceGenerator
from .controller_generator import ControllerGenerator



class CodeFactory:


    def __init__(self):

        self.model = ModelGenerator()

        self.repository = RepositoryGenerator()

        self.service = ServiceGenerator()

        self.controller = ControllerGenerator()



    def generate(self, metadata):

        result = {}


        for entity in metadata["entities"]:

            result[entity.name] = {

                "model":
                    self.model.generate(entity),

                "repository":
                    self.repository.generate(entity),

                "service":
                    self.service.generate(entity),

                "controller":
                    self.controller.generate(entity)
            }


        return result
