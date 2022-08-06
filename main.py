import sys, os, shutil
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.button.clicked.connect(self.download)
        # set the folder to which the files should be downloaded
        self.outpath_button.clicked.connect(self.choose_outpath)
        # set the folder with yt-dlp and ffmpeg
        self.libpath_button.clicked.connect(self.choose_libpath)

    # set global variables
    def set_globall(self):
        user = os.environ.get("USERNAME")
        self.outpath = f"C:\\Users\\{user}\\Desktop\\"
        self.libpath = f"{os.path.abspath(os.curdir)}\\lib\\"
        self.mode = "Video"
        self.res = "Best"

    def initUI(self):
        # load most of widgets from file
        uic.loadUi('main.ui', self)

        # set text to appropriate labels
        self.outpath_label.setText(self.outpath)
        self.libpath_label.setText(self.libpath)

        # connect buttons with functions (signals)
        self.video_button.toggled.connect(self.set_mode)
        self.audio_button.toggled.connect(self.set_mode)

        # make a group to radiobuttons
        self.number_group1 = QButtonGroup(self)
        self.number_group1.addButton(self.video_button)
        self.number_group1.addButton(self.audio_button)

    def choose_outpath(self):
        self.outpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.getcwd())
        if self.outpath:
            self.outpath_label.setText(self.outpath)

    def choose_libpath(self):
        self.libpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.getcwd())
        if self.libpath:
            self.libpath_label.setText(self.libpath)

    def set_mode(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.mode = radioBtn.text()

    def download(self):
        # get a url
        url = self.line.text()
        print(url)

        # make libpath the current folder for script
        os.chdir(self.libpath)

        # choose the mode and make a commant to execute
        if self.mode == "Audio":
            command = f'yt-dlp --audio-format "mp3" --extract-audio {url}'
        elif self.mode == "Video":
            command = f'yt-dlp -S "res:{self.quality_box.currentText()}" {url}'

        # execute the command
        os.system(command)
        self.command_label.setText(command)

        get_files = os.listdir(self.libpath)
        
        # move files from libpath to outpath
        for file in get_files:
            if file.endswith(".mp3") or file.endswith(".mp4") or file.endswith(".opus") or file.endswith(".webm") or file.endswith(".mkv"):
                shutil.move(self.libpath + file, self.outpath + file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec()) 