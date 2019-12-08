# This Python file uses the following encoding: utf-8
import sys
#from PySide2.QtWidgets import QApplication
import PySide2
import os
import sys
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import qdarkstyle

#这三条是windows的一个配置信息，我觉得在mac跑可能不一定需要这三行
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


def getlist(dir):
    return os.listdir(dir)


current_path="/" #这里需要修改我用的是当前路径，应该要改成数据库内的虚拟的文件路径
file_list = getlist(current_path) #这里也要修改，我用的是os包自带的getlist方法，获取当前文件夹的每一条文件或文件夹信息，存到file_list这个list里面
#这个list里面应该是每一个item都是一个我们定义的文件或文件夹实例
#而且这里我是比较省事情就直接用了一个全局变量，所以你可能要import dbclass，然后每次点击那个下拉菜单里面的某一个条目的时候，需要把这个file_list刷新一下


class Ui_Exile(object):
    def setupUi(self, Exile):
        Exile.setObjectName("Exile")
        Exile.resize(1210, 720)#420, 714
        #Doco.setFixedSize(420, 714)#
        #Exile.setWindowFlags(QtCore.Qt.FramelessWindowHint)#隐藏默认窗口样式


        self.retranslateUi(Exile)
        QtCore.QMetaObject.connectSlotsByName(Exile)

        #self.login = QtWidgets.QPushButton(Exile)
        #self.login.setGeometry(QtCore.QRect(0, 30, 50, 30))
        #self.login.setObjectName("Login")
        #self.login.setText("Login")

        self.tb = Exile.addToolBar("Login")

        new = QAction(QIcon("./login.png"),"login",Exile)
        new.triggered.connect(self.backpath_modify)
        self.tb.addAction(new)

        self.cb = QComboBox(Exile)
        self.cb.setGeometry(QtCore.QRect(0, 50, 500, 30))
        self.cb.addItem('C') #这个函数是用来往下拉菜单添加item，每一个item应该都是一个时间戳，格式03/12/2019 17:19:03
        #可以写一个for i in listoftimestamp: self.cb.addItem(i)
        #然后下面还需要链接到一个clicked事件，比如clicked=Lambda:Refresh


        self.pushButton_pre = QtWidgets.QPushButton(Exile,clicked=lambda:Event.Pre(self))
        self.pushButton_pre.setGeometry(QtCore.QRect(0, 680, 50, 30))
        self.pushButton_pre.setObjectName("pushButton_pre")
        self.pushButton_pre.setText("Back")

        self.listWidget = QtWidgets.QListWidget(Exile)
        self.listWidget.setGeometry(QtCore.QRect(0, 80, 1200, 600))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.verticalScrollBar().setSingleStep(1)#set step
        #self.listWidget.setAlternatingRowColors(True);
        #self.listWidget.setVisible(False)
        self.music_list()

    def retranslateUi(self, Exile):
        _translate = QtCore.QCoreApplication.translate
        Exile.setWindowTitle(_translate("Exile", "Exile"))
        #self.label_name.setText(_translate("Exile", ""))
        #self.label_time.setText(_translate("Exile", ""))

    def music_list(self):
        self.listWidget.clear()#clear list
        #print(len(file_list))
        for n in range(0,len(file_list)): #这个地方就是对于file_list中的每个实例，创建一个小的Item，然后再Item中显示文件或文件夹名
            # Create QCustomQWidget
            myItemQWidget = ItemQWidget(n,self)
            myItemQWidget.setName()
            #myItemQWidget.setPlay()
            #myItemQWidget.setEvent(self.listWidget)
            # Create QListWidgetItem
            item = QtWidgets.QListWidgetItem(self.listWidget)
            # Set size hint
            item.setSizeHint(myItemQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, myItemQWidget)

    def backpath_modify(self,a):
        print("a")
        #这个地方可以考虑用来作为用户更改备份文件夹路径的方法

class ItemQWidget(QtWidgets.QWidget):
    def __init__(self,n,ui,parent = None):
        super(ItemQWidget, self).__init__(parent)
        self.n = n
        self.ui = ui
        self.textQHBoxLayout = QtWidgets.QHBoxLayout()
        self.name = QtWidgets.QLabel() #文件或文件夹名
        self.play_btn= QtWidgets.QToolButton()
        self.play_btn.setIcon(QIcon("./download.png")) #这里需要一个def download方法，点击之后下载这个文件到本地
        #self.play_btn.clicked.connect(download)
        self.info_btn = QtWidgets.QToolButton() #这里是显示文件信息的button，然后这个点击一下之后需要显示出来一个新窗口，在底下InfoQWidge
        self.info_btn.setIcon(QIcon("./info.png"))
        self.textQHBoxLayout.addWidget(self.name) 
        self.textQHBoxLayout.addWidget(self.play_btn)
        self.textQHBoxLayout.addWidget(self.info_btn)
        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQHBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setName (self):
        self.name.setText(file_list[self.n])

    def mouseDoubleClickEvent(self, e): #双击事件，如果这个item是文件夹且被双击了，
    #那么就进入这个文件夹里面，重新刷新一下路径表，这里使用的是os.path，但是我们应该要换成写出来的自己的path
        global current_path
        global file_list
        #print("clicked"+self.name.text())
        current_path = current_path + self.name.text()+"/"
        if(os.path.isdir(current_path)):
            file_list = getlist(current_path)
            self.ui.music_list() #刷新路经表

class Event():
    def Pre(self): #这个方法就是返回上一级菜单，就是那个back按钮
        global current_path
        global file_list
        cache = current_path.split("/")
        le = len(cache[len(cache)-2])+1
        current_path = current_path[:-le]
        file_list = getlist(current_path)
        self.music_list() #刷新路经表
        #print(file_list)

class infodialog(QDialog): #这个dialog是用来新打开一个窗口显示文件的各种信息的
    def __init__(self, file_info, *args, **kwargs):#这里需要传入一个自己定义的file_list里面的实例file_info
        super().__init__(*args, **kwargs)
        self.setWindowTitle('info')
        self.resize(200,200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.frame = QFrame(self)
        self.modifiedtime = QtWidgets.QLabel() #modifiedtime方法应该是内置于文件类中的，返回一个string变量，是最后修改时间
        self.modifiedtime.setText(file_info.modifiedtime)
        self.size = QtWidgets.QLabel()
        self.size.setText(file_info.size)



class logindialog(QDialog): # This is the class for the login dialog
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.resize(400, 300)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        ###### 设置界面控件
        self.frame = QFrame(self)
        self.frame.resize(400,300)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.label_account = QtWidgets.QLabel()
        self.label_account.setText("Username")
        self.label_account.setFixedSize(400,20)
        self.verticalLayout.addWidget(self.label_account)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setFixedSize(370,30)
        #self.lineEdit_account.setPlaceholderText("Username")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.label_password = QLabel()
        self.label_password.setText("Password")
        self.label_password.setFixedSize(400,20)
        self.verticalLayout.addWidget(self.label_password)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setFixedSize(370,30)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        #self.lineEdit_password.setPlaceholderText("Password")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("Sign In")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("Cancel")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)
        

    def on_pushButton_enter_clicked(self):
        # Verify Account
        if self.lineEdit_account.text() == "":
            return
        # Verify password
        if self.lineEdit_password.text() == "":
            return
        # Password Verified
        self.accept()



app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
dialog = logindialog()
if dialog.exec_() == QDialog.Accepted:
    Form = QMainWindow()
    ui = Ui_Exile()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
