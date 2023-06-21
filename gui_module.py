from PySide2.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox
from PySide2.QtCore import QTimer
import re
from animation_naming import AnimationNaming
import al1mayautils, naming


class FetchingAsset():
    def __init__(self):
        self.nm = naming.Naming()

    def get_asset(self):
            data = {self.nm.parse(k).context['assetcode']:None for k in self.nm.search('dmvastcode')}
            self.data = data

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or al1mayautils.maya_main_window())
        self.setWindowTitle("Animation Naming Tool")
        self.build_ui()
        self.init_connections()

    def build_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.assetLabel = QLabel("Asset:")
        self.assetComboBox = QComboBox()
        self.layout.addWidget(self.assetLabel)
        self.layout.addWidget(self.assetComboBox)

        self.fetch_assets()
        for asset in self.assets:
            self.assetComboBox.addItem(asset)

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

    def fetch_assets(self):
        fetching_asset = FetchingAsset()
        fetching_asset.get_asset()
        self.assets = list(fetching_asset.data.keys())

    def submit(self):
        asset = self.assetComboBox.currentText()
        action = self.actionEdit.text()
        direction = self.directionEdit.text() if self.directionEdit.text() != "" else None
        secondary_action = self.secondaryActionEdit.text() if self.secondaryActionEdit.text() != "" else None
        variant = self.variantEdit.text() if self.variantEdit.text() != "" else None
        if variant and variant.isdigit():
            variant = int(variant)
        elif variant is None:
            pass
        else:
            QTimer.singleShot(0, lambda: self.variantEdit.clear())
            self.variantEdit.setPlaceholderText("Please, insert a number. ex: 1 ")
            return
        meters = self.metersEdit.text() if self.metersEdit.text() != "" else None
        if meters:
            if not re.search(r',', meters):
                QTimer.singleShot(0, lambda: self.metersEdit.clear())
                self.metersEdit.setPlaceholderText("Please split with a comma. ex: 4,0 ")
                return
        animation_naming = AnimationNaming(action, direction, secondary_action, variant, meters)
        print(animation_naming.create_name())

