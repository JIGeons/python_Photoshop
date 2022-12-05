from paint_init import *
from paint_utils import *
from filter import *

def onMouse(event, x, y, flags, param):

    global pt1, pt2, pt3, mouse_mode, draw_mode

    if event == cv2.EVENT_LBUTTONUP:                    # 왼쪽 버튼 떼기
        for i, (x0, y0, w, h) in enumerate(icons):      # 메뉴아이콘 사각형 조회
            if x0 <= x < x0+ w and y0 <= y < y0 + h:    # 메뉴 클릭 여부 검사
                if i < 6:                               # 그리기 명령이면
                    mouse_mode = 0                      # 마우스 상태 초기화
                    draw_mode = i                       # 그리기 모드
                else:
                    command(i)              # 일반 명령이면
                return

        pt2 = (x, y)                        # 종료좌표 저장
        mouse_mode = 1                      # 버튼 떼기 상태 지정

    elif event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 누르기
        pt1 = (x, y)  # 시작좌표 저장
        mouse_mode = 2
    
    elif event == cv2.EVENT_RBUTTONDOWN:
        pt3 = (x,y)    # 복제할 좌표 저장
        mouse_mode = 1

    if mouse_mode >= 2:  # 왼쪽 버튼 누르기 또는 드래그
        mouse_mode = 0 if x < 125 else 3  # 메뉴 영역 확인- 마우스 상태 지정
        pt2 = (x, y)

def draw(image, color=(200, 200, 200)):
    global draw_mode, thickness, pt1, pt2

    if draw_mode == SELECT_RECTANGLE:       # 부분 선택
        print(pt1, pt2)
        canvas = image[pt1[1] : (pt2[1] - pt1[1]), pt1[0] : (pt2[0] - pt1[0])]  # 선택한 부분을 캔버스로 지정 그 부분만 수정을 해야하는데 어떻게..?
        cv2.rectangle(image, pt1, pt2, (150,0,0), 1)

    elif draw_mode == DRAW_CLONE:
        pixel = image[pt3[::-1]]
        x, y, w, h = icons[COLOR]
        image[:,:,:] = pixel[:,:,:]
        Color = tuple(map(int, pixel))
        color = Color
        cv2.line(image, pt1, pt2, color, thickness * 3)
        pt1 = pt2



    elif draw_mode == CUT:
        print(pt1, pt2)
        cv2.rectangle(image, pt1, pt2, (0,0,0), 1)
        if mouse_mode == 1 :
            w = pt2[1] - pt1[1]
            h = pt2[0] - pt1[0]
            canvas = image[pt1[1] : h, pt1[0] : w]
            canvas = scalling(canvas, (380, 800))
    
    elif draw_mode == SELECT_LASSO:
        cv2.line(image, pt1, pt2, color, thickness)

    elif draw_mode == DRAW_BRUSH:                   # 브러시 그리기
        cv2.line(image, pt1, pt2, color, thickness * 3)
        pt1 = pt2                               # 종료 좌표를 시작 좌표로 지정

    elif draw_mode == ERASE:                        # 지우개
        cv2.line(image, pt1, pt2, (255, 255, 255), thickness * 5)
        pt1 = pt2

    cv2.imshow("PaintCV", image)

