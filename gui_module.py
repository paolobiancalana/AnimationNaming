from PySide2.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QTextEdit
from PySide2.QtCore import QTimer, Qt, QPoint
from PySide2.QtGui import QTextCharFormat
import re, json
from animation_naming import AnimationNaming
import al1mayautils, naming


class FetchingAsset():
    def __init__(self):
        self.nm = naming.Naming()

    def get_asset(self):
            data = {self.nm.parse(k).context['assetcode']:None for k in self.nm.search('dmvastcode')}
            self.data = data

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1 
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


class LevenshteinCompleterTextEdit(QTextEdit):
    def __init__(self, actions, parent=None):
        super().__init__(parent)
        self.actions = [a['name'] for a in actions]
        self.closest_match = ''
        self.user_input = ''
        self.is_updating = False
        self.build_ui()
        self.init_connections()

    def build_ui(self):
        self.setFixedHeight(24)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("""
        QTextEdit {
            border: 1px solid gray;
            border-radius: 2px;
        }
        """)
        self.suggestion_widget = QLabel(self)
        self.suggestion_widget.setStyleSheet("color: #808080;")
        self.suggestion_widget.hide()

    def init_connections(self):
        self.textChanged.connect(self.updateSuggestion)

    def updateSuggestion(self):
        if self.is_updating:
            return

        self.is_updating = True
        input_text = self.user_input
        if input_text:
            cursor_position = self.textCursor().position()

            # Calculate similarity for each action and filter those that have similarity over 90%
            filtered_actions = [(action, 1 - levenshtein_distance(input_text, action) / max(len(input_text), len(action))) for action in self.actions if action.startswith(input_text[0])]
            filtered_actions = [action for action, similarity in filtered_actions if similarity > 0.75][:10]

            if filtered_actions:
                self.closest_match = min(filtered_actions, key=lambda x: levenshtein_distance(input_text, x))
            self.showSuggestion()
            cursor = self.textCursor()
            cursor.setPosition(cursor_position)
            self.setTextCursor(cursor)
        else:
            self.clear()

        self.is_updating = False


    def showSuggestion(self):
        input_text = self.user_input
        if input_text:
            completer = self.closest_match[len(input_text):] if self.closest_match.startswith(input_text) else ""

            if completer:
                self.blockSignals(True)  # Block signals temporarily
                self.clear()
                self.insertPlainText(input_text)  # Insert user input as plain text
                self.textCursor().insertHtml("<span style='color: #808080;'>" + completer + "</span>")  # Insert suggestion as HTML
                self.setCurrentCharFormat(QTextCharFormat())  # Reset text format
                self.blockSignals(False)  # Unblock signals
        else: 
            self.clear()
            self.setCurrentCharFormat(QTextCharFormat())


    def completeText(self):
        self.user_input += self.closest_match[len(self.user_input):]
        self.setText(self.user_input)

    def keyPressEvent(self, event):
        if event.text().isalnum() or event.key() == Qt.Key_Backspace:  # Check if the event text is alphanumeric
            if event.key() == Qt.Key_Backspace and self.user_input:
                self.user_input = self.user_input[:-1]
            elif event.text().isalnum():
                self.user_input += event.text()

        if event.key() == Qt.Key_Tab:
            self.completeText()
            if len(self.user_input) > 0:
                cursor = self.textCursor()
                cursor.setPosition(len(self.user_input))  # Set the cursor position to the end
                self.setTextCursor(cursor)
                self.focusNextChild()  # Change focus to the next element in the UI
                return
        else:
            super().keyPressEvent(event)
        print(self.user_input)
        self.updateSuggestion()

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or al1mayautils.maya_main_window())
        self.setWindowTitle("Animation Naming Tool")

        with open("P:\\temp\\AnimationNaming\\actions.json") as f:
            self.data = json.load(f)
        
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
        self.actionEdit = LevenshteinCompleterTextEdit(self.data['actions'])
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
