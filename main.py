import tkinter as tk
from deepseekui import FormulaConverterApp
import os


def main():
    root = tk.Tk()

    # 设置DPI感知
    if os.name == 'nt':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

    root.tk.call('tk', 'scaling', 2.0)

    app = FormulaConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
