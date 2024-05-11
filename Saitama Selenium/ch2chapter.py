import subprocess

p0 = subprocess.Popen(['ls', 'pdf_out'], stdout=subprocess.PIPE, text=True)

out, _ = p0.communicate()

out = out.split('\n')

for x in out:
    n_name = x
    if 'Chapter' in x:
        ind1 = x.index('Chapter')
        n_name = x[:ind1] + x[ind1+7:]
    if 'Ch.' in x:
        ind1 = x.index('Ch.')
        n_name = x[:ind1] + x[ind1+3:]
    if '  ' in x:
        ind1 = x.index('  ')
        n_name = x[:ind1] + x[ind1+1:]
    
    if x != n_name:
        subprocess.Popen(['mv', f'pdf_out/{x}', f'pdf_out/{n_name}'], text=True)


