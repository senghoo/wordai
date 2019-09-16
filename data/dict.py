# -*- coding: utf-8 -*-
import string
import re

class Description(object):
    def __init__(self, des):
        self.des = des
        self.idx = 0
        self.length = len(des)
        self.info = []
        if not self.read_seq():
            self.seq = 0
            self.en = self.des[self.idx:]
            self.cn = self.des[self.idx:]
            self.speech = 'OTHER'
            return

        if not self.read_word_speech():
            self.en = self.des[self.idx:]
            self.cn = self.des[self.idx:]
            self.speech = 'OTHER'
            return
        if not self.read_cn_and_en():
            self.en = self.des[self.idx:]
            self.cn = self.des[self.idx:]
            return
        self.read_info()

    def read_seq(self):
        res = ''
        while(self.idx < self.length):
            if self.des[self.idx] <= '9' and self.des[self.idx] >= '0':
                res += self.des[self.idx]
                self.idx += 1
            else:
                break
        if self.des[self.idx] == '.':
            self.idx += 1
        if len(res) > 0:
            self.seq = int(res.strip())
            return True
        return False

    def read_word_speech(self):
        res = ''
        while(self.idx < self.length):
            if self.des[self.idx] in string.ascii_uppercase+"- ;":
                res += self.des[self.idx]
                self.idx += 1
            else:
                break
        res = res.strip()
        if self.des[self.idx] == '\t':
            self.idx += 1
        if len(res) > 0:
            self.speech = res
            return True
        return False


    def read_cn_and_en(self):
        end = self.des.find('【', self.idx)
        if end == -1:
            end = len(self.des)
        idx = end
        while(idx >= self.idx):
            idx -= 1
            if self.des[idx] not in string.printable:
                break
        if idx == self.idx:
            self.cn = ''
            self.en = self.des[idx:end]
        elif idx == end-1:
            self.cn = self.des[idx:end]
            self.en = self.des[idx:end]
        else:
            self.cn = self.des[self.idx:idx+1]
            self.en = self.des[idx+1:end]
        self.idx = end
        return True

    def read_info(self):
        text = self.des[self.idx:]
        res = re.findall(r'【([^【】]+)】：([^【】]+)', text, re.M)
        for item in res:
            self.info.append({
                'name': item[0],
                'value': item[1],
            })
