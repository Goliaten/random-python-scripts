# import requests
from bs4 import BeautifulSoup
import subprocess
import fnctime
import cfscrape

def katakana_conv(inp):
    if inp in katakana:
        outp, contrl = katakana_out[katakana.index(inp)], 0
    elif inp in chiisai:
        outp, contrl = chiisai[chiisai.index(inp)], 1
    elif inp == 'ッ':
        outp, contrl = '', 2
    return outp, contrl

katakana = ['ア','カ','サ','タ','ナ','ハ','マ','ヤ','ラ','ワ',
            'イ','キ','シ','チ','ニ','ヒ','ミ','リ','ヰ',
            'ウ','ク','ス','ツ','ヌ','フ','ム','ユ','ル',
            'エ','ケ','セ','テ','ネ','ヘ','メ','レ','ヱ',
            'オ','コ','ソ','ト','ノ','ホ','モ','ヨ','ロ','ヲ',
            'ン',
            'ガ','ギ','グ','ゲ','ゴ',
            'ザ','ジ','ズ','ゼ','ゾ',
            'ダ','ヂ','ヅ','デ','ド',
            'バ','ビ','ブ','ベ','ボ',
            'パ','ピ','プ','ペ','ポ']
chiisai = ['ャ','ュ','ョ']
katakana_out = ['a','ka','sa','ta','na','ha','ma','ya','ra','wa',
               'i','ki','shi','chi','ni','hi','mi','ri','wi',
               'u','ku','su','tsu','nu','fu','mu','yo','ru',
               'e','ke','se','te','ne','he','me','re','we',
               'o','ko','so','to','no','ho','mo','yo','ro','wa',
               'n',
               'ga','gi','gu','ge','go',
               'za','ji','zu','ze','zo',
               'da','ji','zu','de','do',
               'ba','bi','bu','be','bo',
               'pa','pi','pu','pe','po']
conv = [x for x in katakana] + [x for x in chiisai] + ['ッ']

x = input('to pdf? ')
# if x == 'html':
#     p = 5
if x == 'v6':
    p = 4
elif x == 'v5':
    p = 3
elif x == 'v4':
    p = 2
elif x == 'v3':
    p = 1
elif x == 'v2':
    p = 0
else:
    p = -1

print('p', p)

