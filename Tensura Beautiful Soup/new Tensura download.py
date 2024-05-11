#improvment from 1h 40min to 1h 10 min with new version
#with 2 threads this goes down to 36 min
#with 4 down to 16 min (if i remember correctly)
#with 5 down to 13 min 40 s
#with 6 down to 13 min (segmentation faults occur)

#handling segmentation fault
# import faulthandler
# faulthandler.enable()
# PYTHONFAULTHANDLER = 1

import cfscrape
import threading
import subprocess
from fnctime import time_check
from bs4 import BeautifulSoup

#----------------------------creating scraper------------------------
print('scrap s')
scrap = cfscrape.create_scraper()
source = scrap.get('https://www.readlightnovel.org/tensei-shitara-slime-datta-ken-wn', headers={"User-Agent": "XZ"}).content
print('scrap e')

soup = BeautifulSoup(source, 'lxml')

#---------------------char table-----------------------------
                        #   V    VnbspV would you believe? there are more than 1 type of spaces. one is 160(noble space), other 32 in hex, another 12288
chars = ['\t', '\n', '\r', ' ', ' ', '　', '‌', '', '「', '“', '」', '”', '『', '』'] #                                                VVV--these are not the same markers
for x in '''QWERTYUIOŌPASDFGHJKLZXCVBNMqweêértyuūiïíoōpaāàsdfghjklzxcçvbnm-_=≠≒+,＜<《〈≪.≫〉》>＞{[]};:：'̍"/?？、`‘’~～1234567890!！‼@#$%^&*＊※（()）\|…〜–—―−ー・●◇◆•→°。✦✧''':
    chars.append(x)

#-----------------------getting more links from main site------------------------------------
print('link s')
links, link = [], []
table = soup.find_all('ul', class_='chapter-chs')[:4]
for x in table:
    x = x.find_all('a')
    links += x
    
for x in links:
    link += [x['href']]
print('link e')

