
print('Welcome to the sauce downloader.')
print('  v2 PIL & PyPDF2')
print('Made by Goliaten(on reddit u/Fondist).')
print('It downloads chosen hentai doujinshi from nhentai.net and converts it to pdf.')
print('Separate multiple sauces by space (" " if you are not sure)')
print('To disable the cleanup write !c')
print('If you want random sauce do not type in anything or type !rx where x is the number of random sauces.')
print(' You can not ask for random sauce and input a sauce at the same time.')
print('The syntax: [!c] [!rx] [sauce/sauce sauce ... sauce]')
print('After you enter the sauce, you will see bunch of control messages pop-up.')
print(' Unless you see some exception, everything is fine.')
print()
print('Notes:')
print('  -made on Linux')
print('  -needed modules: Pillow, pypdf2, requests, bs4')
print('  -needed parser: lxml')
print('  -on Linux you may have to also install libjpeg-dev and zlib1g')
print("  -it's best to run this script from its location")
print()
sauces = input('Enter the sauce(leave empty to download random) ')

print('importing urllib.request', end=' . . . ')
import urllib.request
print('done')
print('importing subprocess', end=' . . . ')
import subprocess
print('done')
print('importing random', end=' . . . ')
from random import randint
print('done')
print('importing json', end=' . . . ')
from json import dumps
print('done')
print('importing requests', end=' . . . ')
from requests import get
print('done')
print('importing os', end=' . . . ')
from os import name as os_name
print('done')
print('importing time', end=' . . . ')
from time import time
print('done')
print('importing threading', end=' . . . ')
import threading
print('done')
print('importing PIL', end=' . . . ')
from PIL import Image
print('done')
print('importing PyPDF2', end=' . . . ')
from PyPDF2 import PdfFileMerger, PdfFileReader
print('done')
print('importing bs4', end=' . . . ')
from bs4 import BeautifulSoup
print('done')


class time_check():
    def __init__(self):      #starts time tracking
        self.start_t = time()
    def check(self):         #prints current time from start
        end_t = time()
        t = end_t - self.start_t
        
        t_sec = int(t % 60)
        t_min = int(((t - t_sec) / 60) % 60)
        t_hr = int(((((t - t % 60) / 60) - t_min) / 60) % 24)
        
        print(f'Operation took {t_hr} hours {t_min} minuts {t_sec} seconds.')

def stat_len(x, y=1, c=0, char=' '):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:          #adds ' ' to the end
        x += char
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = char + x
    return x

def downloader(src, name, x):
    y = -1
    for source, namae in zip(src, name):
        y += 1
        for _ in range(10):
            try:
                urllib.request.urlretrieve(source, f'png_src/{sauce}/{namae}')
            except:
                print(f'{sauce} urllib exception {name}')
            else:
                break
        else:
            print(f'{sauce}, {name}')
            urllib.request.urlretrieve(source, f'png_src/{sauce}/{namae}')
        print(f'{x}:{stat_len(y,3,1,"0")}, {sauce}: {namae} get')
        
    print(f'{sauce} thread img {x} end')

def img_get(src, thr_id='?'):
    global s_table
    for y, site in enumerate(src):
        while True:
            try:
                source = get(site).content
                soup = BeautifulSoup(source, 'lxml')
                
                nr = soup.find('span', class_='current').text
                ns_table.append(stat_len(nr, 3, 1, '0'))
                n_table.append(stat_len(nr, 3, 1, '0') + '.jpg')
                
                phot = soup.find('section', id='image-container')
                phot = phot.a.img['src']
#                 phot = soup.find('img', class_='fit-horizontal')['src']#Goliaten
                s_table.append(phot)
                
                print(f'{thr_id}:{stat_len(y,3,1,"0")}, {sauce}: {nr} href get')
            except Exception as e:
                print(f'{sauce} href {nr} exception {thr_id}:{stat_len(y,3,1,"0")}')
            else:
                break
    
    print(f'{sauce} thread {thr_id} end')


