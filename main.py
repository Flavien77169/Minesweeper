import tkinter as tk
from menu import MenuWindow


def main():
    # Create and start the main application window
    root = tk.Tk()
    root.title("Minesweeper")
    MenuWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()