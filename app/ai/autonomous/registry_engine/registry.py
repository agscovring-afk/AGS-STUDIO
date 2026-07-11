from ..engine_base import EngineBase
from ..workers.bridge import bridge
import json


class RegistryEngine(EngineBase):

    name = "AUTO_REGISTRY_ENGINE_V1"


    def run(self, context):

        if isinstance(context, str):
            module = context.replace("CREATE ERP MODULE", "").strip().lower().replace(" ", "_")
        else:
            module = context.get("module", "module")

        registry = {
            "module": module,
            "controller": f"{module}_controller",
            "service": f"{module}_service",
            "model": f"{module}",
            "ui": f"{module}_page",
            "status": "registered"
        }

        result = bridge.dispatch(
            "file_creator",
            {
                "files": [
                    {
                        "path": f"generated/modules/{module}/registry/registry.json",
                        "content": json.dumps(registry, indent=4)
                    }
                ]
            }
        )

        return {
            "engine": self.name,
            "status": "completed",
            "module": module,
            "result": result
        }