#-----------------------------cleanup disabler------------------------------------
no_clean = 0
if sauces[0:2] == '!c':
    no_clean = 1
    sauces = sauces[3:]
    
    print('Cleanup disabled')

#-----------------------------random sauce gen-------------------------------------
if sauces == '' or sauces[0:2] == '!r':
    times = 0
    
    for _ in range(10):
        try:
            source = get('https://www.nhentai.net').content
        except:
            pass
        else:
            break
    else:
        print(f'{sauce} random href exception')
        source = get('https://www.nhentai.net').content
    soup = BeautifulSoup(source, 'lxml')
    max_sauce = soup.find('div', class_='container index-container').div.a['href'][3:-1]
    
    if sauces[0:2] == '!r':
        times = int(sauces[2:])
        if times < 1:
            times = 1
    else:
        times = 1
    
    sauces = ''
    for x in range(times):
        while True:
            sauce = str(randint(0, int(max_sauce))) + ' '
            if sauce not in sauces:
                sauces += sauce
                break
    else:
        sauces = sauces[:-1]    #removing ' ' from the end
    
    del max_sauce, times, x

sauces = sauces.split(' ')

if os_name == 'posix':
    mkdir = 'mkdir'
    rmdir = 'rm -rf'#'rmdir'u/fondist
    rm = 'rm -rf'
    slash = '/'
else:
    mkdir = 'mkdir'
    rmdir = 'rmdir /S /Q'
    rm = 'del /P /Q'
    slash = '\\'



tc = time_check()
inv_sauce = []
no_sauce = []

