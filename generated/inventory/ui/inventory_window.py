from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton


class InventoryWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Inventory")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Inventory Module"))

        layout.addWidget(QPushButton("New"))

        layout.addWidget(QPushButton("Save"))

        layout.addWidget(QPushButton("Delete"))

        self.setLayout(layout)
