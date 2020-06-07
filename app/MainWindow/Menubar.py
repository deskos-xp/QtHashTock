class Menubar:
    def __init__(self,parent):
        self.mb=parent.menuBar
        self.parent=parent 
        parent.actionExit.triggered.connect(parent.close)
