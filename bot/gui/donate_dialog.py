from PyQt6 import QtCore, QtGui, QtWidgets

from gui.quick_message import quick_message

class Ui_Donate_Dialog(object):

    address = '0x136d4B54A17800B5D1D4172AeEcCf5e1E2bdeE59'
    
    def setupUi(self, Dialog):

        self.Dialog = Dialog

        Dialog.setObjectName('donateDialog')
        Dialog.resize(400, 100)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.address_label = QtWidgets.QLabel(Dialog)
        self.address_label.setText(self.address)
        self.address_label.setFont(QtGui.QFont('Comic Sans MS', 17))
        self.address_label.setStyleSheet('color: #e68ea0')
        self.address_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.address_label.setObjectName('address_label')
        layout.addWidget(self.address_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        
        self.copy_button = QtWidgets.QPushButton(Dialog)
        self.copy_button.setMinimumSize(QtCore.QSize(358, 58))
        self.copy_button.setMaximumSize(QtCore.QSize(358, 58))
        self.copy_button.setIcon(QtGui.QIcon('images:copy.png'))
        self.copy_button.setIconSize(QtCore.QSize(350, 50))
        self.copy_button.setObjectName("copy_button")
        self.copy_button.clicked.connect(self.copy_donate_address)
        layout.addWidget(self.copy_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        Dialog.setLayout(layout)
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

        quick_message(self.Dialog, 'love', '💕 Address copied to clipboard! 💕', 2)