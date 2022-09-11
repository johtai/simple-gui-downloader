import sys, os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QFileDialog
from downloader import Downloader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_globals()
        self.initUI()

        # initialize button signals 
        self.download_button.clicked.connect(self.download)
        self.copy_button.clicked.connect(self.copy)
        self.clear_button.clicked.connect(self.clear)

        # set the folder to which the files should be downloaded
        self.outpath_button.clicked.connect(self.choose_outpath)
        # set the folder with yt-dlp and ffmpeg
        self.libpath_button.clicked.connect(self.choose_libpath)

        # initialize checkbox signals 
        self.thumbnail_checkbox.stateChanged.connect(self.sync_checkbox)

        # set QLineEdit cursor to the first position
        self.outpath_line.textChanged.connect(self.change_paths)
        self.libpath_line.textChanged.connect(self.change_paths)

        self.outpath_line.setCursorPosition(0)
        self.libpath_line.setCursorPosition(0)

        self.downloader_instance = Downloader(mainwindow=self)

    # set global variables
    def set_globals(self):
        user = os.environ.get("USERNAME")
        self.ydl_opts = {}
        self.outpath = f"C:/Users/{user}/Desktop/"
        self.libpath = f"{os.path.abspath(os.curdir)}/lib/".replace("\\", "/")
        self.mode = "Video"
        self.res = "Best"

    def initUI(self):
        # load most of widgets from file
        uic.loadUi('ui/main.ui', self)

        # set text to appropriate lines
        self.outpath_line.setText(self.outpath)
        self.libpath_line.setText(self.libpath)

        # connect buttons with functions (signals)
        self.video_button.toggled.connect(self.set_mode)
        self.audio_button.toggled.connect(self.set_mode)

        # make a group to radiobuttons
        self.number_group1 = QButtonGroup(self)
        self.number_group1.addButton(self.video_button)
        self.number_group1.addButton(self.audio_button)

    # sync checkbox state
    def sync_checkbox(self):
        if self.thumbnail_checkbox.isChecked() == False:
            self.youtube_cover_checkbox.setEnabled(False)
        else:
            self.youtube_cover_checkbox.setEnabled(True)

    # change variables if user changes paths
    def change_paths(self):
        self.outpath = self.outpath_line.text()
        self.libpath = self.libpath_line.text()

    # interface for selecting a folder manually
    def choose_outpath(self):
        self.outpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.getcwd())
        if self.outpath:
            self.outpath_line.setText(self.outpath)

    # interface for selecting a folder manually
    def choose_libpath(self):
        self.libpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.getcwd())
        if self.libpath:
            self.libpath_line.setText(self.libpath)

    # set mode (video or audio)
    def set_mode(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.mode = radioBtn.text()

    # copy button
    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.url_line.text())

    # clear button
    def clear(self):
        self.url_line.clear()
        
        # download the file
    def download(self):
        self.downloader_instance.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec()) 