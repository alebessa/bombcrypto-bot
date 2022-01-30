from PyQt6 import QtCore, QtGui, QtWidgets
from shared import log_color_map


class Ui_Quick_Message(object):

    _id = 0
    color_map = log_color_map

    def __init__(self, parent, dialog_type, message, timeout=4):
        self.parent = parent
        self.dialog_type = dialog_type
        self.message = message
        self.timeout = timeout
        self.color = self.color_map[dialog_type]
        Ui_Quick_Message._id += 1
        self.id = Ui_Quick_Message._id

    def setupUi(self, Dialog: QtWidgets.QDialog):
        Dialog.setObjectName(f'message_box_{self._id}')
        Dialog.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        self.timer = QtCore.QTimer(Dialog)
        self.timer.singleShot(self.timeout * 1000, Dialog.accept)

        self.message_label = QtWidgets.QLabel(Dialog)
        self.message_label.setText(self.message)
        self.message_label.setFont(QtGui.QFont('Comic Sans MS', 11))
        self.message_label.setStyleSheet(f"""
            margin: 0;
            color: {self.color.font};
            background-color: {self.color.background};
            border: 3px {self.color.border}"""
        )
        self.message_label.adjustSize()
        Dialog.adjustSize()
        self.message_label.setObjectName('message_label')

        px = self.parent.pos().x()
        py = self.parent.pos().y()
        wp = self.parent.width()
        wd = Dialog.width()

        Dialog.move(px + int((wp - wd) / 2), py)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Donation Info"))
        Dialog.setWindowIcon(QtGui.QIcon("images:donation.png"))

    def copy_donate_address(self):
        clip_mode = QtGui.QClipboard.Mode.Clipboard

        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=clip_mode)
        cb.setText(self.address, mode=clip_mode)


def quick_message(parent, message_type, message, timeout=4):
    Dialog = QtWidgets.QDialog()
    ui = Ui_Quick_Message(parent, message_type, message, timeout)
    ui.setupUi(Dialog)
    Dialog.show()
    Dialog.exec()