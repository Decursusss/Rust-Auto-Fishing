import cv2
import mss
import pyautogui
import win32api
import win32gui
import win32con
import numpy as np
import pygetwindow as gw

window_rect = None

def get_window_rect(window_title_substring):
    global window_rect

    if window_rect:
        return window_rect

    for window in gw.getWindowsWithTitle(''):
        if window_title_substring.lower() in window.title.lower():
            hwnd = window._hWnd
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetForegroundWindow(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            window_rect = rect
            return rect
    return None

def capture_window(window_title_substring):
    rect = get_window_rect(window_title_substring)
    if rect:
        x1, y1, x2, y2 = rect
        width, height = x2 - x1, y2 - y1

        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": width, "height": height}
            sct_img = sct.grab(monitor)

            img = np.array(sct_img, dtype=np.uint8)
            if img is None or img.size == 0:
                print("Ошибка: пустой кадр!")
                return None

            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
    return None

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Левая кнопка мыши: ({x}, {y})")
    elif event == cv2.EVENT_RBUTTONDOWN:
        print(f"Правая кнопка мыши: ({x}, {y})")

cv2.namedWindow("Кликни для получения координат")
cv2.setMouseCallback("Кликни для получения координат", click_event)

print("Кликайте на окне, чтобы увидеть координаты. Для выхода нажмите 'q'.")

while True:
    frame = capture_window("Rust")

    if frame is not None:
        cv2.imshow("Кликни для получения координат", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
