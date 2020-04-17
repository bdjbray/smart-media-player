import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow,QMessageBox,
                             QWidget, QFileDialog,QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy,QSlider, QStyle, QAction,
                             QVBoxLayout, QWidget,QLineEdit,QInputDialog)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon
import sqlite_test
import loadFrames
import detect



class VideoMain(QMainWindow):

    def __init__(self, parent=None):
        super(VideoMain, self).__init__(parent)

        self.setWindowTitle("smart video player")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        # play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.playVideo)

        # skip button
        self.seekLeft = QPushButton()
        self.seekLeft.setEnabled(False)
        self.seekLeft.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.seekLeft.clicked.connect(self.seekBackward)

        self.seekRight = QPushButton()
        self.seekRight.setEnabled(False)
        self.seekRight.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.seekRight.clicked.connect(self.seekForward)

        # volume button
        self.volumeButton = QPushButton()
        self.volumeButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeButton.clicked.connect(self.volume)

        # seek slider
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        # error label
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        


        # open action
        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+A')
        openAction.setStatusTip('Open Video')
        openAction.triggered.connect(self.openFile)

        #search action
        searchAction = QAction('&Open', self)
        searchAction.setShortcut('Ctrl+W')
        searchAction.setStatusTip('search Video')
        searchAction.triggered.connect(self.gettext)

        # exit action
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+S')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Intro action
        introAction = QAction('&Intro', self)
        introAction.setShortcut('Ctrl+Q')
        introAction.setStatusTip('Get some info')
        introAction.triggered.connect(self.show_popup)

        # create menubar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        HelpMenu = menuBar.addMenu('&Help')


        # add actions in menubar
        fileMenu.addAction(openAction)
        fileMenu.addAction(searchAction)
        fileMenu.addAction(exitAction)
        HelpMenu.addAction(introAction)
        
        



        # create a widget for window content
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # create and control layout
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.seekLeft)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.seekRight)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.volumeButton)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # set widget to contain window contents
        wid.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)


    def playVideo(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def seekBackward(self):
        pass

    def seekForward(self):
        pass

    def volume(self):
        pass

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            loadFrames.loadFrame(fileName)  # video to frame
            labels=detect.detect()   # detect objects
            item1=None
            item2=None
            try:
                item1=labels[0]
                print(item1)
            except Exception as e:
                pass
            try:
                item2=labels[1]
                print(item2)
            except Exception as e:
                pass
            sqlite_test.insert_emp(str(fileName),item1,item2)   #store the directory and objects to database
            print(sqlite_test.get_emps_by_directory(fileName))
            self.playButton.setEnabled(True)  #after choosing, enable play button

    def exitCall(self):
        sys.exit(app.exec_())

    # help Qmessage box
    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText("Introduction")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setInformativeText("press show details to get introduction on how to use the media player")

        msg.setDetailedText("You can play any local videos you have\nPress File and Open to choose one.(or Ctrl+A)\nPress File and Search to search any contents.\n(or Ctrl+W)")
        x=msg.exec_()

        msg.buttonClicked.connect(self.popup_button)

    def popup_button(self, i):
        print(i.text())

    #the input dialog box
    def gettext(self):   
      text, ok = QInputDialog.getText(self, 'Search contents', 'Choose the contents you want:')
      if ok:
         self.searchContents(str(text))
    
    # search action
    def searchContents(self,text):  
        print(text)
        directory1=sqlite_test.get_emps_by_obj1(text)
        directory2=sqlite_test.get_emps_by_obj2(text)
        if directory1!=None:     # contents exist, set the media
            print(directory1[0])
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(directory1[0])))
            self.playButton.setEnabled(True)
        if directory2!=None:    #contents exist, set the media
            print(directory2[0])
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(directory2[0])))
            self.playButton.setEnabled(True)
        if directory1==None and directory2==None:
            self.didNotFound()

    def didNotFound(self):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Warning")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setInformativeText("Sorry, the contents you want does not exist!")

        #msg.setDetailedText("You can play any local videos you have\nPress File and Open to choose one.(or Ctrl+A)\nPress File and Search to search any contents.\n(or Ctrl+W)")
        x=msg.exec_()

        msg.buttonClicked.connect(self.popup_button)

    def popup_button(self, i):
        print(i.text())

    def mediaStateChanged(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("ERror: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoMain()
    player.resize(1500, 800)
    player.show()
    sys.exit(app.exec_())


