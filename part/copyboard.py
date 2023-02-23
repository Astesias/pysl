# -*- coding: utf-8 -*-
# @Time : 2020/3/16 21:26
# @File : get_text_from_cupboard_13.py
# @Author: Hero Liu
# python读取剪切板内容
import win32clipboard as w
import win32con


def get_text():
  w.OpenClipboard()
  d = w.GetClipboardData(win32con.CF_TEXT)
  w.CloseClipboard()
  return d.decode('GBK')


def set_text(aString):
  w.OpenClipboard()
  w.EmptyClipboard()
  w.SetClipboardData(win32con.CF_TEXT, aString)
  w.CloseClipboard()


try:
    
    set_text('iuyu'.encode('ascii'))
    ss = get_text()
    print(ss.replace('\x00',''))
finally:
    import sys
    sys.exit()