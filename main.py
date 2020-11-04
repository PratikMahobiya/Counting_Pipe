import os
from gui import gui

# initialize output folder------------------------------------------------
CWD = os.getcwd()
if not os.path.isdir("output"):
	os.mkdir("output")
Path_to_img = os.path.join(CWD, "output")

# Calling Gui---------------------------------------------------------------
window = gui.Window(Path_to_img)
window.win.mainloop()