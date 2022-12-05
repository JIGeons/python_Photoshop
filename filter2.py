import numpy as np, cv2


image = cv2.imread("images/me.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상파일 읽기 오류")

def cartoon_filter(img):
    h, w = img.shape[:2]
    img2 = cv2.resize(img, (w//2, h//2))

    blr = cv2.bilateralFilter(img2, -1, 20, 7)
    edge = 255 - cv2.Canny(img2, 80, 120)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    dst = cv2.bitwise_and(np.array(blr, dtype = np.uint8), np.array(edge, dtype = np.uint8)) # and연산
    dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)
                                                                  
    return dst

image = cartoon_filter(image)
cv2.imshow("cartoon", image)
																	
cv2.waitKey(0)