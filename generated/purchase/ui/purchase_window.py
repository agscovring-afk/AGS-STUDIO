from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton


class PurchaseWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Purchase")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Purchase Module"))

        layout.addWidget(QPushButton("New"))

        layout.addWidget(QPushButton("Save"))

        layout.addWidget(QPushButton("Delete"))

        self.setLayout(layout)
