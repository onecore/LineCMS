

class LoadThemeSettings:
    current = None

    def __init__(self, current_theme):
        self.theme = current_theme

    def printx(self):
        print(self.theme)


class boy(LoadThemeSettings):
    pass


v = LoadThemeSettings("asdasdasd")
y = boy("asdasd")
y.printx()
