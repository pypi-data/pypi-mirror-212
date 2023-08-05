import re
from ascvid.utils import html2curses as h2c

class SubError(ValueError):
    pass


NUM = re.compile(r"^\d+$")
TIME = re.compile(
    r"^(\d{2})\:(\d{2})\:(\d{2}\,\d{3}) \-\-\> (\d{2})\:(\d{2})\:(\d{2}\,\d{3})$"
)


def __corr(msg="unknown reason", filename="?", line="?"):
    raise SubError(f"{filename}:{line} => corrupted srt file: [{msg}]")


def calculate_timestamp(h, m, s):
    return h * 3600 + m * 60 + s


class SubEntry:
    def __init__(self, index, tstamp, contents):
        self.index = index
        self.stamp = tstamp
        self.contents = h2c.parse(contents)
        self.active = self.stamp.active

class Timestamp:
    def __init__(self, start, end):
        self.start_tup = start
        self.end_tup = end
        self.start_s = calculate_timestamp(*start)
        self.end_s = calculate_timestamp(*end)

    def active(self, time):
        return self.start_s <= time <= self.end_s


class SubParser:
    def __init__(self, stream):
        self.stream = stream
        self.line_counter = 0

    def readline(self):
        self.line_counter += 1
        return self.stream.readline()

    def _corr(self, msg):
        __corr(msg, self.stream.name, self.line_counter)
    def iter_subs(self):
        while True:
            first_line = self.readline()

            if not first_line:
                return
            first_line = first_line.strip()
            if NUM.match(first_line):
                index = int(first_line)
            else:
                self._corr("incorrect index line format: {first_line!r}")

            time_line = self.readline()
            if not time_line:
                self._corr("missing timestamp line")
            time_line = time_line.strip()
            if not TIME.match(time_line):
                self._corr(f"wrong timestamp line format: {time_line!r}")
            t_r = TIME.search(time_line).groups()
            h, m, s, *end = t_r
            s = s.replace(",", ".")
            h, m, s = int(h), int(m), float(s)
            eh, em, es = end
            es = es.replace(",", ".")
            eh, em, es = int(eh), int(em), float(es)
            cont_line = self.readline()
            if not cont_line:
                self._corr("missing content")

            content = cont_line
            while True:
                nline = self.readline()
                if not nline.strip():
                    break
                content+=nline
            timestamp = Timestamp((h, m, s), (eh, em, es))
            yield SubEntry(index, timestamp, content)


class Subtitles:
    def __init__(self, subtitle_file):
        self.file=subtitle_file
        with open(self.file) as fi:
            self.subs=list(SubParser(fi).iter_subs())
        self.current_sub_index=0
        self.max_lines=max([len(q.contents.splitlines()) for q in self.subs])

    def get_sub(self,t):
        if self.current_sub_index==len(self.subs):
            return ""
        sub=self.subs[self.current_sub_index]
        if sub.active(t):
            return sub.contents
        elif sub.stamp.end_s<=t:
            self.current_sub_index+=1
            return self.get_sub(t)
        return ""
