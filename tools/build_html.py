# coding=utf-8

try:
    import markdown
except:
    import os

    os.system("pip install markdown")
    import markdown

import os


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
    <link rel="stylesheet" href="/css/normalize.css">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/styles/github.css">
    </head>

    <body>
    %s
    <script src="/js/script.js"></script>
    <script src="/js/highlight.pack.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    </body>

    </html>
    """
    return html % markdown.markdown(md_str, extensions=["markdown.extensions.extra"])


for m in ("endless", "pvz.py", "scripts", "docs"):

    SRC = os.path.join(os.getcwd(), "..", "html", m, "index.md")
    DST = os.path.join(os.getcwd(), "..", "html", m, "index.html")

    if not os.path.exists(SRC):
        exit(0)
    if os.path.exists(DST):
        os.remove(DST)

    src_file = open(SRC, "r", encoding="utf-8")
    md = src_file.read()
    src_file.close()

    dst_file = open(DST, "a", encoding="utf-8")
    dst_file.write(md2html(md))
    dst_file.close()
