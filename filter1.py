import numpy as np, cv2

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

image = cv2.imread("images/me.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상파일 읽기 오류")

ksize = (20, 32)                                        # 크기는 가로x세로로 표현
gaussian_2d = getGaussianMask(ksize, 0, -1)

gauss_img1 = cv2.filter2D(image, -1, gaussian_2d)     # 사용자 생성 마스크 적용
gauss_img1 = cv2.resize(gauss_img1, (500,400))

cv2.imshow("filter1", gauss_img1)

val = np.full(gauss_img1.shape, 20, np.uint8)            # 증가 화소값 행렬 생성
cv2.add(gauss_img1, val, gauss_img1)


titles = ['gauss_img1']
cv2.imshow("filter2", gauss_img1)
cv2.waitKey(0)