with open('json_log.txt', 'w') as file:
    for sauce in sauces:
        n_table, ns_table, s_table = [], [], []
        thr_src_out, thr_img_out, thr_pdf_out = {}, {}, {}
        
        file.write(f'\n{sauce}')
        
        try:
            _ = int(sauce)
            del _
        except:
            print(f'Sauce {sauce} is not a valid number')
            inv_sauce.append(sauce)
            file.write('\n unvalid sauce')
            continue
        
        
        print(f'{sauce} source start')
        file.write('\n source start')
        
        #request threw exception about bad SSL decryption or something like that G-o-l-i-a-t-e-n
        for _ in range(10):
            try:
                source = get(f'https://www.nhentai.net/g/{sauce}').content
            except:
                print(f'{sauce} request error')
                continue
            else:
                break
        else:
            print(f'{sauce} main href exception')
            file.write('\n  main href exception')
            source = get(f'https://www.nhentai.net/g/{sauce}').content
            
        soup = BeautifulSoup(source, 'lxml')
            
        if soup.find(class_='container error'):
            print(f'Given sauce {sauce} does not exist')
            file.write('\n  does not exist')
            no_sauce.append(sauce)
            continue

        title = soup.find('div', id='info').h1.text
        
        n_title = ''
        for x in title:
            if x not in ['/', '\\', '?', '|', "'", '"']:
                n_title += x
        
        title = n_title
        
        print(f'{sauce} source end')
        #creating folders
        p1 = subprocess.Popen(f'{mkdir} png_src', stderr=subprocess.PIPE, shell=True, text=True)
        p1 = p1.communicate()
        file.write(f'\n  {p1}')
        print(p1)
        p1 = subprocess.Popen(f'{mkdir} pdf_out', stderr=subprocess.PIPE, shell=True, text=True)
        p1 = p1.communicate()
        file.write(f' {p1}')
        print(p1)
        p1 = subprocess.Popen(f'{mkdir} png_src{slash}{sauce}', stderr=subprocess.PIPE, shell=True, text=True)
        p1 = p1.communicate()
        file.write(f' {p1}')
        print(p1)
        p1 = subprocess.Popen(f'{mkdir} pdf_out{slash}{sauce}', stderr=subprocess.PIPE, shell=True, text=True)
        p1 = p1.communicate()
        file.write(f' {p1}')
        print(p1)
        if no_clean != 1:
            p1 = subprocess.Popen(f'{rm} -rf png_src{slash}{sauce}{slash}*', stderr=subprocess.PIPE, shell=True, text=True)
            p1 = p1.communicate()
            file.write(f' {p1}')
            print(p1)
            p1 = subprocess.Popen(f'{rm} -rf pdf_out{slash}{sauce}{slash}*', stderr=subprocess.PIPE, shell=True, text=True)
            p1 = p1.communicate()
            file.write(f' {p1}')
            print(p1)
        

        #getting links for images
        table = soup.find('div', id='thumbnail-container').find_all('a')
        table = ['https://www.nhentai.net' + x['href'] for x in table]
        file.write('\n  ' + dumps([x.split('/')[-2] for x in table]))


        print(f'{sauce} threads src start')
        file.write('\n threads src start')
        thr_times = 5          #6 sometimes throws up segmentation fault (like 5 but more often)(4 also does that, but more chaotically)

        threads = {}
        for x in range(thr_times):    #creating threads                                     #V V V splitting links equally for all of the threads
            threads[str(x)] = threading.Thread(target=img_get, name=f'Sauce src thr.{x}', args=([table[x::thr_times], x])) #<-- x == thread id
            
        for thread in threads:
            threads[thread].start()
            
        for thread in threads.values():
            try:
                thread.join()    #waiting for each thread to finish
            except:
                pass
        print(f'{sauce} threads src end')


        print(f'{sauce} threads img start')
        file.write('\n threads img start')
        #Fondist
        threads = {}
        for x in range(thr_times):    #creating threads                                     #V V V splitting links equally for all of the threads
            threads[str(x)] = threading.Thread(target=downloader, name=f'Sauce down thr.{x}', args=([s_table[x::thr_times], n_table[x::thr_times], x])) #<-- x == thread id

        for thread in threads:
            threads[thread].start()

        for thread in threads.values():
            try:
                thread.join()    #waiting for each thread to finish
            except:
                pass



        print(f'{sauce} pdf start')
        file.write('\n pdf start')
        
        file.write('\n  n_table=' + dumps(n_table))
        file.write('\n  ns_table=' + dumps(ns_table))
        
        for y, namae in enumerate(n_table):
            img = Image.open(f'png_src{slash}{sauce}{slash}{namae}')
            try:
                img = img.convert('RGB')
            except:
                pass
            img.save(f'pdf_out{slash}{sauce}{slash}{ns_table[y]}.pdf', save_all=True)
            print(f' {sauce} pdf create {namae}')

        print(f' {sauce} pdf merge start')
        file.write('\n  pdf merge start')
        ns_table.sort()
        
        file.write('\n   ns_table=' + dumps(ns_table))
        
        merger = PdfFileMerger()
        for name in ns_table:
            merger.append(PdfFileReader(f'pdf_out{slash}{sauce}{slash}{name}.pdf', 'rb'))
            
        merger.write(f'pdf_out{slash}{sauce} {title}.pdf')
        
        del merger
        print(f' {sauce} pdf merge end')
        file.write('\n  pdf merge end')
        file.write('\n   n_table=' + dumps(n_table))
        file.write('\n   ns_table=' + dumps(ns_table))
        print(f'{sauce} pdf end')


        if no_clean != 1:
            print(f'{sauce} clean up start')
            p1 = subprocess.Popen(f'{rmdir} png_src{slash}{sauce}', stdin=subprocess.PIPE, shell=True, text=True)
            print(p1.communicate())
            p1 = subprocess.Popen(f'{rmdir} pdf_out{slash}{sauce}', stdin=subprocess.PIPE, shell=True, text=True)
            print(p1.communicate())    
            print(f'{sauce} clean up end')


if no_clean != 1: 
    p1 = subprocess.Popen(f'{rmdir} png_src', stderr=subprocess.PIPE, shell=True, text=True)
    print(p1.communicate())
    print('Final cleanup')

if inv_sauce:
    print(f'Total number of invalid sauces: {len(inv_sauce)}')
    print(' '.join(inv_sauce))
if no_sauce:
    print(f'Total number of missing sauces: {len(no_sauce)}')
    print(' '.join(no_sauce))


tc.check()
