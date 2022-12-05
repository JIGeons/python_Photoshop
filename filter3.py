import numpy as np, cv2

def make_noise(std, gray):
    height, width = gray.shape
    img_noise = np.zeros((height, width), dtype=np.float)
    for i in range(height):
        for a in range(width):
            make_noise = np.random.normal()  # 랜덤함수를 이용하여 노이즈 적용
            set_noise = std * make_noise
            img_noise[i][a] = gray[i][a] + set_noise
    return img_noise


def filter3(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    std = 15
    img_noise = make_noise(std, gray)
    img_noise2 = make_noise(std, gray)
    img_noise3 = make_noise(std, gray)

    out3 = np.zeros((height, width), dtype=np.uint8)
    
    # 평균 계산
    for i in range(height):
        for j in range(width):
            if (img_noise[i][j] + img_noise2[i][j]) / 3 > 255:
                out3[i][j] = np.random.normal()
            else:
                out3[i][j] = (img_noise[i][j] + img_noise2[i][j]) / 3

    cv2.imshow('avr3', out3.astype(np.uint8))
    cv2.waitKey(0)

run()