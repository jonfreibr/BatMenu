#!/usr/bin/env python3
"""
Program : BatMenu
Author  : Jon Freivald <jfreivald@brmedical.com>
        : Copyright © Blue Ridge Medical Center, 2024. All Rights Reserved.
        : License: Creative Commons
Date    : 2024-06-05
Purpose : GUI Menu wrapper for batch files
        : Version change log at EoF.
"""

import os
import sys

from PySide6.QtGui import (
    QFont,
)

from PySide6 import (
    QtCore,
)

from PySide6.QtCore import (
    QPoint,
    QProcess,
    QSettings,
    QSize,
)

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

progver = '2.0'
brmc_dark_blue = '#00446a'
brmc_medium_blue = '#73afb6'
brmc_gold = '#ffcf01'
brmc_rust = '#ce7067'
brmc_warm_grey = '#9a8b7d'
light_grey = '#d3d3d3'
flat_white = '#e7e7e7'

buttons = []

# The following 2 lines are required in case we are running with pythonw.exe
if sys.stdout is None: sys.stdout = open(os.devnull, "w")
if sys.stderr is None: sys.stderr = open(os.devnull, "w")

def listbats():
    files = []
    for f in os.listdir():
        if f.endswith(".bat"):
            files.append(f)
    return files

class Scripts:
    def __init__(self, script):
        self.name = script.strip('.bat')
        self.script = script

        self.button = QPushButton(self.name)
        self.button.setStyleSheet(f'background-color: {brmc_dark_blue}; color: {brmc_gold}')
        self.button.clicked.connect(self.display)

    def get_button(self):
        return self.button

    def display(self):
        self.out = DataWindow(self.name, self.script)
        self.out.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            with open("batmenu.cfg", 'r') as fp:
                win_title = fp.readline()
        except:
            win_title = "Batch File Menu System"

        self.settings = QSettings("Blue Ridge MEdical Center", "Jon's Backup System 2.0")
        self.resize(self.settings.value('MainWIndowSize', QSize(180, 30)))
        self.move(self.settings.value('MainWindowPos', QPoint(50, 50)))

        self.setStyleSheet(f'background-color: {brmc_medium_blue}')

        self.setWindowTitle(f"{win_title}, v {progver}")
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        for file in listbats():
            buttons.append(Scripts(file))
        
        for b in buttons:
            layout.addWidget(b.get_button())

    def closeEvent(self, a0):
        self.settings.setValue('MainWindowSize', self.size())
        self.settings.setValue('MainWindowPos', self.pos())
        return super().closeEvent(a0)
    
class DataWindow(QWidget):
    def __init__(self, name, file):
        super().__init__()
        self.name = name
        self.file = file

        self.settings = QSettings("Blue Ridge MEdical Center", "Jon's Backup System 2.0")
        self.resize(self.settings.value(f'{self.name}WIndowSize', QSize(180, 30)))
        self.move(self.settings.value(f'{self.name}WindowPos', QPoint(50, 50)))
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(f'background-color: {brmc_medium_blue}')

        self.p = None
        self.current_process = None

        self.text = QTextEdit()
        font = QFont("Cascadia Code", 10)
        self.text.setFont(font)
        self.text.setStyleSheet(f'background-color: {flat_white}; color: black')
        self.cursor = self.text.textCursor()
        self.cursor.setPosition(0)
        self.text.setTextCursor(self.cursor)
        self.text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)

        self.current_process = name
        self.start_process(name, file)

    def message(self, s):
        self.text.insertPlainText(s)
        self.text.setTextCursor(self.cursor)

    def start_process(self, which, file):
        self.which = which
        if self.p is None:  # No process running.
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("cmd", ['/c', file])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode(sys.stdout.encoding)
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode(sys.stdout.encoding)
        self.message(stdout)

    def handle_state(self, state):
        if QProcess.Running:
            self.setWindowTitle(f"Jon's Backup System, v {progver} ({self.current_process} running)")
    #     states = {
    #         QProcess.NotRunning: 'Not running',
    #         QProcess.Starting: 'Starting',
    #         QProcess.Running: 'Running',
    #     }
    #     state_name = states[state]
    #     self.message(f"State changed: {state_name}\n")

    def process_finished(self):
        # self.message("Process finished.\n")
        self.setWindowTitle(f"Jon's Backup System, v {progver} ({self.current_process} finished)")
        self.p = None

    def closeEvent(self, a0):
        self.settings.setValue(f'{self.name}WindowSize', self.size())
        self.settings.setValue(f'{self.name}WindowPos', self.pos())
        return super().closeEvent(a0)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

"""
change log:

v 0.1   : 240605    : Blatantly stolen from the Internet and modified to fit my purposes.
v 0.2   : 240605    : Updated UI to be able to clear output area.
v 0.3   : 240605    : Added standard header and PySimpleGUI distribution license.
v 0.4   : 240611    : Added option to backup Renee's ADMIN share
v 0.5   : 250103    : Expanded window to deal with output from robocopy
v 0.6   : 250305    : Removed reverse-mirror option -- media needs to be dedicated to the backup scheme
v 0.7   : 250811    : Re-write migrating from PySimpleGUI to PySide6.
v 1.0   : 250812    : Encountered issue with pythonw.exe and stdout/stderr. Finished re-write.
v 1.01  : 250818    : Tweaking the interface.
v 2.0   : 250923    : Major refactor to dynamically create menu based on .bat files found in CWD.
"""