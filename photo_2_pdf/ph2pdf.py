
print('importing PIL', end=' . . . ')
from PIL import Image
print('done')
print('importing PyPDF2', end=' . . . ')
from PyPDF2 import PdfFileMerger, PdfFileReader
print('done')
print('importing subprocess', end=' . . . ')
import subprocess
print('done')


#p1 = subprocess.Popen([], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

subprocess.Popen(['mkdir', 'inter'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
subprocess.Popen(['mkdir', 'output'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



p1 = subprocess.Popen(['ls', 'input'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
src = p1.communicate()
src = src[0].split('\n')
src = src[:-1]  #getting rid of space at the end

s_src = [' '.join(x.split('.')[:-1]) for x in src]

print('Convert start')
for y, phot in enumerate(src):
    print(f'convert {y} {phot}')
    img = Image.open(f'input/{phot}')
    try:
        img = img.convert('RGB')
    except:
        pass
    img.save(f'inter/{s_src[y]}.pdf')
print('Convert end')
    
    
print('Merge start')
merger = PdfFileMerger()
for y, pdf in enumerate(s_src):
    print(f'merge {y} {pdf}.pdf')
    merger.append(PdfFileReader(f'inter/{pdf}.pdf', 'rb'))
merger.write(f'output/output.pdf')
print('Merge end')


subprocess.Popen(['rm', '-rf', 'inter'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

