import sys
from PyQt5 import QtWidgets
from gui.tailor_gui import GUI


def main():
    """Starts the GUI and runs the program
    """
    app = QtWidgets.QApplication(sys.argv)    
    main_window = QtWidgets.QMainWindow()
    ui = GUI()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()