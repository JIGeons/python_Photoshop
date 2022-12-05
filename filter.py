import numpy as np, cv2

def cartoon_filter(img):
    h, w = img.shape[:2]
    img2 = cv2.resize(img, (w//2, h//2))

    blr = cv2.bilateralFilter(img2, -1, 20, 7)
    edge = 255 - cv2.Canny(img2, 80, 120)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    dst = cv2.bitwise_and(np.array(blr, dtype = np.uint8), np.array(edge, dtype = np.uint8)) # and연산
    dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)
                                                                  
    return dst

def getGaussianMask(ksize, sigmaX, sigmaY):
    sigma = 0.03 * ((np.array(ksize)-1.0) * 0.5 - 1.0) + 0.08  # 표준 편차
    if sigmaX <= 0: sigmaX = sigma[0]
    if sigmaY <= 0: sigmaY = sigma[1]

    u = np.array(ksize)//2
    x = np.arange(-u[0], u[0]+1, 1)
    y = np.arange(-u[1], u[1]+1, 1)
    x, y = np.meshgrid(x, y)

    ratio = 1 / (sigmaX*sigmaY * 2 * np.pi)
    v1 = x ** 2 / (2 * sigmaX ** 2)
    v2 = y ** 2 / (2 * sigmaY ** 2 )
    mask = ratio * np.exp(-(v1+v2))
    return mask / np.sum(mask)


def filter1(image):
    ksize = (20, 32)                                        # 크기는 가로x세로로 표현
    gaussian_2d = getGaussianMask(ksize, 0, -1)

    gauss_img1 = cv2.filter2D(image, -1, gaussian_2d)     # 사용자 생성 마스크 적용

    val = np.full(gauss_img1.shape, 20, np.uint8)            # 증가 화소값 행렬 생성
    cv2.add(gauss_img1, val, gauss_img1)

    return gauss_img1

def make_noise(std, gray):
    height, width = gray.shape
    img_noise = np.zeros((height, width), dtype=np.uint8)
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

    out = np.zeros((height, width), dtype=np.uint8)
    
    # 평균 계산
    for i in range(height):
        for j in range(width):
            if (img_noise[i][j] + img_noise2[i][j]) / 2 > 255:
                out[i][j] = np.random.normal()
            else:
                out[i][j] = (img_noise[i][j] + img_noise2[i][j]) / 2
    
    return out