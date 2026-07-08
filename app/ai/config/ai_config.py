import yaml
import os


CONFIG = "ags.yaml"


def load_ai_config():

    if not os.path.exists(CONFIG):

        return {}


    with open(CONFIG,"r",encoding="utf-8") as f:

        data = yaml.safe_load(f)


    return data.get(
        "ai",
        {}
    )