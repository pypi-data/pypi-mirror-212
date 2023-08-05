from customtkinter import CTk, CTkToplevel, CTkFrame, CTkLabel, CTkButton, ThemeManager, get_appearance_mode
from tkinter import ttk


class CTkCustom(CTk):
    def __init__(self, title: str = "", advanced: bool = True, **kwargs):
        try:
            super().__init__(**kwargs)
        except:
            pass
        from sys import platform
        from customtkinterx import CTkFluentThemePath
        if advanced:
            if platform == "win32":
                if "CTkCustom" in ThemeManager.theme:
                    self.__transparent_color = ThemeManager.theme["CTkCustom"]["transparent_color"]
                else:
                    self.__transparent_color = "#101010"
                self.attributes("-transparentcolor", self.__transparent_color)
                self.configure(fg_color=self.__transparent_color)
            elif platform == "darwin":
                self.__transparent_color = 'systemTransparent'
                self.attributes("-transparent", True)
                self.configure(fg_color=self.__transparent_color)
            else:
                self.__transparent_color = '#000001'

        self.wm_overrideredirect(True)

        if advanced:
            if platform == "win32":
                from ctypes import windll
                GWL_EXSTYLE = -20
                WS_EX_APPWINDOW = 0x00040000
                WS_EX_TOOLWINDOW = 0x00000080
                hwnd = windll.user32.GetParent(self.winfo_id())
                style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                style = style & ~WS_EX_TOOLWINDOW
                style = style | WS_EX_APPWINDOW
                res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            else:
                try:
                    self.wm_attributes("-topmost", True)
                except:
                    pass

        self.minsize(150, 180)

        self.__frame_border = CTkFrame(self, border_width=1,
                                       background_corner_colors=(
                                           self.__transparent_color,
                                           self.__transparent_color,
                                           self.__transparent_color,
                                           self.__transparent_color
                                       )
                                       )
        self.__frame_border.pack(fill="both", expand=True, padx=0, pady=0)

        self.__frame_title = CTkFrame(self.__frame_border, border_width=0, corner_radius=ThemeManager.theme["CTkFrame"]["corner_radius"]/2+2)
        self.__frame_title.pack(fill="x", side="top", padx=2, pady=2)
        self.bind_move(self.__frame_title)

        self.__label_title = CTkLabel(self.__frame_title, text=title)
        self.__label_title.pack(side="left", anchor="w", padx=10, pady=5)
        self.bind_move(self.__label_title)

        self.title(title)

        self.maximized = False

        self.__button_close = CTkButton(self.__frame_title, text="✕", width=30, height=30,
                                        command=lambda: self.destroy())
        self.__button_close.pack(side="right", anchor="e", padx=5, pady=5)

        self.__button_minimize = CTkButton(self.__frame_title, text="–", width=30, height=30,
                                           command=lambda: self.minimize())
        from sys import platform
        if platform == "win32":
            self.__button_minimize.pack(side="right", anchor="e", padx=5, pady=5)

        if "CTkCustom" in ThemeManager.theme:
            self.__button_close._text_color = ThemeManager.theme["CTkCustom"]["closebutton_text_color"]
            self.__button_close._fg_color = ThemeManager.theme["CTkCustom"]["closebutton_color"]
            self.__button_close._hover_color = ThemeManager.theme["CTkCustom"]["closebutton_hover_color"]
            self.__button_close._draw()

            self.__button_minimize._text_color = ThemeManager.theme["CTkCustom"]["minimizebutton_text_color"]
            self.__button_minimize._fg_color = ThemeManager.theme["CTkCustom"]["minimizebutton_color"]
            self.__button_minimize._hover_color = ThemeManager.theme["CTkCustom"]["minimizebutton_hover_color"]
            self.__button_minimize._draw()

        if platform == "linux":
            self.__frame_border.configure(corner_radius=0)

        self.x, self.y = 0, 0

    def minimize(self):
        try:
            from ctypes import windll
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.user32.ShowWindow(hwnd, 2)
        except:
            pass

    def bind_move(self, widget):
        widget.bind("<Button-1>", self._click)
        widget.bind("<B1-Motion>", self._move)

    def create_sizegrip(self):
        if get_appearance_mode() == "Dark":
            ttk.Style().configure("CTkCustom.TSizegrip", background=ThemeManager.theme["CTkFrame"]["fg_color"][1])
        else:
            ttk.Style().configure("CTkCustom.TSizegrip", background=ThemeManager.theme["CTkFrame"]["fg_color"][0])
        self.sizegrip = ttk.Sizegrip(self.__frame_border, style="CTkCustom.TSizegrip")
        self.sizegrip.pack(side="bottom", anchor="se", padx=5, pady=5, ipady=2)
        return self.sizegrip

    @property
    def titlebar(self):
        return self.__frame_title

    @property
    def titlebar_title(self):
        return self.__label_title

    @property
    def titlebar_closebutton(self):
        return self.__button_close

    @property
    def titlebar_minimizebutton(self):
        return self.__button_minimize

    @property
    def mainframe(self):
        return self.__frame_border

    def _click(self, event):
        self.x, self.y = event.x, event.y

    def _move(self, event):
        new_x = (event.x - self.x) + self.winfo_x()
        new_y = (event.y - self.y) + self.winfo_y()
        if new_y <= -self.__frame_title.winfo_height()+5:
            new_y = -self.__frame_title.winfo_height()+5
        s = f"+{new_x}+{new_y}"
        self.geometry(s)


class CTkCustomToplevel(CTkCustom, CTkToplevel):
    pass


if __name__ == '__main__':
    root = CTkCustom()
    root.title("helloworld")
    root.titlebar_title.configure(text="helloworld")

    root.mainloop()
