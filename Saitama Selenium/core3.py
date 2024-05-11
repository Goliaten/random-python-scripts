#!/usr/bin/env python3.8
import sys
sys.path.insert(1, '/home/pi/scripts/usable_imports')
del sys
import fnctime
from time import sleep
from urllib.request import urlretrieve
from subprocess import Popen, PIPE
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader
from selenium import webdriver
# for chromedriver search for 'chromedriver armhf'
#https://launchpad.net/ubuntu/xenial/armhf/chromium-chromedriver
#https://chromedriver.storage.googleapis.com/index.html
def stat_len(x, y=1, c=0, char=' '):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:          #adds ' ' to the end
        x += char
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = char + x
    return x

def char_check(text):
    n_title = ''
    for x in text:
        if x not in ['/', '\\', '?', '|', "'", '"', '!']:
            n_title += x
    
    return n_title

ttime = fnctime.time_check()

print('Manga downloader')
print('Made by: Goliaten')
print('install by pip PIL,PyPDF2, selenium ')
print('Welcome "me" to this manga downloader.')
print()
print('Write last part of link from kissmanga.com or the whole link.')
print('In example:')
print('either this: Onepunch-Man-ONE')
print('or this: https://kissmanga.com/Manga/Onepunch-Man-ONE')
print()
print('To disable clean up, write at the beginning "!c "(mind the space)')
print('To start at certain index(the number at the left you see in command line)..')
print('.. write "!ind " where ind is a number')

src = input('Write it here: ')

if src == '':
    src = 'Onepunch-Man-ONE'
    srcc = 'https://kissmanga.com/Manga/Onepunch-Man-ONE'

start = 0
cln_flg = 0
if src[0] == '!c ':
    src = src[2:]
    cln_flg = 1   #cleaning flag
elif src[0] == '!':
    src = src.split(' ')
    start = src[0][1:]
    src = src[1]

if src[0:4] != 'http':
    srcc = 'https://kissmanga.com/Manga/' + src
else:
    srcc = src
    src = src.split('/')[-1]

print('source start')
# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome('chromedriver')
driver.get(srcc)

del srcc

sleep(5)
# input('Clickenter once you got through captcha')
# sleep(10)

while True:
    try:
        source = driver.find_element_by_class_name('listing')
        source = source.find_elements_by_tag_name('a')
        source = [x.get_attribute('href') for x in source][::-1]
    except:
        print('source exception')
        sleep(0.5)
        pass
    else:
        break

driver.close()
print('source end')

# p1 = Popen(f'rm -rf png_src/{src}', stderr=PIPE, shell=True, text=True)
# print(p1.communicate())
# p1 = Popen(f'rm -rf pdf_out/{src}', stderr=PIPE, shell=True, text=True)
# print(p1.communicate())
p1 = Popen('mkdir png_src && touch png_src/test', stderr=PIPE, shell=True, text=True)
print(p1.communicate())
p1 = Popen('mkdir pdf_out && touch pdf_out/test', stderr=PIPE, shell=True, text=True)
print(p1.communicate())
p1 = Popen(f'mkdir -v png_src/{src} && touch png_src/{src}/test', stdout=PIPE, stderr=PIPE, shell=True, text=True)
print(p1.communicate())
p1 = Popen(f'mkdir -v pdf_out/{src} && touch pdf_out/{src}/test', stdout=PIPE, stderr=PIPE, shell=True, text=True)
print(p1.communicate())
del p1

def core(source):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    if type(source) == str:
        source = [source]
        
    for z, site in enumerate(source):
        print(f' {z} start')
        print(f'  site start')
        
        print('   w8, site')
        driver.get(site)
        print('   w8 over')
        
        table = [None]
        while None in table:
            try:
                table = driver.find_element_by_id('divImage')
                table = table.find_elements_by_tag_name('img')
                table = [x.get_attribute('src') for x in table]
            except:
                print('   table exception')
            finally:
                sleep(1.5)
        else:
            table = driver.find_element_by_id('divImage')
            table = table.find_elements_by_tag_name('img')
            table = [x.get_attribute('src') for x in table]
        
        wind_title = driver.title[11:-23]
        wind_title = char_check(wind_title)
        
        p1 = Popen(f'mkdir -v png_src/{src}/"{wind_title}" && touch png_src/{src}/"{wind_title}"/test', stdout=PIPE, stderr=PIPE, shell=True, text=True)
        print(p1.communicate(), end='')
        p1 = Popen(f'mkdir -v pdf_out/{src}/"{wind_title}" && touch pdf_out/{src}/"{wind_title}"/test', stdout=PIPE, stderr=PIPE, shell=True, text=True)
        print(p1.communicate(), end='')
        del p1
        print(src, wind_title)
        
        print('   retrieve start')
        
        table = table[start:]
        n_table, ns_table = [], []
        for y, phot in enumerate(table):
#             print(f'f_nam={stat_len(y, 3, 1, "0")} {phot=} {y=} {wind_title=}')
#             input()
            l = 0
            while True:
                try:
                    f_nam = stat_len(y, 3, 1, '0')
                    ext = phot.split('.')[-1]
                    urlretrieve(phot, f'png_src/{src}/{wind_title}/{f_nam}.{ext}')
                    n_table.append(f'{f_nam}.{ext}')
                    ns_table.append(f_nam)
#                     print('   downloaded')
                except:
                    if l == 10:
                        print(src, wind_title)
                        raise Exception()
                    
                    print('   urllib exception: ' + str(Exception()))
                    l += 1
                    sleep(0.5)
                else:
#                     print('   else break')
                    sleep(0.5)
                    break
        del ext, f_nam, l, phot, y, table
        print('   retrieve end')
        
        print(f'   {z} pdf start')
#         print(n_table)
#         print(ns_table)
        
        p_table = []
        for y, namae in enumerate(n_table):
#             print(f'png_src/"{wind_title}"/{namae}')
            img = Image.open(f'png_src/{src}/{wind_title}/{namae}')
            try:
                img = img.convert('RGB')
            except:
                pass
            img.save(f'pdf_out/{src}/{wind_title}/{ns_table[y]}.pdf', save_all=True)
#             print(f'pdf_out/{src}/"{wind_title}"/{ns_table[y]}.pdf')
            print(f'    {z} pdf create {namae}')

        print(f'    {z} pdf merge start')
        ns_table.sort()
        
        del n_table, p_table, y, namae
        
        merger = PdfFileMerger()
        for name in ns_table:
            merger.append(PdfFileReader(f'pdf_out/{src}/{wind_title}/{name}.pdf', 'rb'))
            
        merger.write(f'pdf_out/{src}/{wind_title}.pdf')
        
        del merger, ns_table
        print(f'    {z} pdf merge end')
        
        if cln_flg == 0:
            print(f'    {z} clean up start')
            p1 = Popen(f'rm -r png_src/{src}/"{wind_title}"', shell=True, text=True)
            print(p1.communicate())
            Popen(f'rm -r pdf_out/{src}/"{wind_title}"', shell=True, text=True)
            print(p1.communicate())
            print(f'    {z} clean up end')
            
        print(f'   {z} pdf end')
        
        print(f'  site end')
    
    if cln_flg == 0:
        print(' final clean up start')
        Popen(f'rm -r png_src', shell=True, text=True)
        print(' final clean up end')
    
    print('driver quit')
    driver.quit()

# for x in range(10):
#     print(f'core {x} start')
#     core(source[x::10])
#     print(f'core {x} end')
core(source)

ttime.check()