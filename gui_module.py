from PySide2.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QSpinBox, QFormLayout, QHBoxLayout, QFrame
from PySide2.QtCore import QTimer
from PySide2 import QtCore
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
        self.layout.addWidget(self.metersLabel)
        self.Xspin = QSpinBox()
        self.Xspin.setRange(0, 100)
        self.Yspin = QSpinBox()
        self.Yspin.setRange(0, 100)
        xFormLayout = QFormLayout()
        xFormLayout.addRow(self.tr("x value:"), self.Xspin)
        yFormLayout = QFormLayout()
        yFormLayout.addRow(self.tr("y value:"), self.Yspin)
        HLayout = QHBoxLayout()
        HLayout.addLayout(xFormLayout)
        HLayout.addLayout(yFormLayout)
        
        self.layout.addLayout(HLayout)
        
        self.suffix = QLabel("Suffix:")
        self.suffixEdit = QLineEdit()
        self.layout.addWidget(self.suffix)
        self.layout.addWidget(self.suffixEdit)

        self.ButtonsLayout = QHBoxLayout()

        self.generateButton = QPushButton("Nice Name")
        self.ButtonsLayout.addWidget(self.generateButton)

        self.submitButton = QPushButton("Long Name")
        self.ButtonsLayout.addWidget(self.submitButton)
        self.layout.addLayout(self.ButtonsLayout)

        self.message_field = QLabel()
        self.message_field.setFrameStyle(QFrame.NoFrame)
        self.message_field.setStyleSheet("border-radius: 5px; border: 1px transparent;")
        self.message_field.setAlignment(QtCore.Qt.AlignCenter)
        self.message_field.setFixedHeight(30)
        self.layout.addWidget(self.message_field)
        
    def init_connections(self):
        self.submitButton.clicked.connect(lambda: self.submit('long'))
        self.generateButton.clicked.connect(lambda: self.submit('nice'))

    def fetch_assets(self):
        fetching_asset = FetchingAsset()
        fetching_asset.get_asset()
        self.assets = list(fetching_asset.data.keys())

    def submit(self, param):
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
        meters = str(self.Xspin.value())+','+str(self.Yspin.value()) if self.Xspin.value() != 0 or self.Yspin.value() != 0 else None
        suffix = self.suffixEdit.text() if self.suffixEdit.text() != "" else None
        animation_naming = AnimationNaming()

        if param == 'long':
            self.message_field.setText(animation_naming.encoder(action=action,  direction=direction, secondary_action=secondary_action, variant=variant, meters=meters, suffix=suffix))
        else:
            self.message_field.setText(animation_naming.simplifier(animation_naming.encoder(action=action,  direction=direction, secondary_action=secondary_action, variant=variant, meters=meters, suffix=suffix)))

        
