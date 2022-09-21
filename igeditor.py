from time import sleep
import pyautogui
from pyautogui import press
import win32con
import win32gui

class IGEditor:

    def __init__(self):
        pyautogui.FAILSAFE = True
        self.hwnd = self.getWindow('IGEditor')
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(self.hwnd)
    
    def getAllHwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwndTitles[hwnd] = win32gui.GetWindowText(hwnd)
    def getWindow(self, suffix:str):
        self.hwndTitles:dict[int, str] = {}
        win32gui.EnumWindows(self.getAllHwnd, 0)
        for hwnd, title in self.hwndTitles.items():
            if title.endswith(suffix):
                return hwnd

    def addObject(self):
        self.click('alt')
        self.click('right', 4)
        self.click('enter')
        self.click('down', 7)
        self.click('enter')
    def importObject(self, path:str):
        self.click('alt')
        self.click('right', 4)
        self.click('enter')
        self.click('down', 16)
        self.click('enter')
        while True:
            dialogHwnd = self.getWindow('打开')
            sleep(0.05)
            if dialogHwnd:
                break
        pyautogui.typewrite(path)
        sleep(0.05)
        self.click('tab', 2)
        self.click('enter')

    def click(self, key, presses=1):
        for i in range(presses):
            press(key)
            sleep(0.05)

    
if __name__ == '__main__':
    IGEditor()



