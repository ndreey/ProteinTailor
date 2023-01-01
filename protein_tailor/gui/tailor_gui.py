from PyQt5 import QtCore, QtGui, QtWidgets
from program.protein_tailor import ProteinTailor


class GUI(object):
    
    # Builds UI from the .ui file
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(452, 646)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("grid_layout")
        self.in_lab = QtWidgets.QLabel(self.central_widget)
        self.in_lab.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.in_lab.setFont(font)
        self.in_lab.setObjectName("in_lab")
        self.grid_layout.addWidget(self.in_lab, 0, 0, 1, 1)        
        
        # combo_box
        self.combo_box = QtWidgets.QComboBox(self.central_widget)
        self.combo_box.setObjectName("combo_box")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")        
        self.grid_layout.addWidget(self.combo_box, 0, 1, 1, 1)
        
        # Text input
        self.seq_box = QtWidgets.QPlainTextEdit(self.central_widget)
        self.seq_box.setObjectName("seq_box")       
        self.grid_layout.addWidget(self.seq_box, 1, 0, 1, 2)
        
        # Organism taxid
        self.org_taxid = QtWidgets.QLineEdit(self.central_widget)
        self.org_taxid.setPlaceholderText("")
        self.org_taxid.setObjectName("org_taxid")       
        self.grid_layout.addWidget(self.org_taxid, 2, 0, 1, 2)
        
        # Host taxid
        self.host_taxid = QtWidgets.QLineEdit(self.central_widget)
        self.host_taxid.setObjectName("host_taxid")
        self.grid_layout.addWidget(self.host_taxid, 3, 0, 1, 2)
        
        # Job Title
        self.job_title = QtWidgets.QLineEdit(self.central_widget)
        self.job_title.setPlaceholderText("")
        self.job_title.setObjectName("job_title")       
        self.grid_layout.addWidget(self.job_title, 4, 0, 1, 2)
        
        # Tailor Button
        self.tailor_button = QtWidgets.QPushButton(
            self.central_widget, clicked = lambda: self.run_tailor())
        self.tailor_button.setMinimumSize(QtCore.QSize(0, 80))
        self.tailor_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tailor_button.setObjectName("tailor_button")
        self.grid_layout.addWidget(self.tailor_button, 5, 0, 1, 2)        
        # Fonts
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        self.tailor_button.setFont(font)
        
        # Menu bar, autocreated from QT Desinger
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(main_window)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtWidgets.QAction(main_window)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionAbout = QtWidgets.QAction(main_window)
        self.actionAbout.setObjectName("actionAbout")
        self.actionGuide = QtWidgets.QAction(main_window)
        self.actionGuide.setObjectName("actionGuide")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_As)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionGuide)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # Adds my custom texts
        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    
    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "ProteinTailor"))
        
        # Set icon
        main_window.setWindowIcon(QtGui.QIcon("resources/dalle2_icon.png"))
        
        self.in_lab.setText(_translate("main_window", " Input format"))
        self.combo_box.setItemText(0, _translate("main_window", "cDNA"))
        self.combo_box.setItemText(1, _translate("main_window", "mRNA"))
        self.combo_box.setItemText(2, _translate("main_window", "aa-seq"))
        self.combo_box.setItemText(3, _translate("main_window", "Uniprot"))
        
        # Add placeholder
        self.job_title.setPlaceholderText(
            _translate("main_window", "Add job title"))
        self.seq_box.setPlaceholderText(
            _translate("main_window", "Insert sequences..."))
        self.org_taxid.setPlaceholderText(
            _translate("main_window", "Organism taxid"))
        self.host_taxid.setPlaceholderText(
            _translate("main_window", "Host taxid"))
        
        self.tailor_button.setText(_translate("main_window", "Tailor"))
        self.menuFile.setTitle(_translate("main_window", "File"))
        self.menuHelp.setTitle(_translate("main_window", "Help"))
        self.actionOpen.setText(_translate("main_window", "Open"))
        self.actionSave_As.setText(_translate("main_window", "Save As"))
        self.actionAbout.setText(_translate("main_window", "About"))
        self.actionGuide.setText(_translate("main_window", "Guide"))
        
    # Runs the ProteinTailor program.
    def run_tailor(self):        
        try:
            oput = ProteinTailor(self.combo_box.currentText(), 
                                 self.seq_box.toPlainText(), 
                                 self.org_taxid.text(),
                                 self.host_taxid.text(), 
                                 self.job_title.text())
        except:
            print("Error in ProteinTailor")        
        
        
