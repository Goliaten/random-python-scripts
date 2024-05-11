# f = 0
# while f < 101:
#     f += 10
#     name = str(f) + '.txt'
#     with open(name, 'w') as file:
#         for x in range(0, f):
#             if x == 0:
#                 continue
#             y = chr(x) + '\n'
#             file.write(y)
#             print(x, y)
with open('asciimax.txt', 'w') as file:
    for x in range(1, 11141111):
        try:
            file.write(str(x) + ': ' + chr(x) + '\n')
        except:
            file.write(str(x) + '-------unable-to-write-----\n')