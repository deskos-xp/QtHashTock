from PyQt5.QtCore import QAbstractTableModel,QModelIndex,Qt
from PyQt5.QtGui import QColor

class TableModel(QAbstractTableModel):
    def __init__(self,item=None,**kwargs):
        super(TableModel,self).__init__()
        self.item=item or dict()
        self.items=[[i,self.item.get(i)] for i in self.item.keys()]
        self.load_data(self.items)
        self.alignment_default=[Qt.AlignLeft,Qt.AlignCenter]
        
    def load_data(self,data):
        if type(data) == type(dict()):
            self.item=data
            tmp=[[i,self.item.get(i)] for i in self.item.keys()]
            data = tmp
            self.items=tmp
        self.fields=[i[0] for i in data]
        self.vals=[i[1] for i in data]
        self.row_count=len(self.vals)
        self.column_count=2

    def rowCount(self,parent=QModelIndex()):
        return self.row_count

    def columnCount(self,parent=QModelIndex()):
        return self.column_count

    def headerData(self,section,orientation,role):
        if role != Qt.DisplayRole:
            return None
        elif orientation == Qt.Horizontal:
            return ("Fields","Values")[section]
        else:
            return "{}".format(section)

    def data(self,index,role=Qt.DisplayRole):
        column=index.column()
        row=index.row()

        if role==Qt.DisplayRole:
            if column == 0:
                return self.fields[row]
            if column == 1:
                return self.vals[row]
        if role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return self.alignment_default[column]
        return None
