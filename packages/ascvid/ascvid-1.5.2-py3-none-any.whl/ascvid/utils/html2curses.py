try:
    from bs4 import BeautifulSoup as bs
except:
    bs=None
MARKUP = {"b" : ("\x1b[1m","\x1b[22m"),"i": ("\x1b[3m","\x1b[23m"),"u":("\x1b[4m","\x1b[24m"),"s":("\x1b[9m","\x1b[29m"),"em":("\x1b[7m","\x1b[27m")}
ALIAS = {"strong":"b"}
def get_ansi(q):
    if q in ALIAS:
        q=ALIAS[q]
    return MARKUP.get(q,("",""))
def parse(text):
    if bs is None:
        return text
    soup=bs(text,"html.parser")
    out = ""
    for p in soup.contents:
        if isinstance(p,str):
            n=None
            t=p
        else:
            n=p.name
            t=parse(p.encode_contents())
        start,end=get_ansi(n)
        out+=start
        out+=t
        out+=end
    return out
        
