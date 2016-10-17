#!/usr/bin/env python

import sys
import random
import os
from PySide import QtGui, QtCore, QtSvg
from brown.clef import Clef
from brown.note_column import NoteColumn
from brown.staff import Staff, StaffAttributeSet
from brown.notehead import Notehead
from brown.testing_view import TestingView
from brown.beam import BeamGlyph

import time
start_time = time.time()

# Dummy application set-up
app = QtGui.QApplication(sys.argv)
window = TestingView()
window.scale(2.0, 2.0)

window.setGeometry(300, 100, 640, 480)
window.setWindowTitle('Test Window')
window.show()

# Register the Gonville Font
font_db = QtGui.QFontDatabase()
# TODO: Make sure that docs mention that on Linux (maybe Mac too???), fonts must be installed on the system to use
gonville_font_path = os.path.join('brown', 'resources', 'Fonts', 'Gonville',
                                  'otf', 'gonville-11.otf')
font_db.addApplicationFont(gonville_font_path)

scene = QtGui.QGraphicsScene()
window.setScene(scene)
# scene.addText('hello world!')
# staff = StaffGlyph(200, scene=scene)
# notehead = NoteheadGlyph(scene=scene)

# Example implementation
staff = Staff(None, scene, 0, 0, 120, 3)
staff.add_cutout_region(30, 5)
# staff.build_glyph()
# staff.add_attribute_set(15, 16, False, 3, 5, 0.05)
# staff.add_attribute_revert_to_previous(30, 50)

clef = Clef(staff, 'treble', 0)
nc1 = NoteColumn(staff, 20, [], '64...')
nc1.contents.append(Notehead((25, 'c'), 'open normal', nc1))
nc1.contents.append(Notehead((23, 'b'), 'open normal', nc1))

nc1.build_glyph()

# del nc1

nc2 = NoteColumn(staff, 50, [], '16...')
nc2.contents.append(Notehead((-6, 'g'), 'open normal', nc2))
nc2.build_glyph()

# test_beam = BeamGlyph(None, scene, 100, 150, 100, 70, 8)

# Save the file
dpi = 72
width = int(scene.sceneRect().size().width()) * (dpi / 72.0)
height = int(scene.sceneRect().size().height()) * (dpi / 72.0)

scene.setBackgroundBrush(QtCore.Qt.white)

######################## PNG Export ##################################
image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
painter = QtGui.QPainter(image)
painter.setRenderHint(QtGui.QPainter.Antialiasing)

scene.render(painter)
painter.end()
image.save('testimage.png', quality=20)

######################### SVG Export #################################
# generator = QtSvg.QSvgGenerator()
# generator.setFileName('testsvg.svg')
# generator.setSize(QtCore.QSize(width, height))
# painter = QtGui.QPainter()
# painter.begin(generator)
# scene.render(painter)
# painter.end()

print(
    'File built & exported in %s ms' % str((time.time() - start_time) * 1000.0))

app.exec_()
