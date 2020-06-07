from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSlot,pyqtSignal

import os,sys,time

class KlockedSignals(QObject):
    hasTime:pyqtSignal=pyqtSignal(time.struct_time)
    finished:pyqtSignal=pyqtSignal()
    killMe:bool=False
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        QThread.sleep(2)


class Klocked(QRunnable):
    def __init__(self):
        super(Klocked,self).__init__()
        self.signals=KlockedSignals()

    def run(self):
        while self.signals.killMe == False:
            QThread.sleep(1)
            t=time.localtime()
            #print(t.tm_hour)
            self.signals.hasTime.emit(t)
        self.signals.finished.emit()
