import os, re, sys
import cv2
from datetime import datetime

sys.path.insert(0, '../src/modules')

import book_recognizer

books = []
resArr = []
desTpl = []

for i in os.listdir('books/'):
    books.append(os.path.join("books/", i))

l = len(books)
for i in range(l):
    resArr.append(0)

#Список с ключевыми точками шаблонов
det = cv2.ORB_create()
for t in books:
    tpl = cv2.imread(t)
    tplGray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    _, tmp = det.detectAndCompute(tplGray, None)
    desTpl.append(tmp)

recognizer = book_recognizer.Recognizer()
recognizer.create("ORB")

video = cv2.VideoCapture('video_sample.mp4')
ret, frame = video.read()
ym, xm, _ = frame.shape

# Цикл по кадрам
while (ret):
    cropFrame = frame[ym//2 - 170 : ym//2 + 170,
                      xm//2 - 120 : xm//2 + 120]
    returned = recognizer.recognize(cropFrame, desTpl, 0.7)
    for i in range(l):
        resArr[i] = resArr[i] + returned[i]
    if max(resArr) > 400:
        break
    ret, frame = video.read()

print(books[resArr.index(max(resArr))])