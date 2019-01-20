import cx_Freeze
import sys
import os
executables = [cx_Freeze.Executable("T_Clone.pyw", base = "Win32GUI")]
os.environ['TCL_LIBRARY'] = "C:\\Users\\David Jones\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\David Jones\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tk8.6"
cx_Freeze.setup(
    name="Tetris Clone",
    version="1.0.0",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["View.pyw", "__init__.pyw","Cell.pyw","Shapes.pyw","Game.pyw"]}},
    executables = executables

    )
