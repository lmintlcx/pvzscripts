# coding=utf-8
# usage: md2html.py src_file dst_file

import os
import sys
import markdown


def md2html(md_str):
    html = """
<html lang="zh-cn">
<head>
<meta charset="UTF-8">
<title>PvZ Scripts</title>
<link rel="icon" href="/favicon.ico">
<link rel="stylesheet" href="/scripts/normalize.css">
<link rel="stylesheet" href="/scripts/style.css">
<link rel="stylesheet" href="/scripts/styles/github.css">
</head>
<body>
%s
<script src="/scripts/script.js"></script>
<script src="/scripts/highlight.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
</body>
</html>
"""

    exts = ["markdown.extensions.extra"]

    ret = markdown.markdown(md_str, extensions=exts)
    return html % ret


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit()

    src_file = open(sys.argv[1], "r", encoding="utf-8")
    md = src_file.read()
    src_file.close()

    if os.path.exists(sys.argv[2]):
        os.remove(sys.argv[2])

    dst_file = open(sys.argv[2], "a", encoding="utf-8")
    dst_file.write(md2html(md))
    dst_file.close()
