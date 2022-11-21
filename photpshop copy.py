import sys
import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *   # 위젯을 사용하기 위해 QtWidgets import
from PyQt5.QtGui import *       # QPixmap을 사용하기 위해 QtGui import
from PyQt5 import QtGui       # QPixmap을 사용하기 위해 QtGui import
from PyQt5 import uic

form_class = uic.loadUiType('C:\\Users\\user\\Desktop\\영상처리프로그래밍 프로젝트\\photoshop.ui')[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_Open.triggered.connect(self.openFunction)       # 열기
        self.action_Save.triggered.connect(self.saveFunction)       # 저장
        self.action_SaveAs.triggered.connect(self.saveAsFunction)   # 다른 이름으로 저장
        self.action_Close.triggered.connect(self.close)             # 종료

        self.action_Undo.triggered.connect(self.UndoFunction)       # 실행 취소
        self.action_Redo.triggered.connect(self.RedoFunction)       # 재실행
        self.action_Cut.triggered.connect(self.CutFunction)         # 잘라내기
        self.action_Copy.triggered.connect(self.CopyFunction)       # 복사
        self.action_Paste.triggered.connect(self.PasteFunction)     # 붙여넣기

        self.B_choose.clicked.connect(self.chooseFunction)           # 선택하기
        self.B_black.clicked.connect(self.blackFunction)           # 선택하기
        self.B_choose.clicked.connect(self.chooseFunction)           # 선택하기

        self.opened = False     # 파일을 열었는지 않열었는지 구분하기 위함
        self.opened_file_path = '제목 없음'

        self.canvas = QPixmap()

    def ischanged(self):
        if not self.opened:
            if self.label_image.pixmap(): # 열린적이 있고 변경사항이 있으면 # 열린적은 없는데 에디터 내용이 있으면
                print(self.label_image.pixmap())
                return True
            return False
        
        # 현재 데이터
        current_Image = self.label_image.pixmap()

        # 파일에 저장된 데이터
        with open(self.opened_file_path) as f:
            file_image = QPixmap().load(f)

        if current_Image == file_image.pixmap():   # 열린적이 있고 변경사항이 없으면
            return False
        else:           # 열린적이 있고 변경사항이 있으면
            return True  

    
    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton('저장', QMessageBox.YesRole)       #0
        msgBox.addButton('저장 안 함',QMessageBox.NoRole)   #1
        msgBox.addButton('취소',QMessageBox.RejectRole)     #2
        ret = msgBox.exec_()

        if ret == 0:
            self.saveFunction()
        else:
            return ret


    def closeEvent(self, event):
        if self.ischanged():  # 열린적이 있고 변경사항이 있으면 # 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()

            if ret == 2:
                event.ignore()

    # 파일 열기 함수
    def open_file(self, fname):
        self.canvas.load(fname)
        self.label_image.setPixmap(self.canvas.scaledToWidth(300))
        self.image = cv.imread(fname, cv.IMREAD_COLOR)

        self.opened = True
        self.opened_file_path = fname
        print(self.opened_file_path)

    # 파일 열기
    def openFunction(self):
        if self.ischanged():  # 변경사항이 있으면 저장
            ret = self.save_changed_data()
            
        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.open_file(fname[0])

    # 파일 저장 함수
    def save_file(self, fname):
        if not self.label_image.pixmap():   # 시작 화면 그대로 변경사항 없이 저장할 때
            self.canvas_save = QPixmap(self.label_image.size())

        else : self.canvas_save = self.label_image.pixmap()
        self.canvas_save.save(fname)
        #self.plainTextEdit.setPlainText(data)

    # 파일 저장
    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    # 다른 이름으로 저장
    def saveAsFunction(self):
        fsave = QFileDialog.getSaveFileName(self,'save image',"untitle","image files(*.jpg)")
        if fsave[0]:
            self.save_file(fsave[0])

    def UndoFunction(self):     # 실행 취소
        self.canvas.undo()

    def RedoFunction(self):     # 재실행
        self.canvas.redo()
    
    def CutFunction(self):      # 자르기
        self.canvas.cut()
    
    def CopyFunction(self):     # 복사
        self.canvas.copy()

    def PasteFunction(self):    # 붙여넣기
        self.canvas.paste()

    def chooseFunction(self):   # 선택하기
        x_min, x_max = 0,0
        value = list()
        for i in range(self.image.height()) :
            for j in range(self.image.width()) :
                value.append(self.image[i][j][0][0])
                x_min = min(value)
                x_max = max(value)
        
        y_min, y_max = 0,0
        value = list()
        for i in range(self.image.height()) :
            for j in range(self.image.width()) :
                value.append(self.image[i][j][0][1])
                y_min = min(value)
                y_max = max(value)

        return 1

    def blackFunction(self):   # 사진 흑백으로 전환
        print(1)
        name = str(self.opened_file_path)
        img_name = name.split('/')
        print(img_name[len(img_name)-1])
        image = cv.imread(img_name[len(img_name)-1])
        print(image)
        image_RGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        blackimage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        h, w = image.shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(blackimage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.canvas.load(pixmap)
        self.label_image.setPixmap(self.canvas)
            
    
app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec()