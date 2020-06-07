from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (QComboBox, QDialog, QFormLayout, QLabel,
                                 QSizePolicy, QSpacerItem)


class AutoNumberingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 300)
        self.formLayout = QFormLayout(self)
        self.formLayout.setSpacing(12)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.label.setText("Layer")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.layerCB = QComboBox(self)
        self.layerCB.setObjectName("layerCB")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.layerCB)
        self.label1 = QLabel(self)
        self.label1.setObjectName("label1")
        self.label1.setText("Field")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label1)
        self.fieldCB = QComboBox(self)
        self.fieldCB.setObjectName("fieldCB")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fieldCB)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)    # vertical spacer
        self.formLayout.addItem(verticalSpacer)
