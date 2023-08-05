from customtkinter import CTkFrame, ThemeManager, CTkLabel, CTkFont, CTkScrollableFrame, CTkButton
from customtkinterx import CTkCustom


class CTkMegaMenuBar(CTkFrame):
    def __init__(self, master=None, title: str = "Mega Menu", custom: CTkCustom = None, **kwargs):
        super().__init__(master, **kwargs)

        self.__custom = custom

        if self.__custom is not None:
            self.__label_title = CTkLabel(self.__custom.titlebar, text=title, anchor="w", font=CTkFont(weight="bold"))
            self.__label_title.pack(side="left", fill="y", padx=8, pady=5)
            self.__custom.bind_move(self.__label_title)

            self.__scrolledframe_menus = CTkScrollableFrame(self)
            self.__scrolledframe_menus.pack(fill="both", expand="yes", padx=5, pady=5)
        else:
            self.__label_title = CTkLabel(self, text=title, anchor="w", font=CTkFont(weight="bold"))
            self.__label_title.pack(side="top", fill="x", padx=8, pady=5)

            self.__scrolledframe_menus = CTkScrollableFrame(self)
            self.__scrolledframe_menus.pack(fill="both", expand="yes", padx=5, pady=5)

        self.__buttons = {}

    def show(self, **kwargs):
        self.pack(fill="y", side="left", padx=5, pady=5, ipadx=5, ipady=5)
        if self.__custom is not None:
            self.pack(padx=2, pady=0)
        self.pack_configure(**kwargs)

    def create_menu(self, text="Menu", id: str | int = -1, **kwargs):
        __button_menu = CTkButton(self.__scrolledframe_menus, width=30, text=text, anchor="w", **kwargs)
        __button_menu._fg_color = self._fg_color
        __button_menu._text_color = ThemeManager.theme["CTkLabel"]["text_color"]
        __button_menu.pack(fill="x", side="top", padx=0, pady=5, ipadx=5, ipady=5)
        __button_menu._draw()

        if id == -1:

            def generate_random_str(randomlength=16):
                import random
                """
                生成一个指定长度的随机字符串
                """
                random_str = ''
                base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
                length = len(base_str) - 1
                for i in range(randomlength):
                    random_str += base_str[random.randint(0, length)]
                return random_str

            id = generate_random_str(8)

        __button_menu.setvar("id", id)

        self.__buttons[id] = __button_menu

        return __button_menu

    @property
    def menus(self):
        return self.__buttons

    @property
    def title(self):
        return self.__label_title

    @property
    def menubar(self):
        return self.__scrolledframe_menus


if __name__ == '__main__':
    from customtkinterx import CTkCustom, CTkMinimalTheme, CTkFluentTheme

    CTkMinimalTheme()
    #CTkFluentTheme()

    root = CTkCustom(title="CTkMegaMenuBar")
    root.create_sizegrip()

    menubar = CTkMegaMenuBar(root.mainframe, custom=root)
    for menu in range(10):
        _menu = menubar.create_menu("Menu"+str(menu))
    menubar.show()

    root.mainloop()