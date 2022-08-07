import sys, os, shutil
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt, QRect, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_globals()
        self.initUI()

        self.button.clicked.connect(self.download)
        # set the folder to which the files should be downloaded
        self.outpath_button.clicked.connect(self.choose_outpath)
        # set the folder with yt-dlp and ffmpeg
        self.libpath_button.clicked.connect(self.choose_libpath)

        self.outpath_line.setCursorPosition(0)
        self.libpath_line.setCursorPosition(0)

    # set global variables
    def set_globals(self):
        user = os.environ.get("USERNAME")
        self.outpath = f"C:/Users/{user}/Desktop/"
        self.libpath = f"{os.path.abspath(os.curdir)}/lib/".replace("\\", "/")
        self.mode = "Video"
        self.res = "Best"

    def initUI(self):
        # load most of widgets from file
        uic.loadUi('main.ui', self)

        # set text to appropriate lines
        self.outpath_line.setText(self.outpath)
        self.libpath_line.setText(self.libpath)

        print(self.outpath_line.cursorPosition())
        print(self.libpath_line.cursorPosition())

        # connect buttons with functions (signals)
        self.video_button.toggled.connect(self.set_mode)
        self.audio_button.toggled.connect(self.set_mode)

        # make a group to radiobuttons
        self.number_group1 = QButtonGroup(self)
        self.number_group1.addButton(self.video_button)
        self.number_group1.addButton(self.audio_button)

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

    # download the file
    def download(self):
        # get a url
        url = self.line.text()
        print(url)

        # make libpath the current folder for script
        os.chdir(self.libpath)

        # choose the mode and make a command to execute
        if self.mode == "Audio":
            command = 'yt-dlp --audio-format "mp3" --extract-audio'
        elif self.mode == "Video":
            command = f'yt-dlp -S "res:{self.quality_box.currentText()}"'

        if self.playlist_checkbox.isChecked():
            command += " --yes-playlist"
        else:
            command += " --no-playlist"

        command += f' "{url}"'

        # execute the command
        os.system(command)
        self.command_label.setText(command)

        # move files from libpath to outpath
        get_files = os.listdir(self.libpath)
        for file in get_files:
            if file.endswith(".mp3") or file.endswith(".mp4") or file.endswith(".opus") or file.endswith(".webm") or file.endswith(".mkv"):
                shutil.move(self.libpath + file, self.outpath + file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec()) 