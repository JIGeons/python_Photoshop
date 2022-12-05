"""
    그림판 프로그램 > 그리기 상수, 일반 명령 상수, 팔레트 관련 상수 정의 
"""
SELECT_RECTANGLE = 0    # 부분 선택
DRAW_CLONE     = 1      # 복제 도장
CUT            = 2      # 자르기
SELECT_LASSO   = 3      # 올가미
DRAW_BRUSH     = 4      # 브러시 그리기
ERASE          = 5      # 지우개
OPEN           = 6      # 열기 명령
SAVE           = 7      # 저장 명령
PLUS           = 8      # 필터 1
MINUS          = 9      # 필터 2
CREAR          = 10     # 지우기 명령
COLOR          = 11     # 색상 아이콘
PALETTE        = 12     # 색상팔레트
HUE_IDX        = 13     # 색상인덱스

# 전역 변수
mouse_mode, draw_mode = 0, 0                # 그리기 모드, 마우스 상태
pt1, pt2, Color = (0, 0), (0, 0), (0, 0, 0) # 시작 좌표, 종료 좌표
thickness = 3                               # 선 두께
