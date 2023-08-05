from . import srt
from ascvid.logger import print_error
import os

SUB_EXTENSIONS = {".srt":srt}

def Subtitles(t):
    _,f = os.path.splitext(t)
    if f not in SUB_EXTENSIONS:
        print_error(f"Invalid subtitle extension. Implemented extensions: {list(SUB_EXTENSIONS.keys())}. Current extension: {f}")
        exit(1)
    subt_class=SUB_EXTENSIONS[f].Subtitles
    return subt_class(t)  
