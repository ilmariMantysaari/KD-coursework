from tkinter import Tk
from tkinter.filedialog import askopenfilename


def main():
    filename = askopenfilename()
    print(filename)


main()