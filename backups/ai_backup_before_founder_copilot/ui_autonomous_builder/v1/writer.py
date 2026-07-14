class UIWriter:

    def write(self, generated):
        return {
            "writer": "UI_WRITER_V1",
            "written": generated.get("files", []),
            "status": "COMPLETED"
        }
