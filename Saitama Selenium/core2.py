#!/usr/bin/env python3.8
import sys
sys.path.insert(1, '/home/pi/scripts/usable_imports')
import fnctime
import time
import urllib.request
import subprocess
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
print('install ImageMagick')
print('Welcome "me" to this manga downloader.')
print('Write last part of link from kissmanga.com or the whole link.')
print()
print('In example:')
print('either this: Onepunch-Man-ONE')
print('or this: https://kissmanga.com/Manga/Onepunch-Man-ONE')

src = input('Write it here: ')

if src == '':
    src = 'Onepunch-Man-ONE'
    srcc = 'https://kissmanga.com/Manga/Onepunch-Man-ONE'
elif src[0:4] != 'http':
    srcc = 'https://kissmanga.com/Manga/' + src
else:
    srcc = src
    src = src.split('/')[-1]

print('source start')
# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome('chromedriver')
driver.get(srcc)
time.sleep(5)

source = driver.find_element_by_class_name('listing')
source = source.find_elements_by_tag_name('a')
source = [x.get_attribute('href') for x in source][::-1]

driver.close()
print('source end')


subprocess.Popen(f'rm -rf png_src/{src}', stderr=subprocess.PIPE, shell=True, text=True)
subprocess.Popen(f'rm -rf pdf_out/{src}', stderr=subprocess.PIPE, shell=True, text=True)
subprocess.Popen(['mkdir', 'png_src'], stderr=subprocess.PIPE, text=True)
subprocess.Popen(['mkdir', 'pdf_out'], stderr=subprocess.PIPE, text=True)
subprocess.Popen(f'mkdir png_src/{src}', shell=True, text=True)
subprocess.Popen(f'mkdir pdf_out/{src}', shell=True, text=True)

def core(source):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    if type(source) == str:
        source = [source]
        
    for z, site in enumerate(source):
        print(f' {x}/{z} start')
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
                time.sleep(0.5)
        else:
            table = driver.find_element_by_id('divImage')
            table = table.find_elements_by_tag_name('img')
            table = [x.get_attribute('src') for x in table]
        
        wind_title = driver.title[11:-23]
        wind_title = char_check(wind_title)
        
        subprocess.Popen(f'mkdir png_src/{src}/"{wind_title}"', stderr=subprocess.PIPE, shell=True, text=True)
        
        for y, phot in enumerate(table):
            l = 0
            while True:
                try:
                    f_nam = stat_len(y, 3, 1, '0')
                    urllib.request.urlretrieve(phot, f'png_src/{src}/{wind_title}/{f_nam}.png')
                except:
                    if l == 10:
                        print(src, wind_title)
                        raise Exception()
                    
                    print('   urllib exception: ' + Exception)
                    l += 1
                    time.sleep(0.5)
                finally:
                    time.sleep(0.5)
                    break
        
        print(f'  site end')
        
        print(f'  pdf start')
        p1 = subprocess.Popen(f'convert png_src/{src}/"{wind_title}"/* "pdf_out/{src}/{wind_title}.pdf"', stderr=subprocess.PIPE, shell=True, text=True)
        print(p1.communicate())
        p1.wait()
        print(f'  pdf end')
        print(f' {x}/{z} end')
    
    print('driver quit')
    driver.quit()

for x in range(10):
    print(f'core {x} start')
    core(source[x::10])
    print(f'core {x} end')
# core(source)

ttime.check()