# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AutoNumbering
                                 A QGIS plugin
 Auto numbering is generating numbers by selected attribute.
                              -------------------
        begin                : 2020-06-07
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Hexa Apps
        email                : orucbe@itu.edu.tr
        version              : 0.2
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path

from qgis.core import QgsField, QgsMapLayer, QgsProject
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QMenu

from .autoNumberingDialog import AutoNumberingDialog


class AutoNumbering:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.instance = QgsProject.instance()
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir, 'i18n', 'AutoNumbering_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
        self.dlg = AutoNumberingDialog()
        self.dlg.rButton2.setChecked(True)
        self.actions = []
        self.menuTitle = self.tr(u'&Auto Numbering')
        self.toolbar = self.iface.addToolBar(u'Auto Numbering')
        self.toolbar.setObjectName(u'Auto Numbering')

    def tr(self, message):
        return QCoreApplication.translate('AutoNumbering', message)

    def initGui(self):
        icon_path = self.plugin_dir+'/images/icon.png'
        self.menu = QMenu(self.menuTitle)
        self.menu.setIcon(QIcon(icon_path))
        self.iface.vectorMenu().addMenu(self.menu)
        action = QAction(QIcon(icon_path), self.menuTitle, self.iface.mainWindow())
        action.triggered.connect(self.run)
        action.setEnabled(True)
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)
        self.dlg.layerCB.activated.connect(self.fillFieldCB)
        self.dlg.buttonBox.accepted.connect(self.runNumbering)
        self.dlg.buttonBox.rejected.connect(self.dlg.close)
        self.dlg.rButton1.toggled.connect(lambda: self.changeCurrField(self.dlg.rButton1.isChecked()))

    def unload(self):
        for action in self.actions:
            self.iface.removePluginVectorMenu(self.tr(u'&Auto Numbering'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        self.fillLayerCB()
        self.fillFieldCB()
        self.dlg.show()
        result = self.dlg.exec_()

    def msgBox(self, title, text, icon, infoText=None):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        if infoText is not None:
            msgBox.setInformativeText(infoText)
        msgBox.setIcon(icon)
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        return msgBox

    def modifyExistField(self, features, layer, field=None):
        msgBox = self.msgBox("Auto Numbering", "Field already exist!", QMessageBox.Warning, infoText="Existing values will be lost.")
        result = msgBox.exec_()
        if result == QMessageBox.Cancel:
            return
        else:
            if  field is None:
                fieldIdx = layer.fields().indexFromName(self.dlg.fieldCB1.currentText())
            else:
                fieldIdx = layer.fields().indexFromName(field)
            self.modifyAttrValue(features, layer, fieldIdx)

    def modifyAttrValue(self, features, layer, index=None, field=None):
        layer.startEditing()
        if field is None:
            [layer.changeAttributeValue(feat.id(), index, None) for feat in features]
        else:
            layer.addAttribute(QgsField(field, QVariant.Int))
            self.fillFieldCB()
            index = layer.fields().indexFromName(field)
        [layer.changeAttributeValue(feat.id(), index, idx+1) for idx, feat in enumerate(features)]
        layer.commitChanges()

    def runNumbering(self):
        state = self.dlg.fieldCB1.isEnabled()
        layer = self.dlg.layerCB.itemData(self.dlg.layerCB.currentIndex())
        field = self.dlg.fieldCB.itemData(self.dlg.fieldCB.currentIndex())
        fieldId = layer.fields().indexFromName(field.name())
        if self.dlg.orderCB.currentIndex() == 0:
            isReverse = False
        else:
            isReverse = True
        sortedFeatures = sorted(layer.getFeatures(), key=lambda feat: feat[fieldId], reverse=isReverse)
        if state and self.dlg.fieldCB1.currentText() != "":
            self.modifyExistField(sortedFeatures, layer)
        elif not state and self.dlg.newField.text() != "":
            allFields = [i.name() for i in layer.fields()]
            if self.dlg.newField.text() in allFields:
                self.modifyExistField(sortedFeatures, layer, self.dlg.newField.text())
            else:
                self.modifyAttrValue(sortedFeatures, layer, field=self.dlg.newField.text())

    def changeCurrField(self, state):
        self.dlg.fieldCB1.setEnabled(state)
        self.dlg.newField.setEnabled(not state)

    def fillLayerCB(self):
        self.dlg.layerCB.clear()
        for layer in self.instance.mapLayers().values():
            if layer.type() == QgsMapLayer.VectorLayer:
                self.dlg.layerCB.addItem(layer.name(), layer)

    def fillFieldCB(self):
        self.dlg.fieldCB.clear()
        self.dlg.fieldCB1.clear()
        currLayer = self.dlg.layerCB.itemData(self.dlg.layerCB.currentIndex())
        if currLayer is not None:
            [self.dlg.fieldCB.addItem(field.name(), field) for field in currLayer.fields()]
            [self.dlg.fieldCB1.addItem(field.name(), field) for field in currLayer.fields()]
