# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AutoNumbering
                                 A QGIS plugin
 Auto numbering is generating numbers by selected attribute.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-06-07
        copyright            : (C) 2020 by Hexa Apps
        email                : orucbe@itu.edu.tr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AutoNumbering class from file AutoNumbering.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .autoNumbering import AutoNumbering
    return AutoNumbering(iface)
