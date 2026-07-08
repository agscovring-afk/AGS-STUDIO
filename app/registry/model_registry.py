import importlib


MODEL_REGISTRY = {}


def register_model(name):

    module = importlib.import_module(
        f"app.models.{name}"
    )


    class_name = ''.join(
        word.capitalize()
        for word in name.split('_')
    )


    model_class = getattr(
        module,
        class_name
    )


    MODEL_REGISTRY[name] = model_class


    return model_class



def get_model(name):

    if name not in MODEL_REGISTRY:

        register_model(name)


    return MODEL_REGISTRY.get(name)
