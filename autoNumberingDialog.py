import os.path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QCheckBox, QComboBox, QDialog, QFormLayout,
                                 QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                                 QSpacerItem, QSizePolicy, QDialogButtonBox, QLineEdit, QRadioButton)


class AutoNumberingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auto Numbering")
        self.setWindowIcon(QIcon(os.path.dirname(__file__)+'/icon.png'))
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
        self.label1.setText("Base Field")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label1)
        self.fieldCB = QComboBox(self)
        self.fieldCB.setObjectName("fieldCB")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fieldCB)
        self.rButton1 = QRadioButton("Modify exist field")
        self.rButton1.setObjectName("rButton1")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.rButton1)
        self.fieldCB1 = QComboBox(self)
        self.fieldCB1.setObjectName("fieldCB1")
        self.fieldCB1.setEnabled(False)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.fieldCB1)
        self.rButton2 = QRadioButton("Add new field")
        self.rButton2.setObjectName("rButton2")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.rButton2)
        self.newField = QLineEdit(self)
        self.newField.setObjectName("newField")
        self.newField.setPlaceholderText("Type new field name")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.newField)
        horizontalSpacer = QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.formLayout.addItem(horizontalSpacer)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Run")
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.buttonBox)

        
        

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)    # vertical spacer
        self.formLayout.addItem(verticalSpacer)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))