def command(mode):
    global icons, image, canvas, Color, hue, mouse_mode, filter

    if mode == PALETTE:  # 색상팔레트 영역 클릭 시
        pixel = image[pt2[::-1]]
        x, y, w, h = icons[COLOR]
        image[y:y + h - 1, x:x + w - 1] = pixel
        Color = tuple(map(int, pixel))

    elif mode == HUE_IDX:  # 색상인텍스 클릭 시
        create_colorPlatte(image, pt2[0], icons[PALETTE])  # 팔레트 새로 그리기

    elif mode == OPEN:                                   # 영상 파일 열기
        tmp = cv2.imread("images/me.jpg", cv2.IMREAD_COLOR)
        cv2.resize(tmp, canvas.shape[1::-1], canvas)

    elif mode == SAVE:                                  # 캔버스 영역 저장
        cv2.imwrite("images/my_save.jpg", canvas)

    elif mode == PLUS:                                  # 캔버스 필터 적용
        canvas = image[:,120:image.shape[1]]
        if filter == 1 :
            canvas1 = filter1(canvas)
            print(canvas1)
            image[:,120:image.shape[1]] = canvas1
            filter = 2
        elif filter == 2 :
            image[:,120:image.shape[1]] = cartoon_filter(canvas)
            filter = 3
        else :
            image = filter3(canvas)
            filter = 1
            print(filter)
        

    elif mode == MINUS:                                 # 캔버스에 필터 적용
        copy = canvas
        if filter == 1 :
            image[:,120:image.shape[1]] = filter1(copy)
            filter = 3
        elif filter == 2 :
            image[:,120:image.shape[1]] = cartoon_filter(copy)
            filter = 1
        else :
            image[:,120:image.shape[1]] = filter3(copy)
            filter = 2
            print(filter)
        icons = place_icons(image, (60, 60))

    elif mode == CREAR:                                 # 캔버스 영역 전체 지우기
        canvas[:] = (255, 255, 255)                     # 캔버스를 흰색으로
        mouse_mode = 0                                  # 마우스 상태 초기화

    cv2.imshow("PaintCV", image)

def scalling(image, size):
    dst = np.zeros(size[::-1], image.dtype)
    ratioY, ratioX = np.divide(size[::-1], image.shape[:2])
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            i, j = int(y * ratioY), int(x * ratioX)
            dst[i,j] = image[y,x]
    return dst
     
def onTrackbar(value):                                   # 트랙바 콜백 함수
    global mouse_mode, thickness
    mouse_mode = 0                                       # 마우스 상태 초기화
    thickness = value

def onTrackbar_br(value):                                # 트랙바 콜백 함수
    if value > 10 :
        val = np.full(canvas.shape, value - 10, np.uint8)            # 증가 화소값 행렬 생성
        cv2.add(canvas, val, canvas)      
    else :
        val = np.full(canvas.shape, (-value + 10), np.uint8)
        cv2.subtract(canvas, val, canvas)

    cv2.imshow("PaintCV", image)

image = np.full((500, 800, 3), 255, np.uint8)
icons = place_icons(image, (60, 60))            # 아이콘 배치, 아이콘 크기
x, y, w, h = icons[-1]                          # 아이콘 사각형 마지막 원소

canvas = image[:, w*2:image.shape[1]]           # 메뉴를 제외한 캔버스 영역

icons.append((0, y + h + 2  , 120, 120) )       # 팔레트 사각형 추가
icons.append((0, y + h + 124, 120, 15))         # 색상인덱스 사각형 추z가
create_colorPlatte(image, 0, icons[PALETTE])    # 팔레트 생성
create_hueIndex(image, icons[HUE_IDX])          # 색상인텍스 생성

cv2.imshow("PaintCV", image)
cv2.setMouseCallback("PaintCV", onMouse)               # 마우스 콜백 함수
cv2.createTrackbar("brightness", "PaintCV", 10, 20, onTrackbar_br)
cv2.createTrackbar("Thickness", "PaintCV", thickness, 255, onTrackbar)
cv2.createTrackbar("Thickness", "PaintCV", thickness, 255, onTrackbar)
 

while True:
    if mouse_mode == 1:                                # 마우스 버튼 떼기
        draw(image, Color)                             # 원본에 그림
    elif mouse_mode == 3:                              # 마우스 드래그 
        if draw_mode == DRAW_BRUSH or draw_mode == ERASE:
            draw(image, Color)                         # 원본에 그림
        else:
            draw(np.copy(image), (200, 200, 200))      # 복사본에 회색으로 그림
    if cv2.waitKey(30) == 27:                          # ESC 키를 누르면 종료 
        break