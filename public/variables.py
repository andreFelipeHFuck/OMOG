from enum import Enum

import pygame

class CurveEnum(Enum):
    NONE = 0
    C1 = 1
    C2 = 2
    ALL = 3
    HUX_C1 = 4,
    HUX_C2 = 5

RUNNING = False

SCREEN_WIDTH = 1_500
SCREEN_HEIGHT = 800

MENU_WIDTH = 0
MENU_HEIGHT = 75

X_ORIGIN = SCREEN_WIDTH // 2
Y_ORIGIN = SCREEN_HEIGHT // 2

# Quantas pixels representa uma unidade no plano 
SCALE = 40
STEP = 100

CARRY_ON = True
CURVE: CurveEnum = CurveEnum.NONE

C0_ACTIVE = False

ADD_POINT = False

COLORS = {
    "background": (255, 255, 255),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "transparent": (255, 255, 255, 0),
    "gray": (52, 49, 49),
    "point_1": (102, 0, 0),
    "curve_1": (176, 0, 32),#B00020
    "hux_curve_1": (0,250,154),
    "point_2": (11, 44, 65),
    "curve_2": (23, 86,  129),#175681
    "hux_curve_2": (75,0,130),
    "active": (201, 201, 201),
    "disabled": (227, 227, 227)
}

# Eventos personalizados 

RENDER_EVENT = pygame.USEREVENT + 1
C0_EVENT = pygame.USEREVENT + 2
C1_EVENT = pygame.USEREVENT + 3
C2_EVENT = pygame.USEREVENT + 4
ADD_POINT_EVENT = pygame.USEREVENT + 5
RESET_EVENT = pygame.USEREVENT + 6
FORM_POINT_EVENT = pygame.USEREVENT + 7
