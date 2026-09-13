import re, sys

# Make the built page charset-independent:
#   markup outside <script>  -> numeric HTML entities
#   JS source inside <script> -> \uXXXX escapes (survive any decoding)
src = open("meridian-petroleum.html", encoding="utf-8").read()
i = src.index("<script>")
head, tail = src[:i], src[i:]


def js_escape(m):
    cp = ord(m.group(0))
    if cp > 0xFFFF:
        cp -= 0x10000
        return "\\u%04x\\u%04x" % (0xD800 + (cp >> 10), 0xDC00 + (cp & 0x3FF))
    return "\\u%04x" % cp


head = re.sub(r"[^\x00-\x7F]", lambda m: "&#%d;" % ord(m.group(0)), head)
tail = re.sub(r"[^\x00-\x7F]", js_escape, tail)
out = head + tail

assert out.isascii(), "non-ascii survived"
open("meridian-petroleum.html", "w", encoding="ascii").write(out)
print("ascii-safe: True   size %.2f MB" % (len(out.encode()) / 1024 / 1024))
