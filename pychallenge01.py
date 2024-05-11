def fnc(chars):
    out = ''
    for x in chars:
        x = ord(x)
        if x > 48:
            x += 2
            if x > 122:
                x -= 26
        out += chr(x)
    
    return out
    
chars = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. "
print(fnc('map'))
print(fnc(chars))
input()

