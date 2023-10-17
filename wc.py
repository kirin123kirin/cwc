# -*- coding: utf-8 -*-

# Install Require
# pip install mecab-python3
# pip install wordcloud
# pip install pyperclip

import os
import re
import sys
from os.path import join as pathjoin
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import pyperclip

try:
    import tkinter as tk
    from tkinter import messagebox

    def cerr(msg):
        tk.Tk().withdraw()
        messagebox.showinfo("エラーメッセージ", msg)
except (ModuleNotFoundError, ImportError):
    def cerr(msg):
        sys.stderr.write(msg)

font_path = "C:/Windows/Fonts/meiryo.ttc"


def build_wc(text, hinshi={"名詞"}, excludes=[], imgfile_path=pathjoin(os.environ.get('TMP'), "tmp_wordcloud.png")):
    t = Tokenizer()
    tokens = t.tokenize(text)
    words = ""

    if not hinshi:
        def hfilter(s):
            return True
    elif len(hinshi) == 1:
        hinshi = list(hinshi)[0]

        def hfilter(s):
            return hinshi in s
    else:
        def hfilter(L):
            return L.split(",")[0] in hinshi

    if excludes:
        for token in tokens:
            s = token.surface
            if hfilter(token.part_of_speech) and all(x not in s for x in excludes):
                words += " " + s
    else:
        for token in tokens:
            if hfilter(token.part_of_speech):
                words += " " + token.surface

    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='winter', font_path=font_path).generate(words)

    wordcloud.to_file(imgfile_path)
    os.startfile(imgfile_path)


def main():
    hinshi = {}
    excludes = []
    
    text = re.sub("\s", "", pyperclip.paste())
    if text:
        build_wc(text, hinshi, excludes)
    else:
        cerr("ワードクラウド化したい文章をコピーして再度実行してください。\n空白や改行のみ場合は")


def test():
    test_text = """インストールされている Tkinter のバージョンを確認するには、Python シェルから次を実行します。"""
    build_wc(test_text.replace("\r", "").replace("\n", ""))


if __name__ == "__main__":
    test()
    # main()
