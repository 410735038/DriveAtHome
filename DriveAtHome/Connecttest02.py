import sys
import time
from datetime import datetime

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import QUrl, QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, QSound
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QThread, QTime, QDateTime
from PyQt5.QtGui import QMovie, QIcon, QCursor
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableView

# import lavie7_3radioB
from Threadtest import Ui_Form
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QCoreApplication
from Dialog_connect import Ui_Dialog_connect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSequentialAnimationGroup, QRect
import random
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlQuery
# import lavie33QMovie

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from allControl_game import *

from SerialManager import *


class Demo(QWidget, Ui_Form):
    # firstP_lab_signal = pyqtSignal()
    # video_con_signal = pyqtSignal()
    def __init__(self):
        super(Demo, self).__init__()
        ####
        self.square = SubDialog()
        ####
        self.setupUi(self)
        self.resize(1192, 842)
        self.stackedWidget.resize(1192, 842)
        self.Intobtn.resize(1192, 842)
        self.firstPgif_l.resize(1192, 842)

        self.animation = QPropertyAnimation(self.pressSbtn, b'pos')
        self.animation.setDuration(1550)
        # self.animation.setStartValue(QPoint(0, 0))
        # self.animation.setEndValue(QPoint(500, 500))
        self.animation.setKeyValueAt(0.4, QPoint(480, 405))
        self.animation.setKeyValueAt(1, QPoint(480, 420))
        self.animation.setLoopCount(-1)
        self.animation.start()

        self.firstPgif = QMovie(self)
        self.firstPgif.setFileName('oneone/firstPgif.gif')
        self.firstPgif_l.setMovie(self.firstPgif)

        self.firstPgif.start()

        self.pressSbtn.clicked.connect(self.IntoMenuP)
        #self.Intobtn.clicked.connect(self.IntoMenuP)
        self.pressSbtn.setFlat(True)
        self.Intobtn.setFlat(True)
        self.SetBtn_M.setFlat(True)
        self.SetBtn_CM.setFlat(True)
        self.SetBtn_PM.setFlat(True)
        self.rank_btn.setFlat(True)

        # 開始遊戲
        # self.Startbtn.clicked.connect(self.start_countdown_func)
        self.Startbtn.clicked.connect(self.gotoModechooP)
        self.start_stackedW.hide()

        self.car_loading = QMovie(self)
        self.car_loading.setFileName('res/car_loading.gif')
        self.show_car_loading_gif.setMovie(self.car_loading)

        self.thread = MyThread()
        self.thread.ok_signal.connect(self.show_result_func)

        self.CMbtn.clicked.connect(self.gotoControlModeP)
        self.PMbtn.clicked.connect(self.gotoPlayingModeP)
        self.CMbackbtn.clicked.connect(self.backtoMenuP)
        self.PMbackbtn.clicked.connect(self.backtoMenuP)
        self.ExitButton.clicked.connect(self.show_messagebox)  # 跳確認是否離開遊戲

        self.SetBtn_M.clicked.connect(lambda: self.gotoSetP(self.MenuP))
        self.SetBtn_CM.clicked.connect(lambda: self.gotoSetP(self.ControlModeP))
        self.SetBtn_PM.clicked.connect(lambda: self.gotoSetP(self.PlayModeP))

        self.video_w_hide_btn_CM.clicked.connect(self.controlCMVideoPlay)
        self.video_w_hide_btn_PM.clicked.connect(self.controlPMVideoPlay)

        self.rank_btn.clicked.connect(self.gotoRankP)
        self.Rankbackbtn.clicked.connect(self.backtoMenuP)

        self.AR1rankbtn.clicked.connect(self.showAR1rank)
        self.AR2rankbtn.clicked.connect(self.showAR2rank)

        # *****背景音樂*****
        self.sound_bgm = QSoundEffect(self)
        self.sound_bgm.setSource(QUrl.fromLocalFile('res/bgm01.wav'))
        self.sound_bgm.setVolume(1.0)
        self.sound_bgm.setLoopCount(-2)
        self.sound_bgm.play()

        # *****按鈕音效*****
        self.effect_button = QSoundEffect(self)
        self.effect_button.setSource(QUrl.fromLocalFile('res/button_effect.wav'))
        self.effect_button.setVolume(1.0)
        # self.Intobtn.clicked.connect(self.effect_button.play)

        self.Startbtn.clicked.connect(self.effect_button.play)
        self.CMbtn.clicked.connect(self.effect_button.play)
        self.PMbtn.clicked.connect(self.effect_button.play)
        self.ExitButton.clicked.connect(self.effect_button.play)
        self.SetBtn_M.clicked.connect(self.effect_button.play)
        self.rank_btn.clicked.connect(self.effect_button.play)
        self.Rankbackbtn.clicked.connect(self.effect_button.play)

        self.DrMbtn.clicked.connect(self.effect_button.play)
        self.ARMbtn.clicked.connect(self.effect_button.play)
        self.FrMbtn.clicked.connect(self.effect_button.play)
        self.PMbackbtn.clicked.connect(self.effect_button.play)
        self.SetBtn_PM.clicked.connect(self.effect_button.play)

        self.DrCMbtn.clicked.connect(self.effect_button.play)
        self.BodyCMbtn.clicked.connect(self.effect_button.play)
        self.CMbackbtn.clicked.connect(self.effect_button.play)
        self.SetBtn_CM.clicked.connect(self.effect_button.play)

        self.SPfinishBtn.clicked.connect(self.effect_button.play)
        self.AR1rankbtn.clicked.connect(self.effect_button.play)
        self.AR2rankbtn.clicked.connect(self.effect_button.play)

        # *****音效音量*****
        self.effectSli.setRange(0, 100)
        self.effectSli.setValue(100)
        self.effectSli.valueChanged.connect(self.set_effect_func)

        # *****背景音量*****
        self.volumeSli.setRange(0, 100)
        self.volumeSli.setValue(100)
        self.volumeSli.valueChanged.connect(self.set_volume_func)

        ###########加影片
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)  ####
        self.player.setPlaylist(self.playlist)  ####
        self.player.setVideoOutput(self.video_widget)
        self.player.setVideoOutput(self.video_widget_CM)
        self.media_contentDr = QMediaContent(QUrl.fromLocalFile('res/DriveM.mp4'))
        self.media_contentAR = QMediaContent(QUrl.fromLocalFile('res/ARM.mp4'))
        self.media_contentFr = QMediaContent(QUrl.fromLocalFile('res/FreeM.mp4'))
        self.media_contentBodyCM = QMediaContent(QUrl.fromLocalFile('fish/BodyCM.avi'))
        self.media_contentDriveCM = QMediaContent(QUrl.fromLocalFile('fish/DriveCM.avi'))

        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('fish/BodyCM.avi')))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('fish/DriveCM.avi')))
        # self.playlist.setCurrentIndex(0)
        # self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

        self.DrMbtn.clicked.connect(lambda: self.playPMvideo(self.DrMbtn))
        self.ARMbtn.clicked.connect(lambda: self.playPMvideo(self.ARMbtn))
        self.FrMbtn.clicked.connect(lambda: self.playPMvideo(self.FrMbtn))

        self.DrCMbtn.clicked.connect(lambda: self.playCMvideo(self.DrCMbtn))
        self.BodyCMbtn.clicked.connect(lambda: self.playCMvideo(self.BodyCMbtn))
        #
        # self.lineEdit.setText("PPP")
        # ppp = self.lineEdit.text()
        # self.tryy(ppp)
        #
        # self.pushButton.clicked.connect(self.tryy)

        ###########
        p_vw = self.video_widget.palette()
        p_vw.setColor(QPalette.Window, Qt.black)
        self.video_widget.setPalette(p_vw)

        self.Startbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.CMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.PMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.ExitButton.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.DrMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.ARMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.FrMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.DrCMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")
        self.BodyCMbtn.setStyleSheet("QToolButton:hover{background-color:rgb(0,0,0)}")

        self.go_btn.clicked.connect(self.start_countdown_func)  # go_btn是選完模式之後按的

        self.ModeChoo_CMD_rbtn.toggled.connect(self.Choose_CM)
        self.ModeChoo_CMB_rbtn.toggled.connect(self.Choose_CM)

        self.db = None
        self.db_connect()
        # self.sql_exec()
        self.tableView_1.setVisible(False)
        self.tableView_2.setVisible(False)


    def db_connect(self):
        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName('localhost')
        self.db.setDatabaseName('TEST0610')

        self.db.setUserName('root')
        self.db.setPassword('root')
        self.db.setPort(3306)
        if not self.db.open():
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())

    def closeEvent(self, QCloseEvent):
        self.db.close()

    def sql_exec1(self):

        model1 = QSqlTableModel()
        model1.setTable('gamehistory_time')
  
        model1.setEditStrategy(QSqlTableModel.OnFieldChange)


        model1.select()

        self.Rank1_tableView.setModel(model1)
        self.Rank1_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.Rank1_tableView.setStyleSheet("background-image:url(fish/arscoreR_mid.jpg)")

        self.Rank1_tableView.horizontalHeader().setVisible(False)
        self.Rank1_tableView.verticalHeader().setVisible(False)
        self.Rank1_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.Rank1_tableView.horizontalHeader().resizeSection(0, 220)
        self.Rank1_tableView.horizontalHeader().resizeSection(1, 180)
        #self.Rank1_tableView.horizontalHeader().resizeSection(2, 350)

        self.Rank1_tableView.horizontalHeader().setStretchLastSection(True)
        self.Rank1_tableView.verticalHeader().resizeSection(0, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(1, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(2, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(3, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(4, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(5, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(6, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(7, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(8, 50)
        self.Rank1_tableView.verticalHeader().resizeSection(9, 50)

        self.Rank1_tableView.setFrameShape(QFrame.NoFrame)
        self.Rank1_tableView.setShowGrid(False)

        self.Rank1_tableView.sortByColumn(1, Qt.AscendingOrder)

        for i in range(model1.rowCount()):
            name= model1.record(i).value(0)
            passTime = model1.record(i).value(1)
            playTime = model1.record(i).value(2)
            print(name, passTime, playTime)


        print('---------------------')

    def sql_exec2(self):
        model2 = QSqlTableModel()

        model2.setTable('gamehistory_ar')
        model2.setEditStrategy(QSqlTableModel.OnFieldChange)


        model2.select()

        self.Rank2_tableView.setModel(model2)

        self.Rank2_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.Rank2_tableView.horizontalHeader().setVisible(False)
        self.Rank2_tableView.verticalHeader().setVisible(False)

        self.Rank2_tableView.horizontalHeader().resizeSection(0, 200)
        self.Rank2_tableView.horizontalHeader().resizeSection(1, 100)
        #self.Rank2_tableView.horizontalHeader().resizeSection(2, 350)

        self.Rank2_tableView.horizontalHeader().setStretchLastSection(True)
        self.Rank2_tableView.verticalHeader().resizeSection(0, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(1, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(2, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(3, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(4, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(5, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(6, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(7, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(8, 50)
        self.Rank2_tableView.verticalHeader().resizeSection(9, 50)

        self.Rank2_tableView.setShowGrid(False)
        self.Rank2_tableView.setFrameShape(QFrame.NoFrame)
        self.Rank2_tableView.sortByColumn(1, Qt.DescendingOrder)

        for i in range(model2.rowCount()):
            name = model2.record(i).value(0)
            score = model2.record(i).value(1)
            playTime = model2.record(i).value(2)
            print(name, score, playTime)

    def Choose_CM(self):
        if self.ModeChoo_CMD_rbtn.isChecked():  # 選方向盤操控所有模式都能玩
            self.ModeChoo_PMD_rbtn.setEnabled(True)
            self.ModeChoo_PMAR1_rbtn.setEnabled(True)
            self.ModeChoo_PMAR2_rbtn.setEnabled(True)
            self.ModeChoo_PMF_rbtn.setEnabled(True)
        else:  # 選肢體操控就不能玩駕訓班模式
            self.ModeChoo_PMD_rbtn.setEnabled(False)
            self.ModeChoo_PMAR1_rbtn.setEnabled(True)
            self.ModeChoo_PMAR2_rbtn.setEnabled(True)
            self.ModeChoo_PMF_rbtn.setEnabled(True)

    def IntoMenuP(self):
        self.stackedWidget.setCurrentIndex(1)

    def gotoControlModeP(self):
        self.stackedWidget.setCurrentIndex(3)
        self.player.setVideoOutput(self.video_widget_CM)  # 補這個才不會殘留畫面

    def gotoPlayingModeP(self):
        self.stackedWidget.setCurrentIndex(2)
        self.player.setVideoOutput(self.video_widget)  # 補這個才不會殘留畫面
        # self.player = QMediaPlayer(self)
        # self.player.setVideoOutput(self.video_widget)
        # self.player.setMedia(self.media_contentDr)

    def backtoMenuP(self):
        self.stackedWidget.setCurrentIndex(1)
        self.player.stop()
        self.sound_bgm.setMuted(False)

    ######從設定完成後返回

    def gotoControlModePset(self):
        self.stackedWidget.setCurrentIndex(3)

    def gotoPlayingModePset(self):
        self.stackedWidget.setCurrentIndex(2)
        self.player.setVideoOutput(self.video_widget_CM)

    def backtoMenuPset(self):
        self.stackedWidget.setCurrentIndex(1)

    def gotoSetP(self, lastP):
        self.stackedWidget.setCurrentIndex(4)
        if self.player.state() == 1:
            self.player.pause()
        if lastP == self.MenuP:
            self.SPfinishBtn.clicked.connect(self.backtoMenuPset)
        if lastP == self.ControlModeP:
            self.SPfinishBtn.clicked.connect(self.gotoControlModePset)
        if lastP == self.PlayModeP:
            self.SPfinishBtn.clicked.connect(self.gotoPlayingModePset)
            self.sound_bgm.setMuted(False)

    def gotoRankP(self):
        self.stackedWidget.setCurrentIndex(5)
        self.sql_exec1()
        self.sql_exec2()


    def showAR1rank(self):
        self.stackedWidget_Rank.setCurrentIndex(0)

    def showAR2rank(self):
        self.stackedWidget_Rank.setCurrentIndex(1)

    def set_volume_func(self):
        self.sound_bgm.setVolume(self.volumeSli.value() / 100)
        self.volumeVal_l.setText(str(self.volumeSli.value()))

    def set_effect_func(self):
        self.effect_button.setVolume(self.effectSli.value() / 100)
        self.effectVal_l.setText(str(self.effectSli.value()))

    def playCMvideo(self, btn):
        if btn == self.DrCMbtn:
            self.player.setVideoOutput(self.video_widget_CM)
            # self.player.setMedia(self.media_contentDriveCM)
            self.playlist.setCurrentIndex(0)
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.player.play()

        elif btn == self.BodyCMbtn:
            self.player.setVideoOutput(self.video_widget_CM)
            # self.player.setMedia(self.media_contentBodyCM)
            self.playlist.setCurrentIndex(1)
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.player.play()

    def playPMvideo(self, btn):
        if btn == self.DrMbtn:
            self.player.setVideoOutput(self.video_widget)
            self.player.setMedia(self.media_contentDr)
            self.player.setVolume(80)  # 影片音量
            self.player.play()
            self.sound_bgm.setMuted(True)
            # self.volumeSli.setValue(0)   #BGM音量

        elif btn == self.ARMbtn:
            self.player.setVideoOutput(self.video_widget)
            self.player.setMedia(self.media_contentAR)
            self.player.setVolume(80)
            self.player.play()
            self.sound_bgm.setMuted(True)
            # self.volumeSli.setValue(0)

        elif btn == self.FrMbtn:
            self.player.setVideoOutput(self.video_widget)
            self.player.setMedia(self.media_contentFr)
            self.player.setVolume(80)
            self.player.play()
            self.sound_bgm.setMuted(True)
            # self.volumeSli.setValue(0)

    # *****按控制教學影片暫停或播放
    def controlCMVideoPlay(self):
        if self.player.state() == 1:
            self.player.pause()
            # self.sound_bgm.setMuted(False)
        else:
            self.player.play()
            # self.sound_bgm.setMuted(True)

    # *****按模式介紹教學影片暫停或播放
    def controlPMVideoPlay(self):
        if self.player.state() == 1:
            self.player.pause()
            self.sound_bgm.setMuted(False)
            # self.volumeSli.setValue(100)
        else:
            self.player.play()
            self.sound_bgm.setMuted(True)
            # self.volumeSli.setValue(0)

    def show_messagebox(self, QCloseEvent):
        choice = QMessageBox.question(self, 'Exit', '確定要結束遊戲嗎?', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            QCloseEvent.accept()
        elif choice == QMessageBox.No:
            pass

    # **********選完模式之後連接車子

    def start_countdown_func(self):
        if self.lineEdit_name.text() == "":
            self.lineEdit_name.setText("Oo無名車手oO")
        if self.ModeChoo_CMD_rbtn.isChecked() and self.ModeChoo_PMD_rbtn.isChecked():
            CMchoose = "drive"
            PMchoose = "drive"
            self.label_9.setText("進到方向盤操控的駕訓班模式")

        if self.ModeChoo_CMD_rbtn.isChecked() and self.ModeChoo_PMF_rbtn.isChecked():
            CMchoose = "drive"
            PMchoose = "drive"
            self.label_9.setText("進到方向盤操控的自由模式")
        if self.ModeChoo_CMD_rbtn.isChecked() and self.ModeChoo_PMAR1_rbtn.isChecked():
            CMchoose = "drive"
            PMchoose = "ar_time"
            self.label_9.setText("進到方向盤操控的AR計時")
        if self.ModeChoo_CMD_rbtn.isChecked() and self.ModeChoo_PMAR2_rbtn.isChecked():
            CMchoose = "drive"
            PMchoose = "ar_score"
            self.label_9.setText("進到方向盤操控的AR計分")


        if self.ModeChoo_CMB_rbtn.isChecked() and self.ModeChoo_PMAR1_rbtn.isChecked():
            CMchoose = "body"
            PMchoose = "ar_time"
            self.label_9.setText("進到肢體操控的AR計時模式")

        if self.ModeChoo_CMB_rbtn.isChecked() and self.ModeChoo_PMAR2_rbtn.isChecked():
            CMchoose = "body"
            PMchoose = "ar_score"
            self.label_9.setText("進到肢體操控的AR計分模式")

        if self.ModeChoo_CMB_rbtn.isChecked() and self.ModeChoo_PMF_rbtn.isChecked():
            CMchoose = "body"
            PMchoose = "drive"
            self.label_9.setText("進到肢體操控的自由模式")

        player = self.lineEdit_name.text()
        x = allControl(player, CMchoose, PMchoose, self.square)

        # self.start_stackedW.setCurrentIndex(0)
        # self.start_stackedW.show()
        # self.wait_dia_btn.clicked.connect(self.start_stackedW.close)  # 連接車子那裡的叉叉

        # self.conOK_btn_f.clicked.connect(self.backtoModechooP)

        # self.car_loading.start()  # 跑車子連接中的動圖
        # self.thread.start()
        # self.car_con_lab.setText("          車子連接中")
        # self.wait_dia_btn.setStyleSheet("QWidget{background-color:rgb(255,255,255)}")
        # self.widget_con.setStyleSheet("QWidget{border-color:rgb(0,0,0)}")
        # # self.test_init()
        # self.conOK_btn_s.hide()
        # self.conOK_btn_f.hide()

    def show_result_func(self):
        ran = random.randint(0, 1)
        self.car_loading.stop()
        if ran == 0:
            self.car_con_lab.setText("           連接成功!")
            print(self.car_con_lab.text())
            # self.wait_dia_btn.setText("OK!")

            self.conOK_btn_s.show()
        else:
            self.car_con_lab.setText("    連接失敗!請重試")
            print(self.car_con_lab.text())
            self.conOK_btn_f.show()


    # **********按開始遊戲後來選模式
    def gotoModechooP(self):
        self.start_stackedW.setCurrentIndex(1)
        self.start_stackedW.show()
        self.wait_dia_btn_2.clicked.connect(self.start_stackedW.close)  # 選模式那裡的叉叉

    def backtoModechooP(self):
        self.start_stackedW.setCurrentIndex(1)

    def gotoPortChooP(self):
        self.start_stackedW.setCurrentIndex(2)


class MyThread(QThread):
    ok_signal = pyqtSignal()

    def __init__(self):
        super(MyThread, self).__init__()
        self.countdown = 100000

    def run(self):
        while self.countdown > 0:
            self.countdown -= 1
            print(self.countdown)

        self.ok_signal.emit()
        self.countdown = 100000


class SubDialog(QDialog, Ui_Dialog_connect):
    def __init__(self):
        super(SubDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("connecting")
        self.car_loading = QMovie(self)
        self.car_loading.setFileName('res/car_loading.gif')
        self.show_car_loading_gif.setMovie(self.car_loading)
        self.car_loading.start()
        self.wait_dia_btn.clicked.connect(self.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    # s = SubDialog()
    # s.show()
    sys.exit(app.exec_())