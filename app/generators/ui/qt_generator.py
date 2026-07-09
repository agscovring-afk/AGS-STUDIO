from pathlib import Path


class QtGenerator:

    def generate(self,module):

        module = module.lower()

        cls = module.capitalize()

        path = Path("generated") / module / "ui"

        path.mkdir(parents=True, exist_ok=True)

        py = f'''from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton


class {cls}Window(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("{cls}")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("{cls} Module"))

        layout.addWidget(QPushButton("New"))

        layout.addWidget(QPushButton("Save"))

        layout.addWidget(QPushButton("Delete"))

        self.setLayout(layout)
'''

        ui = f'''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
<class>{cls}Window</class>
<widget class="QWidget" name="{cls}Window"/>
<resources/>
<connections/>
</ui>
'''

        pyfile = path / f"{module}_window.py"
        uifile = path / f"{module}.ui"

        pyfile.write_text(py,encoding="utf8")
        uifile.write_text(ui,encoding="utf8")

        return {
            "generator":"QtGenerator",
            "status":"success",
            "files":[
                str(pyfile),
                str(uifile)
            ]
        }
