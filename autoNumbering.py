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
        version              : 0.1
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
from qgis.PyQt.QtWidgets import QAction, QMessageBox

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
        self.menu = self.tr(u'&Auto Numbering')
        self.toolbar = self.iface.addToolBar(u'Auto Numbering')
        self.toolbar.setObjectName(u'Auto Numbering')

    def tr(self, message):
        return QCoreApplication.translate('AutoNumbering', message)

    def add_action(self,icon_path,text,callback,enabled_flag=True,add_to_menu=True,add_to_toolbar=True,status_tip=None,whats_this=None,parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None: action.setStatusTip(status_tip)
        if whats_this is not None: action.setWhatsThis(whats_this)
        if add_to_toolbar: self.toolbar.addAction(action)
        if add_to_menu: self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = self.plugin_dir+'/icon.png'
        self.add_action(icon_path, text=self.tr(u'Auto number'), callback=self.run, parent=self.iface.mainWindow())
        self.dlg.layerCB.activated.connect(self.fillFieldCB)
        self.dlg.buttonBox.accepted.connect(self.runNumbering)
        self.dlg.buttonBox.rejected.connect(self.dlg.close)
        self.dlg.rButton1.toggled.connect(lambda: self.changeCurrField(self.dlg.rButton1.isChecked()))

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Auto Numbering'), action)
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

    def modifyExistField(self, layer, field=None):
        msgBox = self.msgBox("Auto Numbering", "Field already exist!", QMessageBox.Warning, infoText="Existing values will be lost.")
        result = msgBox.exec_()
        if result == QMessageBox.Cancel:
            return
        else:
            if  field is None:
                fieldIdx = layer.fields().indexFromName(self.dlg.fieldCB1.currentText())
            else:
                fieldIdx = layer.fields().indexFromName(field)
            self.modifyAttrValue(layer, fieldIdx)

    def modifyAttrValue(self, layer, index=None, field=None):
        layer.startEditing()
        if field is None:
            [layer.changeAttributeValue(feat.id(), index, None) for feat in layer.getFeatures()]
        else:
            layer.addAttribute(QgsField(field, QVariant.Int))
            self.fillFieldCB()
            index = layer.fields().indexFromName(field)
        [layer.changeAttributeValue(feat.id(), index, idx+1) for idx, feat in enumerate(layer.getFeatures())]
        layer.commitChanges()

    def runNumbering(self):
        state = self.dlg.fieldCB1.isEnabled()
        layer = self.dlg.layerCB.itemData(self.dlg.layerCB.currentIndex())
        field = self.dlg.fieldCB.itemData(self.dlg.fieldCB.currentIndex())
        fieldId = layer.fields().indexFromName(field.name())
        sortedFeatures = sorted(layer.getFeatures(), key=lambda feat: feat[fieldId])
        if state and self.dlg.fieldCB1.currentText() != "":
            self.modifyExistField(layer)
        elif not state and self.dlg.newField.text() != "":
            allFields = [i.name() for i in layer.fields()]
            if self.dlg.newField.text() in allFields:
                self.modifyExistField(layer, self.dlg.newField.text())
            else:
                self.modifyAttrValue(layer, field=self.dlg.newField.text())

            
        # attributeIndex = layer.fields().indexFromName(seld.dlg.)
        # for value, feature in sortedFeatures:
        #     layer.changeAttributeValue(feature.id(), )

        print([featt[field.name()] for featt in sortedFeatures])

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
