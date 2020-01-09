import webbrowser
from enum import Enum, unique
from typing import Tuple, Optional
from time import sleep, time

import numpy as np
import pyautogui
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.feature import match_template
from mss import mss


@unique
class State(Enum):
    NORM = 1
    UP = 2
    DOWN = 3


class Dino:
    def __init__(self, template: np.ndarray) -> None:
        super().__init__()
        self._template: np.ndarray = template
        self._dino_position: Optional[Tuple[int, int]] = None
        self._initialized = False
        self._monitor = None
        self._state: State = State.NORM
        self._last_time: int = int(time())
        self._speed = 15

    def init(self, sleep_delay=7):
        self._open_browser(sleep_delay)
        scm = mss()
        monitor = scm.monitors[0]
        monitor['top'] = 190
        monitor['left'] = 25
        monitor['width'] = 800
        monitor['height'] = 270

        pyautogui.PAUSE = 0
        pyautogui.MINIMUM_DURATION = 0.008
        pyautogui.MINIMUM_SLEEP = 0.000

        dino_position = None
        while dino_position is None:
            shot = np.array(scm.grab(monitor))
            gray_shot = rgb2gray(shot)
            dino_position = self._find_dino_on_shot(gray_shot)
        self._up()
        sleep(3)
        shot = np.array(scm.grab(monitor))
        gray_shot = rgb2gray(shot)
        dino_position = self._find_dino_on_shot(gray_shot)
        scm.close()

        self._monitor = monitor
        self._dino_position = dino_position
        self._initialized = True

    def start(self):
        if not self._initialized:
            raise UninitializedError
        scm = mss()
        self._up()
        last_time = time()
        while True:
            curr_time = time()
            # print(f"Time spent: {curr_time - last_time}")
            last_time = curr_time
            shot = np.array(scm.grab(self._monitor))
            gray_shot = rgb2gray(shot)
            self._handle_shot(gray_shot)
            # break
        scm.close()

    @staticmethod
    def _up():
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        # pyautogui.keyDown('down')

    @staticmethod
    def _down():
        # pass
        # pyautogui.keyUp('space')
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')

    @staticmethod
    def _open_browser(sleep_delay):
        # webbrowser.open('https://chromedino.com/')
        webbrowser.open('https://dino.zone/ru/')
        sleep(sleep_delay)

    def _find_dino_on_shot(self, shot: np.ndarray) -> Optional[Tuple[int, int]]:
        result = match_template(shot, self._template)
        max_value = np.argmax(result)
        ij = np.unravel_index(max_value, result.shape)
        if max_value < 1:
            return None
        y, x = ij
        return x, y

    def _handle_shot(self, shot: np.ndarray):
        dino_position = self._dino_position
        template_shape = self._template.shape

        if int(time()) - self._last_time > 2:
            self._last_time = int(time())
            self._speed += 2
            if self._speed > 200:
                self._speed = 200

        x, y = dino_position
        t_h, t_w = template_shape

        prev_state = self._state

        mid_y = y + t_h // 2
        next_x_1 = x + t_w + (t_w // 3)  # if prev_state == DOWN else 0
        next_x_2 = next_x_1 + int(self._speed)
        # next_x_2 = int(next_x_2)
        next_low_pixel = np.min(shot[mid_y, next_x_1:next_x_2])
        # next_low_pixel = shot[mid_y, next_x]
        if next_low_pixel < 0.4 and prev_state != State.UP:
            self._state = State.UP
            # self._up()
        else:
            if self._state == State.DOWN:
                next_x_1 = x
            next_high_pixel = np.min(shot[y - 4:y - 3, next_x_1:next_x_2])
            if next_high_pixel < 0.4:
                self._state = State.DOWN
                # self._down()
            else:
                self._state = State.NORM

        curr_state = self._state
        if prev_state != curr_state:
            print(prev_state, curr_state)
            if prev_state == State.UP:
                pyautogui.keyUp('up')
                if curr_state == State.DOWN:
                    pyautogui.keyDown('down')
                elif curr_state == State.NORM:
                    pass
            elif prev_state == State.NORM:
                if curr_state == State.DOWN:
                    pyautogui.keyDown('down')
                elif curr_state == State.UP:
                    pyautogui.keyDown('up')
            elif prev_state == State.DOWN:
                pyautogui.keyUp('down')
                if curr_state == State.UP:
                    pyautogui.keyDown('up')
                elif curr_state == State.NORM:
                    pass

        # print(shot.shape)
        # print(next_low_pixel)
        # plt.figure(figsize=(16, 9), dpi=100)
        # plt.imshow(shot, cmap=plt.get_cmap('gray'))
        # plt.plot([next_x_1, next_x_2], [mid_y, mid_y], 'ro')
        # plt.plot(next_x, mid_y, 'ro')
        # plt.show()


class UninitializedError:
    pass
