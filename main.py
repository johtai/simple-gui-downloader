import sys, os, shutil
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt, QRect, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_globals()
        self.initUI()

        self.download_button.clicked.connect(self.download)
        self.copy_button.clicked.connect(self.copy)
        self.clear_button.clicked.connect(self.clear)
        # set the folder to which the files should be downloaded
        self.outpath_button.clicked.connect(self.choose_outpath)
        # set the folder with yt-dlp and ffmpeg
        self.libpath_button.clicked.connect(self.choose_libpath)

        # set QLineEdit cursor to the first position
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

    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.url_line.text())

    def clear(self):
        self.url_line.setText("")

    # download the file
    def download(self):
        # get a url
        url = self.url_line.text()

        # make libpath the current folder for script
        os.chdir(self.libpath)

        # choose the mode (audio or video download) and make a command to execute
        if self.mode == "Audio":
            ext = self.audio_format_box.currentText()
            command = f'yt-dlp -P {self.outpath} -x --audio-format "{ext} / mp3"'
            # download and embed the album/track cover
            if self.thumbnail_checkbox.isChecked():
                command += " --embed-thumbnail"
            # download and embed the album/track cover for YouTube (from this issue https://github.com/yt-dlp/yt-dlp/issues/429#issuecomment-865423256)
            elif self.youtube_cover_checkbox.isChecked():
                command += """ --embed-thumbnail -v --convert-thumbnail jpg --ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\"" --exec ffprobe"""
        
        elif self.mode == "Video":
            # convenient variables for further use
            ext = self.video_format_box.currentText()
            res = self.quality_box.currentText()

            # if there is no required extension, the program chooses the mp4
            if self.quality_box.currentText() != "Best":
                command = f'yt-dlp -P {self.outpath} -f "bestvideo[ext={ext}][height<={res}]+bestaudio[ext=m4a] / bestvideo[ext=mp4][height<={res}]+bestaudio[ext=m4a]"'
            else:
                # yt-dlp chooses the best resolution by itself
                command = f'yt-dlp -P {self.outpath} -f "bestvideo[ext={ext}]+bestaudio[ext=m4a] / bestvideo[ext=mp4]+bestaudio[ext=m4a]"'

            # force merge file to mkv
            if ext == "mkv":
                command += " --merge-output-format mkv"

        # downloads the full playlist, if it is contained in the url
        if self.playlist_checkbox.isChecked():
            command += " --yes-playlist"
        else:
            command += " --no-playlist"

        command += f' "{url}"'

        # execute the full command
        os.system(command)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec()) 