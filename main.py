import sys, os, shutil
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        user = os.environ.get("USERNAME")
        self.libpath = f"{os.path.abspath(os.curdir)}\\bin\\"
        self.outpath = f"C:\\Users\\{user}\\Desktop\\"
        self.mode = "Video"
        self.res = "Best"

        self.initUI()

        self.button.clicked.connect(self.download)
        self.folder_button.clicked.connect(self.choose_outpath)
        self.libpath_button.clicked.connect(self.choose_libpath)

    def initUI(self):
        uic.loadUi('main.ui', self)

        self.folder_label.setText(self.outpath)
        self.libpath_label.setText(self.libpath)

        self.r0.toggled.connect(self.set_mode)
        self.r1.toggled.connect(self.set_mode)

        self.number_group = QButtonGroup(self)
        self.number_group.addButton(self.r0)
        self.number_group.addButton(self.r1)

        self.res1.toggled.connect(self.set_res)
        self.res2.toggled.connect(self.set_res)
        self.res3.toggled.connect(self.set_res)
        self.res4.toggled.connect(self.set_res)
        self.res5.toggled.connect(self.set_res)

    def choose_outpath(self):
        self.outpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.getcwd())
        if self.outpath:
            self.folder_label.setText(self.outpath)

    def choose_libpath(self):
        self.libpath = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.getcwd())
        if self.libpath:
            self.libpath_label.setText(self.libpath)

    def set_res(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.res = radioBtn.text()

    def set_mode(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.mode = radioBtn.text()

    def download(self):
        url = self.line.text()
        print(url)

        os.chdir(self.libpath)

        if self.mode == "Audio":
            os.system(f'yt-dlp --audio-format "mp3" --extract-audio {url}')
        elif self.mode == "Video":
            os.system(f'yt-dlp -S "res:{self.res}" {url}')

        get_files = os.listdir(self.libpath)
        
        for file in get_files:
            if file.endswith(".mp3") or file.endswith(".mp4") or file.endswith(".opus") or file.endswith(".webm") or file.endswith(".mkv"):
                shutil.move(self.libpath + file, self.outpath + file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec()) 