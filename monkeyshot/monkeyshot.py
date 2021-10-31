"""monkeyShot is an applciation for making screenshots and video recording
"""

from shutil import move

from os import remove
from os.path import join
from os.path import isfile
from os.path import dirname
from os.path import realpath
from os.path import expanduser

from tkinter import Tk
from tkinter import Frame
from tkinter import Canvas
from tkinter import Button
from tkinter import Toplevel
from tkinter.filedialog import asksaveasfilename

from pyautogui import size
from pyautogui import position
from pyautogui import screenshot

from keyboard import is_pressed

from PIL import ImageTk

from idlelib.tooltip import Hovertip

from numpy import array

from cv2 import cvtColor
from cv2 import VideoWriter
from cv2 import COLOR_BGR2RGB
from cv2 import VideoWriter_fourcc

IMAGES = [
    ('JPEG Image', '*.jpg'),
    ('PNG Image', '*.png'),
    ('TIFF Image', '*.tif'),
    ('WEBP Image', '*.webp'),
    ('BMP Image', '*.bmp'),
    ('GIF Image', '*.gif'),
    ('All Image Formats', '*.*'),
]

VIDEOS = [
    ('MP4 Video', '*.mp4'),
    ('AVI Video', '*.avi'),
    ('MKV Video', '*.mkv'),
    ('WEBM Video', '*.webm'),
    ('WMV Video', '*.wmv'),
    ('All Video Formats', '*.*'),
]


class MonkeyHouse:
    """GUI for MonkeyShot
    """
    def __init__(self):
        self.last_click_x = 0
        self.last_click_y = 0
        self.region = None
        self.main_window()

    def main_window(self):
        self.window = Tk()
        self.window.overrideredirect(True)
        self.window.title('MonkeyHouse')
        self.window.configure(bg='black')
        self.window.resizable(False, False)
        self.window.geometry('400x100+200+200')

        self.title_bar = Frame(self.window, bg='black', relief='raised', bd=2, highlightthickness=0)

        self.close_button_img = ImageTk.PhotoImage(
            file=join(
                dirname(realpath(__file__)),
                "img",
                "close_button_24px_#AA0000.png"
            )
        )

        self.close_button = Button(
            self.title_bar,
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
            file=join(
                dirname(realpath(__file__)),
                "img",
                "static_screenshot_button_48px_#AA0000.png"
            )
        )

        self.dynamic_screenshot_button_img = ImageTk.PhotoImage(
            file=join(
                dirname(realpath(__file__)),
                "img",
                "dynamic_screenshot_button_48px_#AA0000.png"
            )
        )

        self.record_button_img = ImageTk.PhotoImage(
            file=join(
                dirname(realpath(__file__)),
                "img",
                "record_button_48px_#AA0000.png"
            )
        )

        self.region_record_button_img = ImageTk.PhotoImage(
            file=join(
                dirname(realpath(__file__)),
                "img",
                "region_record_button_48px_#AA0000.png"
            )
        )

        self.settings_button_img = ImageTk.PhotoImage(
            file=join(
                dirname(realpath(__file__)),
                "img",
                "settings_button_48px_#AA0000.png"
            )
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
        self.record_button = Button(
            self.canvas,
            image=self.record_button_img,
            command=self.monkey_see,
            bg="black",
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=10
        )
        self.region_record_button = Button(
            self.canvas,
            image=self.region_record_button_img,
            command=lambda: self.monkey_see(fullscreen=False),
            bg="black",
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=10
        )
        self.settings_button = Button(
            self.canvas,
            image=self.settings_button_img,
            command=None,
            bg="black",
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=10
        )

        self.static_screenshot_button.pack(side='left')
        self.dynamic_screenshot_button.pack(side='left')
        self.record_button.pack(side='left')
        self.region_record_button.pack(side='left')
        self.settings_button.pack(side='right')

        Hovertip(
            self.static_screenshot_button,
            'Static Screenshot using Crosshair'
        )
        Hovertip(
            self.dynamic_screenshot_button,
            'Dynamic Screenshot using Crosshair'
        )
        Hovertip(
            self.record_button,
            'Fullscreen recording'
        )
        Hovertip(
            self.region_record_button,
            'Specific region recording'
        )
        Hovertip(
            self.settings_button,
            'Settings'
        )

        self.canvas.pack(expand=1, fill='both')

        self.title_bar.bind('<Button-1>', self._save_last_click)
        self.title_bar.bind('<B1-Motion>', self._window_moving)

        self.window.mainloop()

    def monkey_shot(self, mode: str = 'static'):
        """Call screenshot function

        Args:
            mode (str, optional): Screenshot mode. Defaults to 'static'.
        """
        self.window.withdraw()
        screenshot_session = MonkeyShot()
        monkey_screenshot = screenshot_session.shoot(mode)
        self.window.deiconify()
        try:
            monkey_screenshot.save(asksaveasfilename(filetypes=IMAGES, defaultextension=IMAGES))
        except ValueError:
            pass

    def monkey_see(self, fullscreen: bool = True):
        """Call video recording function

        Args:
            fullscreen (bool, optional): Fullscreen recording. Defaults to True.
        """
        self.window.withdraw()
        recording_session = MonkeyShot()
        if fullscreen:
            recording_session.record()
        else:
            recording_session.shoot(mode='video')
        self.window.deiconify()
        monkey_recording = asksaveasfilename(filetypes=VIDEOS, defaultextension=VIDEOS)
        if isfile(monkey_recording):
            remove(monkey_recording)
        move("Recording.mp4", monkey_recording)

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
        self.filename = join(expanduser("~/Desktop"), "cyberMonkeyScreenShort.jpg")
        self.monkey_screenshot = None
        self.mode = None
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
            self.mode = 'screenshot'
        elif mode == 'dynamic':
            transparency = 0.4
            self.mode = 'screenshot'
        elif mode == 'video':
            transparency = 1
            self.mode = 'video'
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

        if mode in ('static', 'video'):
            self.canvas.image = ImageTk.PhotoImage(screenshot())
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

        self.window.after(1, self._crosshair, None, None, None)
        self.window.mainloop()
        return self.monkey_screenshot

    def record(self, region=None):
        resolution = (size())
        if region is not None:
            resolution = (region[2], region[3])
        # codec = cv2.VideoWriter_fourcc(*"XVID")  # AVI
        codec = VideoWriter_fourcc(*'mp4v')  # MP4
        fps = 24.0
        out = VideoWriter("Recording.mp4", codec, fps, resolution)
        run = True

        while run:
            if region is not None:
                img = screenshot(region=region)
            else:
                img = screenshot()
            frame = array(img)
            frame = cvtColor(frame, COLOR_BGR2RGB)
            out.write(frame)
            if is_pressed('esc'):
                run = False

        out.release()
        return out

    def set_filename(self, fname: str):
        """Set name of the image

        Args:
            nam (str): Filename for the screenshot
        """
        self.filename = fname

    @staticmethod
    def _points_to_region(pt1: list, pt2: list) -> tuple:
        x_1, y_1 = pt1
        x_2, y_2 = pt2

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

        return (top_left_x, top_left_y, width, height)

    def _run(self):
        reg = self._points_to_region(self._points[0], self._points[1])
        if self.mode == 'video':
            self.record(reg)
        elif self.mode == 'screenshot':
            self.monkey_screenshot = screenshot(region=reg)
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
            self._run()

if __name__ == '__main__':
    MonkeyHouse()
