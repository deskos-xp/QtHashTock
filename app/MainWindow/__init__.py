from PyQt5.QtCore import QObject,QThread,QRunnable,QThreadPool,pyqtSignal,pyqtSlot,QCoreApplication
from PyQt5.QtWidgets import QMainWindow,QDialog,QWidget,QApplication,QLCDNumber,QProgressBar,QHeaderView
from PyQt5.QtMultimedia import QSound

from PyQt5 import uic
import os,sys,json
from .workers.klocked import Klocked
import time as Time
from .workers.IterWorker import IterWorker
from ..common.TableModel import TableModel
from .Menubar import Menubar
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("app/MainWindow/forms/main.ui",self)
        
        self.timeWorker=Klocked()
        self.timeWorker.signals.hasTime.connect(self.timeParse)
        
        QThreadPool.globalInstance().start(self.timeWorker)
        QCoreApplication.instance().aboutToQuit.connect(self.killWorkers)
        self.progressToEndOfDay.setMaximum(24*60*60)
        self.progressToEndOfDay.setValue(0)
        self.progressToNextHour.setMaximum(60*60)
        self.progressToNextHour.setValue(0)
        
        self.progressToNextMinute.setMaximum(60)
        self.progressToNextMinute.setValue(0)

        self.dateModel=TableModel(item=self.displayCompatTime(Time.localtime()))
        self.setViews(views=['dateView'],models=['dateModel'])
        self.tick=QSound("app/sounds/tiktok.wav",parent=self)
        self.hourFMT.toggled.connect(self.hourFMTChange)
        if self.hourFMT.isChecked():
            self.dayStage.show()
        else:
            self.dayStage.hide()

        self.mb=Menubar(self)            
        #QLCDNumber.
        args=QCoreApplication.instance().arguments()
        if args:
            for i in ['-w','--waste-cycles']:
                if i in args:
                    self.iterWorkerPrep() 
        self.setWindowTitle("Qt5 HashTok")
        self.show()

    def hourFMTChange(self,state):
        if state:
            self.dayStage.show()
        else:
            self.dayStage.hide()

    def killWorkers(self):
        for i in ['timeWorker','iterworker']:
            try:
                getattr(self,i).signals.kill()
            except Exception as e:
                print(e)

    def iterWorkerPrep(self):
        self.iterworker=IterWorker()
        self.iterworker.signals.hasElement.connect(self.statusBar().showMessage)
        self.iterworker.signals.hasError.connect(lambda x:print(x))
        self.iterworker.signals.finished.connect(self.iterWorkerPrep)
        QThreadPool.globalInstance().start(self.iterworker)

    def setViews(self,views,models):
        def setupView(view,model):
            view.setModel(model)
            view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for v,m in zip(views,models):
            view=getattr(self,v)
            model=getattr(self,m)
            setupView(view,model)

    def displayCompatTime(self,time):
        f=[i for i in dir(time) if not callable(getattr(time,i)) and i.startswith('tm_') ]
        timeDict={i:getattr(time,i) for i in f}
        return timeDict

    def playSound(self):
        self.tick.play()
    
    def timeParse(self,time):
        self.playSound()
        if not self.hourFMT.isChecked(): 
            self.hour.display(time.tm_hour)
        else:
            tm=time.tm_hour-12
            if tm >= 0:
                self.hour.display(tm)
                self.dayStage.setText("PM")
            else:
                self.hour.display(time.tm_hour)
                self.dayStage.setText("AM")
        self.minute.display(time.tm_min)
        self.second.display(time.tm_sec)
        progress=(time.tm_hour*60*60)+(time.tm_min*60)+time.tm_sec
        self.progressToEndOfDay.setValue(progress)
        self.progressToNextHour.setValue((time.tm_min*60)+time.tm_sec)
        self.progressToNextMinute.setValue(time.tm_sec)

        self.dateModel.load_data(self.displayCompatTime(time))
        self.dateModel.layoutChanged.emit() 

def main():
    app=QApplication(sys.argv)
    echo=MainWindow()
    app.exec_()