#--------------------core------------------------------
def core(links, thr_id='?'):
    ttime = time_check()
    for num, link in enumerate(links):
        
        #--------------------------request--------------------------------
        source = scrap.get(link, headers={"User-Agent": "XZ"}).content
        soup = BeautifulSoup(source, 'lxml')
        
        
        #---------------------some deleting of useless data---------------------------
        for trin in soup.find_all('div', class_='trinity-player-iframe-wrapper'):
            trin.replace_with('')
        for scr in soup.find_all('script'):
            scr.replace_with('')
        for scr in soup.find_all('text-center add11'):
            scr.replace_with('')
        for scr in soup.find_all('text-center'):
            scr.replace_with('')
        for div in soup.find_all('div', 'hidden'):
            div.replace_with('')
        
        #----------getting title for chapter---------------------------
        try:
            title = soup.find('div', class_='block-title').h1.text
        except:
            try:
                title = f'v6 Tensei Shitara Slime Datta Ken (WN) - Chapter {num.name}'
            except:
                title = f'v6 Tensei Shitara Slime Datta Ken (WN) - Chapter {num}'
        
        #-------------------getting wanted part of the site--------------------
        desc = soup.find('div', class_='desc').text
        
        #----------------new line/dialogue breaker------------------------------
        beg_list, end_list, tetr, out = ['「', '(', '（' '<', '“', '＜', '《', '≪', '['], ['」', ')', '）', '>', '”', '》', '≫', ']', '“'], '   ', ''
        dialog = 0 
        
        #it is based on cart/sight/focus basically there is this tetr variable.
        #At the beginning it changes its focus from lets say characters 21,22,23 to 22,23,24, and at the end addes first one to the output(in this case it would add 22).

        #thats only if nothing would be changed.
        #But each time newest letter (24 for this example) is added, it goes through a scanner.
        
        #Some(all) of them manually alter the focus, so that new letters can be added(mostly \n).
        for x in desc:
            tetr = tetr[1:] + x
                        
            if tetr in [' . ', ' . ', '　.　'] and dialog == 0:     #line end after dot v1
                tetr = ' \n '
                out += '.'
            
            elif tetr[1:] in ['. ', '. ', '.　'] and dialog == 0:   #line end after dot v2
                out += tetr[0]
                tetr = tetr[0] + '.\n'
            
            elif x in beg_list and dialog == 0:     #beginning of dialog/thought or something similar
                dialog = 1
                out += tetr[0:2]
                tetr = tetr[2] + '\n' + x
                
            elif x in end_list:                           #end of above
                dialog = 0
                out += tetr[0:2]
                tetr = tetr[2] + x + '\n'
            
            elif x in ['!', '！', '?'] and dialog == 0:        #breaker for ! and ?
                out += tetr[0:2]
                tetr = tetr[1] + x + '\n'
            
            else:                                       #for all other letters
                out += tetr[0]
                
        desc = out
        del out, beg_list, end_list, tetr, dialog
        
        #------------------character changer------------------------
        out, tetr = '', '   '
        for x in desc:
            tetr = tetr[1:] + x
            
            
            if tetr[0] not in chars:
                out += '\\'
                continue
            
            if tetr[0] in ['△'] :
                out += '$'
                
            elif tetr[0] in ['？']:
                out += '?'
                
            elif tetr[0] in ['！']:
                out += '!'
                
            elif tetr[0] in ['‼']:
                out += '!!'
                
            elif tetr[0] in ['：']:
                out += ':'
                
            elif tetr[0] in ['’', '‘', '̍'] :
                out += "'"
                
            elif tetr[0] in ['「'] :
                out += '['
                
            elif tetr[0] in ['」'] :
                out += ']'
                
            elif tetr[0] in ['＞', '〉'] :
                out += '>'
                
            elif tetr[0] in ['＜', '〈']:
                out += '<'
                
            elif tetr[0] in ['（']:
                out += '('
                
            elif tetr[0] in ['）']:
                out += ')'
                
            elif tetr[0] in ['“', '”']:
                out += '"'
                
            elif tetr[0] in ['＊']:
                out += '*'
                
            elif tetr[0] in ['※']:
                out += '--'
                
            elif tetr[0] in ['…']:
                out += '...'
                
            elif tetr[0] in ['≠', '≒']:
                out += '=/='
            
            elif tetr[0] in ['～']:
                out += '~'
                
            elif tetr[0] in ['『', '“', '《', '≪', '〈'] :
                out += '<<'
                
            elif tetr[0] in ['』', '”', '》', '≫', '〉'] :
                out += '>>'
                
            elif tetr[0] in ['–', '—', 'ー', '・', '−', '―', '〜', '、'] :
                out += '-'
                
            elif tetr[0] in ['→'] :
                out += '->'
                
            elif tetr[0] in [' ', '　', '‌']:
                out += ' '
                
            elif tetr[0] in ['\t']:
                out += '    '
                
            elif tetr[0] in ['é']:
                out += 'e'
                
            elif tetr[0] in ['ū']:
                out += 'uu'
                
            elif tetr[0] in ['Ō']:
                out += 'Oo'
                
            elif tetr[0] in ['ō']:
                out += 'oo'
                
            elif tetr[0] in ['ā']:
                out += 'aa'
                
            elif tetr[0] in ['ï', 'í']:
                out += 'i'
            
            elif tetr[0] in ['ê', 'é']:
                out += 'e'
                
            elif tetr[0] in ['à']:
                out += 'a'
                
            elif tetr[0] in ['ç']:
                out += 'c'
                
            elif tetr[0] in ['✦', '✧', '●', '。', '•', '◇', '◆']:
                out += '*'
                
            elif tetr[0] in ['°']:
                out += ' degrees '
            
            else:
                out += tetr[0]
             
        desc = out
        del out, tetr
        
        #--------------------nice line break---------------------------------
        line, f_list = '', []
        for x in desc:            #converting long text into list of shorter strings
            if x == '\n':
                f_list.append(line)
                line = ''
            line += x
        
        for y, line in enumerate(f_list):
            if len(line) > 91:
                for z in range(91, -1, -1):
                    v = line[z]
                    if v in [' ', ' ']:              #looking for closest space from the (length) character to first
                        sep = z    #+1          #separator
                        break
                else:                       #or taking the (width) bit
                    sep = 90
                    
                if sep == 0:
                    sep = 1
                    
                part1 = line[:sep]   #separating line
                part2 = line[sep:]
                f_list[y] = part1 + '\n'      #and adding it to menu  (part1 to place on old line)
                f_list.insert(y+1, part2)                   #(part 2 to next line)
        
        out = ''
        for line in f_list:
            out += line
            
        desc = out
        del out, sep, part1, part2, f_list, line
        
        #-------------title adder------------------
        desc = title + '\n' + desc
        
        #----------------file creator------------------------
        file = f'v7 {title}'
        with open(f'v7/{file}.txt', 'w') as file:
            file.write(desc)
        file = f'v7 {title}'
        
        #----------------------------ps creeation--------------------------
        n_file_ps = f'{file}.ps'
        proc = subprocess.Popen(['enscript', '-p', f'psv7/{n_file_ps}', f'v7/{file}.txt', f'--header={file}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.wait()
        
        #---------------------------pdf creation----------------------------------
        n_file_pdf = f'{file}.pdf'
        proc = subprocess.Popen(['ps2pdf', f'psv7/{n_file_ps}', f'pdfv7/{n_file_pdf}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.wait()
        
        print(thr_id, n_file_pdf, 'done')
        
    ttime.check()

#-----------------------------folders--------------------------------
try:       #deleing existing files
    proc = subprocess.Popen('cd pdfv7 && rm v7*', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    proc = subprocess.Popen('cd psv7 && rm v7*', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    proc = subprocess.Popen('cd v7 && rm v7*', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
except:
    pass

for fold in ['psv7', 'pdfv7', 'v7']:
    try:    #creating new folders
        proc = subprocess.Popen(['mkdir', fold], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except:
        pass
    proc.wait()

#---------------------threads creation------------------------------------------
#for fixing segmentation error i used terminal command(8192 default) "ulimit -s 16284" <---no, i changed it back
thr_times = 5          #6 sometimes throws up segmentation fault (like 5 but more often)(4 also does that, but more chaotically)

threads = {}
for x in range(thr_times):    #creating threads                                     #V V V splitting links equally for all of the threads
    threads[str(x)] = threading.Thread(target=core, name=f'Tensura thr.{x}', args=([link[x::thr_times], x])) #<-- x == thread id

for thread in threads:
    threads[thread].start()


# core([link[80]])
