# coding=utf-8

import os
import markdown


def md2html(md_str):
    html = """
    <html lang="zh-cn">

    <head>
    <meta charset="UTF-8">
    <meta name="author" content="lmintlcx">
    <meta name="description" content="植物大战僵尸脚本框架">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PvZ Scripts</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="stylesheet" href="normalize.css">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="styles/github.css">
    </head>

    <body>
    %s
    <script src="script.js"></script>
    <script src="highlight.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    </body>

    </html>
    """
    return html % markdown.markdown(md_str, extensions=["markdown.extensions.extra"])


SRC = os.path.join(os.getcwd(), "..", "html", "index.md")
DST = os.path.join(os.getcwd(), "..", "html", "index.html")

src_file = open(SRC, "r", encoding="utf-8")
md = src_file.read()
src_file.close()

os.remove(DST)
dst_file = open(DST, "a", encoding="utf-8")
dst_file.write(md2html(md))
dst_file.close()