time = fnctime.time_check()
#---------------creating folder---------------------
try:
    proc = subprocess.Popen(['mkdir', f'v{p+2}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
except:
    pass
finally:
    proc = subprocess.Popen(f'cd v{p+2} && rm v{p+2}* && touch control.txt', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)


links = []
link = []
filenames = []
#---------------allowed characters-----------------------
chars = ['\n', '\r', ' ', '', '「', '“', '」', '”', '『', '』'] #         VV VV these are not the same markers
for x in '''QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm-_=+,＜<《≪.≫》>＞[{]};:'"/?`‘’~1234567890!！@#$%^&*＊()\|…–−ー・→''':
    chars.append(x)
if p == 3:
    for x in 'アカサタナハマヤラワイキシチニヒミリヰウクスツヌフムユルエケセテネヘメレヱオコソトノホモヨロヲガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペッャュョ':
        chars.append(x)
#-----------------------------getting site--------------------------------
#----------with cloudflare---------------------
if p >= 4:
    print('scrape c begin')
    scraper = cfscrape.create_scraper(delay=6)
    print('scrape c end')
    print('scrape begin')
    source = scraper.get('https://www.readlightnovel.org/tensei-shitara-slime-datta-ken-wn', headers={"User-Agent": "XZ"}).content
    print('scrape end')
# print(source)
# input()
# print('scrape p end')

#----------without cloudflare-----------------
else:
    print('req')
    source = requests.get('https://www.readlightnovel.org/tensei-shitara-slime-datta-ken-wn', headers={"User-Agent": "XZ"}).content
#     source = requests.get('https://www.readlightnovel.org/tensei-shitara-slime-datta-ken-wn', headers={"User-Agent": "XZ"}).text
    print('req get')
    
#-------creating soup---------------------
soup = BeautifulSoup(source, 'lxml')
# with open('site.txt', 'w') as file:
#     file.write(soup.text)
# input()

# print(soup.prettify)

table = soup.find_all('ul', class_='chapter-chs')[:4]
for x in table:
    x = x.find_all('a')
    links += x
    
for x in links:
    link += [x['href']]

del x, soup, source, table, links
#----------------------------
print('conversion')

for num, x in enumerate(link):
    #----------getting source for site-----------------
    if p >= 4:
        source = scraper.get(x, headers={"User-Agent": "XY"}).text #with cloudflare
    else:
        source = requests.get(x, headers={"User-Agent": "XY"}).text #without cloudflare
    #--------------creating soup---------------
    soup = BeautifulSoup(source, 'lxml')
#     print(soup.prettify)
#     input()
#     #----------------------output only html file--------------------------------------------------------
#     if p == 5:
#         try:
#             proc = sunprocess.Popen('cd html && rm html_*', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
#         except:
#             pass
#         
#         try:
#             proc = subprocess.Popen(['mkdir', 'html'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         except:
#             pass
#         
#         with open(f'''html/html_{f"{soup.find('div', class_='block-title').h1.text}"}''', 'w') as file:
#             file.write(soup.text)
#         continue
    
    #---------------deleting useless data-------------------
 #     for br in soup.find_all('br'):
 #         br.replace_with('\n')
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
        
    #--------------getting title for a chapter--------------
    try:
        title = soup.find('div', class_='block-title').h1.text
    except:
        title = f'v6 Tensei Shitara Slime Datta Ken (WN) - Chapter {num}'
#     print('title')
    
    #------------------getting text-------------------------
    desc_2 = soup.find('div', class_='desc').text
    
    #--------------breaking lines------------------------
    #-----------V V V markers to new line+-----------------------
    beg_lis, end_lis, tetr, out, dialog, buffer = ['「', '(', '[', '<', '“', '＜', '《', '≪'], ['」', ')', ']', '>', '”', '》', '≫'], '   ', '', 0, 0
    for x in desc_2:
        tetr = tetr[1:]
        tetr += x
        
#         print(out)
        
        if x in beg_lis and dialog == 0:
            out += '\n' + x
            dialog = 1
        elif x in end_lis:
            out += x + '\n'
            dialog = 0
            
#         elif x == '＜' and buffer == 1:  #for great sage dialog
#             out += x
#             buffer == 0
#         elif x == '＜' and buffer == 0:  #for great sage dialog
#             out += '\n' + x
#             buffer = 1
            
        elif x == '＞' and buffer == 1:  #for great sage dialog
            out += x + '\n'
            buffer == 0
        elif x == '＞' and buffer == 0:  #for great sage dialog
            out += x
            buffer = 1
        
        elif x in ['.', '!', '?'] and dialog == 0:
            out += f'{x}\n'
        elif tetr == ' . ' and dialog == 0:
            out = out[:-2] + '.\n'
        elif tetr[1:3] == '. ' and dialog == 0:
            out += '\n'
        else:
            out += x
            
#         if len(out)%10==0:
#             print(out)
#             input()

#     print(out)
#     input()
    desc_2_out = out
    
    #-------' . ' to new line---character changer for pdf creation--controls allowed characters---------
    old_out, out, char, sample, buffer = out, '', ' ', '   ', 0
    temp_sample = sample
    for char in old_out:
#         if sample == 'rds':
#             print(out)
#             print('pass')
        
        if char == '':
            break
        
        if p >= 1:
            if char == '△':          ##
                char = '$'           ##
            elif char in ['’', '‘']:   ##
                char = "'"           ##
            elif char == '「':   ##
                char = "["            ##
            elif char == '」':
                char = ']'
            elif char in ['＞', '〉']:
                char = '>'
            elif char in ['＜', '〈']:
                char = '<'
            elif char in ['“', '”']:   ##
                char = '"'           ##
            elif char in ['＊']:
                char = '*'

        if char not in chars and p >= 1:
#             print(char, chars)
            continue
            
        if buffer > 0:
            buffer -= 1
            sample = sample[1:] + char
            continue
        temp_sample = sample[1:] + char
        

#         print('Outputting')
        if sample[0] == '…' and p >= 1:     ##
            out += '...'                    ##
        elif sample[0] in ['〉', '『', '“', '《', '≪'] and p >= 1:
            out += '<<'
        elif sample[0] in ['〈', '』', '”', '》', '≫'] and p >= 1:
            out += '>>'
        elif sample[0] in ['?']:
            out += '? '
        elif sample[0] in ['!', '！']:
            out += '! '
        elif sample[0] in ['.']:
            out += '. '
        elif sample[0] in ['–', 'ー', '・', '−']:
            out += '-'
        elif sample[0] in ['→']:
            out += '->'
        elif temp_sample == ' . ':
            out += sample[0] + '.'
            buffer = 3
#         elif temp_sample[:2] == '. ':
#             out += '. '
#             buffer = 2
        elif char == '':
            out += sample
        else:
            out += sample[0]
        
#         if len(out)%10==0:
#             print(out)
#             input()
        sample = temp_sample

    #------for converting katakana into latin--------------
    if p >= 3:
        n_out = ''
        chiis = 0
        for y, x in enumerate(out):
            if x in conv:
                v, z = katakana_conv(x)
                if z == 0:
                    if chiis == 1:
                        n_out += v[:1] + v
                        chiis = 0
                    else:
                        n_out += v
                elif z == 1:
                    n_out = n_out[:-1] + v
                elif z == 2:
                    chiis = 1
            else:
                n_out += x
        out = n_out
    
    

    #----line breaking to fit nicely in pdf page
    if p >= 1:
        line = ''         ##
        f_list = []
        for x in out:
            if x == '\n':
                f_list.append(line)
                line = ''
            line += x
        
        y = -1
        for line in f_list:
#             print('f_list', line)
            y += 1
            if len(line) > 91:
                for z in range(91, -1, -1):
                    v = line[z]
                    if v == ' ':              #looking for closest space from the (length) character to first
                        sep = z    #+1          #separator
                        break
                else:                       #or taking the (width) bit
                    sep = 91
                part1 = line[:sep]   #separating line
                part2 = line[sep:]
                f_list[y] = part1 + '\n'      #and adding it to menu  (part1 to place on old line)
                f_list.insert(y+1, part2)                   #(part 2 to next line)
        
        out = ''
        for line in f_list:
            out += line
    #---------writing to files----------------
    if p == -1:
        with open('v1/v1 ' + title + '.txt', 'w') as file:
            file.write(title + '\n')
            for line in desc_1_out:
                file.write(line.text + '\n')
            
    elif p == 0:
        with open('v2/v2 ' + title + '.txt', 'w') as file:
            file.write(title + '\n')
            file.write(desc_2_out)

    elif p >= 1:
        with open(f'v{p+2}/v{p+2} ' + title + '.txt', 'w') as file:
            file.write(title + '\n')
            file.write(out)
            filenames.append(f'v{p+2} {title}.txt')
    print(title)


if p == 1:
    del proc, out, part1, part2, link,  old_out, sample, scr, sep, soup, source, temp_sample, tetr, title, v, x, y, z, char, buffer, f_list, div, dialog, desc_2

# sudo apt-get install enscript ghostscript
print('pdf')
if p >= 1 and p != 5:
    try:
        proc = subprocess.Popen(f'cd pdfv{p+2} && rm v{p+2}*', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        proc = subprocess.Popen(f'cd psv{p+2} && rm v{p+2}*', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    except:
        pass

    for fold in [f'psv{p+2}', f'pdfv{p+2}']:
        try:
            proc = subprocess.Popen(['mkdir', fold], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except:
            pass
        proc.wait()

    for file in filenames:
        print(file)
        n_file_ps = file[:-3] + '.ps'
        n_file_pdf = file[:-3] + '.pdf'

        proc = subprocess.Popen(['enscript', '-p', f'psv{p+2}/{n_file_ps}', f'v{p+2}/{file}', f'--header={file}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.wait()
        proc = subprocess.Popen(['ps2pdf', f'psv{p+2}/{n_file_ps}', f'pdfv{p+2}/{n_file_pdf}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.wait()
        
time.check()