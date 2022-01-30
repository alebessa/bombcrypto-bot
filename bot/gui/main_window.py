from PyQt6 import QtCore, QtGui, QtWidgets
from engine import FuzzyBomberEngine

from gui.donate_dialog import Ui_Donate_Dialog
from gui.quick_message import quick_message

class Ui_MainWindow(object):

    def __init__(self, engine: FuzzyBomberEngine):
        self.engine = engine
        self.log_bridge = None

    def setupUi(self, MainWindow):

        self.MainWindow = MainWindow
        
        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(428, 507)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))

        self.log_bridge = QtCore.QTimer(MainWindow)
        self.log_bridge.setInterval(1000)
        self.log_bridge.timeout.connect(self.check_log)
        self.log_bridge.start()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 6, -1, -1)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")


        # Title box
        self.title_box = QtWidgets.QHBoxLayout()
        self.title_box.setObjectName("title_box")
        self.title_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_box.addStretch()
        
        # Bcoin gif left
        self.bcoin_box = QtWidgets.QLabel(self.centralwidget)
        self.bcoin_box.setMinimumSize(QtCore.QSize(66, 66))
        self.bcoin_box.setMaximumSize(QtCore.QSize(66, 66))
        self.bcoin = QtGui.QMovie('images:bcoin.gif')
        self.bcoin.setScaledSize(QtCore.QSize(60, 60))
        self.bcoin_box.setMovie(self.bcoin)
        self.bcoin_box.setToolTip('🤑💲💰')
        self.bcoin.start()
        self.title_box.addWidget(self.bcoin_box)

        # Title
        self.bot_title = QtWidgets.QLabel(self.centralwidget)
        self.bot_title_art = QtGui.QImage()
        self.bot_title_art.load('images:bot_title.png')
        bot_title_pix_map = QtGui.QPixmap.fromImage(self.bot_title_art)
        self.bot_title.setPixmap(bot_title_pix_map.scaledToWidth(300))
        self.bot_title.setToolTip('💣💣weeeeeeeee!!💣💣')
        self.bot_title.setObjectName("bot_title")
        self.title_box.addWidget(self.bot_title)

        # Bcoin gif right
        self.bcoin_box2 = QtWidgets.QLabel(self.centralwidget)
        self.bcoin_box2.setMinimumSize(QtCore.QSize(66, 66))
        self.bcoin_box2.setMaximumSize(QtCore.QSize(66, 66))
        self.bcoin2 = QtGui.QMovie('images:bcoin.gif')
        self.bcoin2.setScaledSize(QtCore.QSize(60, 60))
        self.bcoin_box2.setMovie(self.bcoin2)
        self.bcoin_box2.setToolTip('🤑💲💰')
        self.bcoin2.start()
        self.title_box.addWidget(self.bcoin_box2)

        
        self.title_box.addStretch()
        
        self.gridLayout.addLayout(self.title_box, 0, 0, 1, 4)


        # Configs button
        self.configs_button = QtWidgets.QPushButton(self.centralwidget)
        self.configs_button.setMinimumSize(QtCore.QSize(48, 48))
        self.configs_button.setMaximumSize(QtCore.QSize(48, 48))
        self.configs_button.setText("")
        self.configs_button.setIcon(QtGui.QIcon('images:configs_icon.png'))
        self.configs_button.setIconSize(QtCore.QSize(40, 40))

        self.configs_button.setEnabled(False)
        self.configs_button.setToolTip('🚧 Under construction... 🚧')
        
        self.configs_button.setObjectName("configs_button")
        self.gridLayout.addWidget(self.configs_button, 2, 3, 1, 1)


        # Find games button
        self.find_games_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_games_button.setMinimumSize(QtCore.QSize(158, 58))
        self.find_games_button.setMaximumSize(QtCore.QSize(158, 58))
        self.find_games_button.setIcon(QtGui.QIcon('images:find_games.png'))
        self.find_games_button.setIconSize(QtCore.QSize(150, 50))
        self.find_games_button.setObjectName("find_games_button")
        self.find_games_button.clicked.connect(self.find_games)
        self.gridLayout.addWidget(self.find_games_button, 2, 0, 1, 1)

        # Start button
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setMinimumSize(QtCore.QSize(158, 58))
        self.start_button.setMaximumSize(QtCore.QSize(158, 58))
        self.start_button.setIcon(QtGui.QIcon('images:start.png'))
        self.start_button.setIconSize(QtCore.QSize(150, 50))
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.start)
        self.start_button.setEnabled(False)
        self.start_button.setVisible(False)
        self.gridLayout.addWidget(self.start_button, 2, 0, 1, 1)
        
        
        # Resume button
        self.resume_button = QtWidgets.QPushButton(self.centralwidget)
        self.resume_button.setMinimumSize(QtCore.QSize(108, 58))
        self.resume_button.setMaximumSize(QtCore.QSize(108, 58))
        self.resume_button.setIcon(QtGui.QIcon('images:resume.png'))
        self.resume_button.setIconSize(QtCore.QSize(100, 50))
        self.resume_button.setObjectName("resume_button")
        self.resume_button.clicked.connect(self.engine.resume)
        
        self.resume_button.setEnabled(False)
        self.resume_button.setToolTip('🚧 Under construction... 🚧')

        self.gridLayout.addWidget(self.resume_button, 3, 0, 1, 1)


        # Pause button
        self.pause_button = QtWidgets.QPushButton(self.centralwidget)
        self.pause_button.setMinimumSize(QtCore.QSize(88, 48))
        self.pause_button.setMaximumSize(QtCore.QSize(88, 48))
        self.pause_button.setIcon(QtGui.QIcon('images:pause.png'))
        self.pause_button.setIconSize(QtCore.QSize(80, 40))
        self.pause_button.setObjectName("pause_button")
        self.pause_button.clicked.connect(self.engine.pause)

        self.pause_button.setEnabled(False)
        self.pause_button.setToolTip('🚧 Under construction... 🚧')

        self.gridLayout.addWidget(self.pause_button, 4, 0, 1, 1)


        # Donate image
        self.donate_img = QtWidgets.QPushButton(self.centralwidget)
        self.donate_img.setMinimumSize(QtCore.QSize(100, 100))
        self.donate_img.setMaximumSize(QtCore.QSize(100, 100))
        self.donate_img.setStyleSheet("border-image: url(images:fuzzybomber.png);")
        self.donate_img.setText("")
        self.donate_img.setObjectName("donate_img")
        self.gridLayout.addWidget(self.donate_img, 6, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)


        # Donate button
        self.donate_button = QtWidgets.QPushButton(self.centralwidget)
        self.donate_button.setMinimumSize(QtCore.QSize(208, 56))
        self.donate_button.setMaximumSize(QtCore.QSize(208, 56))
        self.donate_button.setIcon(QtGui.QIcon('images:plsdonate.png'))
        self.donate_button.setIconSize(QtCore.QSize(200, 48))
        self.donate_button.setObjectName("donate_button")
        self.donate_button.setToolTip('Ugh.. do-donate pwease...? 😳👉👈')
        self.donate_button.clicked.connect(self.show_donate_dialog)

        self.gridLayout.addWidget(self.donate_button, 7, 0, 1, 1)


        # spacers

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def find_games(self):
        
        self.find_games_button.setEnabled(False)

        if self.engine.find_games():
            self.find_games_button.setVisible(False)
            self.start_button.setVisible(True)
            self.start_button.setEnabled(True)
        else:
            self.find_games_button.setEnabled(True)

    def start(self):
        
        self.start_button.setVisible(False)
        self.start_button.setEnabled(False)
        self.engine.start()

    def check_log(self):
        if log := self.engine.pull_log():
            quick_message(self.MainWindow, **log)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FuzzyBomber"))
        MainWindow.setWindowIcon(QtGui.QIcon("images:bcoin_icon.png"))

    def show_donate_dialog(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Donate_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec()