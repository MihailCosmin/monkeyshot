"""monkeyShot provides a tool for making easy screenshots
"""
from os.path import join
from os.path import expanduser

from pathlib import Path

from tkinter import Tk
from tkinter import Label
from tkinter import Frame
from tkinter import Canvas
from tkinter import Button
from tkinter import Toplevel

from pyautogui import position
from pyautogui import screenshot

from PIL import ImageTk

from idlelib.tooltip import Hovertip

class MonkeyHouse:
    """GUI for MonkeyShot
    """
    def __init__(self):
        self.last_click_x = 0
        self.last_click_y = 0
        self.main_window()

    def main_window(self):
        self.window = Tk()
        # self.window['cursor'] = 'diamond_cross'
        self.window.overrideredirect(True)
        self.window.title('MonkeyHouse')
        self.window.configure(bg='black')
        self.window.resizable(False, False)
        self.window.geometry('400x100+200+200')
        self.window.iconbitmap(r'C:\Users\munte\OneDrive\Desktop\Test\monkey.ico')

        self.title_bar = Frame(self.window, bg='black', relief='raised', bd=2, highlightthickness=0)

        self.close_button_img = ImageTk.PhotoImage(
            file="C:\\Users\\munte\\OneDrive\\Desktop\\Test\\close_button_24px_#AA0000.png"
        )

        self.close_button = Button(
            self.title_bar,
            # text='X',
            image=self.close_button_img,
            command=self.window.destroy,
            bg="black",
            padx=2,
            pady=2,
            bd=0,
            font="bold",
            fg='red',
            highlightthickness=0
        )

        self.canvas = Canvas(self.window, bg='black', highlightthickness=0)
        self.window.attributes('-alpha', 0.8, '-topmost', 1)

        self.title_bar.pack(expand=1, fill='x')
        self.close_button.pack(side='right')

        self.static_screenshot_button_img = ImageTk.PhotoImage(
            file="C:\\Users\\munte\\OneDrive\\Desktop\\Test\\static_screenshot_button_48px_#AA0000.png"
        )
        self.dynamic_screenshot_button_img = ImageTk.PhotoImage(
            file="C:\\Users\\munte\\OneDrive\\Desktop\\Test\\dynamic_screenshot_button_48px_#AA0000.png"
        )

        self.static_screenshot_button = Button(
            self.canvas,
            image=self.static_screenshot_button_img,
            command=self.monkey_shot,
            bg="black",
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=10
        )
        self.dynamic_screenshot_button = Button(
            self.canvas,
            image=self.dynamic_screenshot_button_img,
            command=lambda: self.monkey_shot('dynamic'),
            bg="black",
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=10
        )

        self.static_screenshot_button.pack(side='left')
        self.dynamic_screenshot_button.pack(side='left')

        static_screenshot_button_tooltip = Hovertip(
            self.static_screenshot_button,
            'Static Screenshot using Crosshair'
        )
        dynamic_screenshot_button_tooltip = Hovertip(
            self.dynamic_screenshot_button,
            'Dynamic Screenshot using Crosshair'
        )

        self.canvas.pack(expand=1, fill='both')

        self.title_bar.bind('<Button-1>', self._save_last_click)
        self.title_bar.bind('<B1-Motion>', self._window_moving)

        self.window.mainloop()

    def monkey_shot(self, mode='static'):
        self.window.withdraw()
        screenshot_session = MonkeyShot()
        screenshot_session.shoot(mode)
        self.window.deiconify()

    def _save_last_click(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

    def _window_moving(self, event):
        x, y = event.x - self.last_click_x + self.window.winfo_x(), event.y - self.last_click_y + self.window.winfo_y()
        self.window.geometry(f'+{x}+{y}')

class MonkeyShot:
    """Take screenshot of specific region, using a croshair for selection
    """
    def __init__(self):
        self._clicks = 0
        self._points = []
        self.location = expanduser("~/Desktop")
        self.name = "cyberMonkeyScreenShort.jpg"
        self.window = None
        self.canvas = None

    def shoot(self, mode: str = 'static'):
        """Take the screenshot

        Args:
            mode (str, optional): Screenshot mode, can be static or dynamic.
            - Static mode: first take a screenshot of complete screen that draw crosshair on top.
              This mode provides a clearer view of what is behind, but cannot be used to capture live images from videos.
            - Dynamic mode: uses transparency. But the image is a more fuzzy and the corsshair is also partially transparent.
              This mode can be used to capture live images from videos.
            Defaults to 'static'.
        """
        if mode == 'static':
            transparency = 1
        elif mode == 'dynamic':
            transparency = 0.4
        self.window = Toplevel()  # Tk()
        self.window.attributes('-fullscreen', True, '-alpha', transparency)
        self.window.configure(bg='black')

        self.canvas = Canvas(
            self.window,
            width=self.window.winfo_screenwidth(),
            height=self.window.winfo_screenheight(),
            cursor="crosshair"
        )
        self.canvas.configure(highlightthickness=0, bg='black')
        self.canvas.bind("<Button-1>", self._two_clicks)
        self.canvas.pack()

        if mode == 'static':
            self.canvas.image = ImageTk.PhotoImage(screenshot())
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

        self.window.after(1, self._crosshair, None, None, None)
        self.window.mainloop()

    def set_location(self, loc: str):
        """Set location where to save the screenshot

        Args:
            loc (str): Folder Path
        """
        self.location = loc

    def set_name(self, nam: str):
        """Set name of the image

        Args:
            nam (str): Filename for the screenshot
        """
        self.name = nam

    def _take_screenshot(self):
        x_1, y_1 = self._points[0]
        x_2, y_2 = self._points[1]

        if x_1 > x_2 and y_1 < y_2:
            top_left_x = x_2
            top_left_y = y_1
            width = x_1 - x_2
            height = y_2 - y_1
        elif x_1 < x_2 and y_1 < y_2:
            top_left_x = x_1
            top_left_y = y_1
            width = x_2 - x_1
            height = y_2 - y_1
        elif x_1 < x_2 and y_1 > y_2:
            top_left_x = x_1
            top_left_y = y_2
            width = x_2 - x_1
            height = y_1 - y_2
        elif x_1 > x_2 and y_1 > y_2:
            top_left_x = x_2
            top_left_y = y_2
            width = x_1 - x_2
            height = y_1 - y_2

        screenshot(Path(join(self.location, self.name)),
                   region=(top_left_x,
                           top_left_y,
                           width,
                           height))
        self.window.quit()

    def _crosshair(self, vertical, horizontal, rectangle):
        if self._clicks == 0:
            x_point, y_point = position()

            self.canvas.delete(vertical)
            self.canvas.delete(horizontal)

            vertical = self.canvas.create_line(
                x_point,
                self.window.winfo_screenheight(),
                x_point,
                0,
                fill='red'
            )
            horizontal = self.canvas.create_line(
                0,
                y_point,
                self.window.winfo_screenwidth(),
                y_point,
                fill='red'
            )
        elif self._clicks == 1:
            self.canvas.delete(vertical)
            self.canvas.delete(horizontal)
            self.canvas.delete(rectangle)
            rectangle = self.canvas.create_rectangle(
                self._points[0][0],
                self._points[0][1],
                position()[0],
                position()[1],
                outline='red'
            )

        self.window.after(1, self._crosshair, vertical, horizontal, rectangle)

    def _two_clicks(self, event):
        self._clicks += 1
        self._points.append((event.x, event.y))
        if self._clicks == 2:
            self.window.destroy()
            self._take_screenshot()

if __name__ == '__main__':
    '''app = MonkeyShot()
    app.shoot()'''
    MonkeyHouse()
