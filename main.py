from classes import *

def main() -> None:
    root=tk.Tk()
    mainwin=Window(root)
    mainwin.face()
    mainwin.inputs()
    mainwin.mainloop()

if __name__ == "__main__":
    main()