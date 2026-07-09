from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton


class SupplierWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Supplier")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Supplier Module"))

        layout.addWidget(QPushButton("New"))

        layout.addWidget(QPushButton("Save"))

        layout.addWidget(QPushButton("Delete"))

        self.setLayout(layout)
