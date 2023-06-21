from PySide2.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PySide2.QtCore import Qt
from .animation_naming import AnimationNaming

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Animation Naming Tool")
        self.build_ui()
        self.init_connections()

    def build_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.actionLabel = QLabel("Action:")
        self.actionEdit = QLineEdit()
        self.layout.addWidget(self.actionLabel)
        self.layout.addWidget(self.actionEdit)

        self.directionLabel = QLabel("Direction:")
        self.directionEdit = QLineEdit()
        self.layout.addWidget(self.directionLabel)
        self.layout.addWidget(self.directionEdit)

        self.secondaryActionLabel = QLabel("Secondary Action:")
        self.secondaryActionEdit = QLineEdit()
        self.layout.addWidget(self.secondaryActionLabel)
        self.layout.addWidget(self.secondaryActionEdit)

        self.variantLabel = QLabel("Variant:")
        self.variantEdit = QLineEdit()
        self.layout.addWidget(self.variantLabel)
        self.layout.addWidget(self.variantEdit)

        self.metersLabel = QLabel("Meters:")
        self.metersEdit = QLineEdit()
        self.layout.addWidget(self.metersLabel)
        self.layout.addWidget(self.metersEdit)

        self.submitButton = QPushButton("Submit")
        self.layout.addWidget(self.submitButton)

    def init_connections(self):
        self.submitButton.clicked.connect(self.submit)

    def submit(self):
        action = self.actionEdit.text()
        direction = self.directionEdit.text() if self.directionEdit.text() != "" else None
        secondary_action = self.secondaryActionEdit.text() if self.secondaryActionEdit.text() != "" else None
        variant = int(self.variantEdit.text()) if self.variantEdit.text() != "" else None
        meters = int(self.metersEdit.text()) if self.metersEdit.text() != "" else None

        animation_naming = AnimationNaming(action, direction, secondary_action, variant, meters)
        print(animation_naming.create_name())
