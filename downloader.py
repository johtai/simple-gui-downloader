import os
from PyQt6.QtCore import QThread


class Downloader(QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        # get a url
        url = self.mainwindow.url_line.text()

        # make libpath the current folder for script
        os.chdir(self.mainwindow.libpath)

        # choose the mode (audio or video download) and make a command to execute
        if self.mainwindow.mode == "Audio":
            ext = self.mainwindow.audio_format_box.currentText()
            command = f'yt-dlp -P {self.mainwindow.outpath} -x --audio-format "{ext} / mp3"'
            # download and embed the album/track cover
            if self.mainwindow.thumbnail_checkbox.isChecked():
                command += " --embed-thumbnail"
            # download and embed the album/track cover for YouTube (from this issue https://github.com/yt-dlp/yt-dlp/issues/429#issuecomment-865423256)
            elif self.mainwindow.youtube_cover_checkbox.isChecked():
                command += """ --embed-thumbnail -v --convert-thumbnail jpg --ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\"" --exec ffprobe"""
        
        elif self.mainwindow.mode == "Video":
            # convenient variables for further use
            ext = self.mainwindow.video_format_box.currentText()
            res = self.mainwindow.quality_box.currentText()

            # if there is no required extension, the program chooses the mp4
            if self.mainwindow.quality_box.currentText() != "Best":
                command = f'yt-dlp -P {self.mainwindow.outpath} -f "bestvideo[ext={ext}][height<={res}]+bestaudio[ext=m4a] / bestvideo[ext=mp4][height<={res}]+bestaudio[ext=m4a]"'
            else:
                # yt-dlp chooses the best resolution by itself
                command = f'yt-dlp -P {self.mainwindow.outpath} -f "bestvideo[ext={ext}]+bestaudio[ext=m4a] / bestvideo[ext=mp4]+bestaudio[ext=m4a]"'

            # force merge file to mkv
            if ext == "mkv":
                command += " --merge-output-format mkv"

        # downloads the full playlist, if it is contained in the url
        if self.mainwindow.playlist_checkbox.isChecked():
            command += " --yes-playlist"
        else:
            command += " --no-playlist"

        command += f' --output "%(title)s.%(ext)s" "{url}"'

        # execute the full command
        os.system(command)