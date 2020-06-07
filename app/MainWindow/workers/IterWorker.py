from PyQt5.QtCore import QObject,QRunnable,pyqtSlot,pyqtSignal
import itertools,string
import hashlib

class IterWorkerSignals(QObject):
    killMe:bool=False
    hasElement:pyqtSignal=pyqtSignal(str)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True

class IterWorker(QRunnable):
    def __init__(self,hashMode=None):
        super(IterWorker,self).__init__()
        self.signals=IterWorkerSignals()
        self.hashMode = hashMode or 'sha512'
    def run(self):
        try:
            for i in itertools.product(string.printable,repeat=10):
                if self.signals.killMe == False:
                    if self.hashMode != None:
                        xm=hashlib.new(self.hashMode)
                        xm.update(bytes(''.join(i),'utf-8'))
                        i=[xm.hexdigest()]
                    self.signals.hasElement.emit(''.join(i))
                else:
                    break
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
