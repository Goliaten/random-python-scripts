import urllib.request
import subprocess
from random import randint
from requests import get
from threading import thread
from bs4 import BeautifulSoup

def stat_len(x, y=1, c=0, char=' '):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:          #adds ' ' to the end
        x += char
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = char + x
    return x

def downloader(src, name, x):
    for source, namae in zip(src, name):
        urllib.request.urlretrieve(source, f'png_src/{sauce}/{namae}')
        print(f'{x}, {sauce}:{namae} get')
        
    print(f'thread img {x} end')

def img_get(src, thr_id='?'):
    global s_table
    for site in src:
        while True:
            try:
                source = get(site).content
                soup = BeautifulSoup(source, 'lxml')
                
                nr = soup.find('span', class_='current').text
                n_table.append(stat_len(nr, 3, 1, '0') + '.jpg')
                
                phot = soup.find('img', class_='fit-horizontal')['src']
                s_table.append(phot)
                
                print(f'{thr_id}, {sauce}: {nr}')
            except:
                pass
            else:
                break
    
    print(f'thread {thr_id} end')
    

print('Welcome to the sauce downloader.')
print('  v1 ImageMagick')
print('Made by Goliaten(on reddit u/Fondist)')
print('It downloads chosen hentai doujinshi and converts it to pdf.')
print('After you enter the sauce, you will se bunch of control messages pop-up.')
print('Unless you see some exception, everything is fine.')
print()
print('Note: made on Linux, needs ImageMagick to convert correctly')
print()
sauce = input('Enter the sauce(leave empty to download random)')

if sauce == '':
    source = get('https://www.nhentai.net').content
    soup = BeautifulSoup(source, 'lxml')
    max_sauce = soup.find('div', class_='container index-container').div.a['href'][3:-1]
    sauce = randint(0, int(max_sauce))
    del max_sauce


n_table, s_table = [], []
print('source start')
source = get(f'https://www.nhentai.net/g/{sauce}').content
soup = BeautifulSoup(source, 'lxml')

if soup.find(id='container error'):
    print('sauce given does not exist')
    quit()

title = soup.find('div', id='info').h1.text
print('source end')

table = soup.find('div', id='thumbnail-container').find_all('a')
table = ['https://www.nhentai.net' + x['href'] for x in table]

subprocess.Popen(['mkdir', 'png_src'], stderr=subprocess.PIPE, text=True)
subprocess.Popen(['mkdir', 'pdf_out'], stderr=subprocess.PIPE, text=True)
subprocess.Popen(['mkdir', f'png_src/{sauce}'], stderr=subprocess.PIPE, text=True)
subprocess.Popen('rm png_src/*', stderr=subprocess.PIPE, shell=True, text=True)
subprocess.Popen('rm pdf_out/*', stderr=subprocess.PIPE, shell=True, text=True)

print('threads src start')
thr_times = 5          #6 sometimes throws up segmentation fault (like 5 but more often)(4 also does that, but more chaotically)

threads = {}
for x in range(thr_times):    #creating threads                                     #V V V splitting links equally for all of the threads
    threads[str(x)] = thread(target=img_get, name=f'Sauce src thr.{x}', args=([table[x::thr_times], x])) #<-- x == thread id

for thread in threads:
    threads[thread].start()
    
for thread in threads.values():
    try:
        thread.join()    #waiting for each thread to finish
    except:
        pass
print('threads src end')

print('threads img start')
threads = {}
for x in range(thr_times):    #creating threads                                     #V V V splitting links equally for all of the threads
    threads[str(x)] = thread(target=downloader, name=f'Sauce down thr.{x}', args=([s_table[x::thr_times], n_table[x::thr_times], x])) #<-- x == thread id

for thread in threads:
    threads[thread].start()

for thread in threads.values():
    try:
        thread.join()    #waiting for each thread to finish
    except:
        pass
    
print('pdf start')



p1 = subprocess.Popen(['convert', f'png_src/{sauce}/*', f'pdf_out/{sauce} {title}.pdf'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
p1.wait()
print(p1.communicate())
print('pdf end')
