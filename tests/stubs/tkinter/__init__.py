import types,sys
class _Any:
    def __init__(self,*a,**k): pass
    def __getattr__(self,n): return _Any()
    def __call__(self,*a,**k): return _Any()
def __getattr__(n): return _Any
Frame=Tk=Toplevel=Canvas=Label=Button=Entry=Text=StringVar=IntVar=BooleanVar=DoubleVar=PhotoImage=Menu=Scrollbar=Listbox=Checkbutton=Radiobutton=Scale=Spinbox=Message=LabelFrame=PanedWindow=_Any
TclError=Exception
END="end"
for m in ("ttk","messagebox","simpledialog","filedialog","font"):
    mod=types.ModuleType("tkinter."+m); mod.__getattr__=lambda n:_Any; sys.modules["tkinter."+m]=mod; globals()[m]=mod
