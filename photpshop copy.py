import sys
import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *   # 위젯을 사용하기 위해 QtWidgets import
from PyQt5.QtGui import *       # QPixmap을 사용하기 위해 QtGui import
from PyQt5 import QtGui       # QPixmap을 사용하기 위해 QtGui import
from PyQt5 import uic
from PyQt5.QtCore import Qt

form_class = uic.loadUiType('E:\\2022_workspace\\python_Photoshop\\photoshop.ui')[0]
changed_image = "log/log_image.jpg" # 필터 적용시 잠시 저장용 

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

        self.opened = False     # 파일을 열었는지 않열었는지 구분하기 위함
        self.opened_file_path = "제목 없음"
        self.original_image = QLabel()

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
        file_image.load(self.opened_file_path)
        self.original_image.setPixmap(file_image)
        file_image = self.original_image.pixmap()

        if current_Image == file_image:   # 열린적이 있고 변경사항이 없으면
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

    def mouseMoveEvent(self, event):
        MouseTracking_Location = "Tracking For Mouse Location: x axis = {0}, y axis ={1}, global x,y = {2}, {3}".format(event.x(), event.y(), event.globalX(), event.globalY())
        print(MouseTracking_Location)
    
    #마우스가 눌렸을 때 해당 이미지 옮기기
    def mousePressEvent(self, e):
        print("안녕",e)
        
    def chooseFunction(self):   # 선택하기 버튼
        #크기 작아지는 것
        print(self.label_image.pixmap().size().width)
        origin_width = self.label_image.pixmap().size().width()
        self.label_image.setPixmap(self.label_image.pixmap().scaledToWidth(origin_width-10))
        print(self.label_image.pixmap())

    def blackFunction(self):   # 사진 흑백으로 전환
        image = cv.imread(self.opened_file_path, cv.IMREAD_GRAYSCALE)   # 사진 opencv 사용해서 흑백으로 전환
        cv.imwrite(changed_image, image)        # label에 set을 하려면 이미지 파일이어야 하기 때문에 미리 설정한 log image로 저장
        self.canvas.load(changed_image)         # log image canvas에 로드 후
        self.label_image.setPixmap(self.canvas) # label로 이미지 출력

    def redFunction(self):   # 사진 흑백으로 전환
        image = cv.imread(self.opened_file_path)
        image[:,:,1] = 0    # 모든 픽셀에 대해 index 0는 R, 1은 G, 2는 B을 의미함
        image[:,:,2] = 0    # Blue만 뽑기 위해 1과, 2 즉, Green와 Blue를 0으로 변환
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        cv.imwrite(changed_image, image)
        self.canvas.load(changed_image)
        self.label_image.setPixmap(self.canvas)

    def greenFunction(self):
        image = cv.imread(self.opened_file_path)
        image[:,:,0] = 0    # 모든 픽셀에 대해 index 0는 R, 1은 G, 2는 B을 의미함
        image[:,:,2] = 0    # Green만 뽑기 위해 0과, 2 즉, Red와 Blue를 0으로 변환
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        cv.imwrite(changed_image, image)
        self.canvas.load(changed_image)
        self.label_image.setPixmap(self.canvas)

    def blueFunction(self):
        image = cv.imread(self.opened_file_path)
        image[:,:,0] = 0    # 모든 픽셀에 대해 index 0는 R, 1은 G, 2는 B을 의미함
        image[:,:,1] = 0    # Red만 뽑기 위해 0과, 1 즉, Red와 Green을 0으로 변환
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        cv.imwrite(changed_image, image)
        self.canvas.load(changed_image)
        self.label_image.setPixmap(self.canvas)

    def spoidFunction(self):
        return
    def cloneFunction(self):
        return
    def cutFunction(self):
        return
    def boundFunction(self):
        return
    def brushFunction(self):
        return
    
app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec()