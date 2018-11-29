
# function typeStyle (t) {
#     var res;
#     switch (t) {
#     case 2: res = 0; break;
#     case 3: res = 80; break;
#     case 4: res = 170; break;
#     case 5: res = 45; break;
#     case 6: res = 126; break;
#     case 7: res = 215; break;
#     default: return '';
#     }
#     return ';fill:hsl(' + res + ',100%,50%)';
# }

def typeStyle(t=""):
    style = {
        "2":0
        "3":80
        "4":170
        "5":45
        "6":126
        "7":215
    }
    if(t in style):
        return ';fill:hsl({},100%,50%)'.format(style[t])
    else:
        return ''

def labelArr(desc, opt):
    pass

def lane(desc, opt):
    res = container.g(transfrom=Transform.translate(4.5,(opt.lanes - opt.index - 1) * opt.vspace + 0.5))
    res.add(cage(desc, opt))
    res.add(labels(desc, opt))
    return res

def vline(len,x=0 ,y=0):
    return Line(start=(x,y), end=(x,y+len))

def hline(len,x=0 ,y=0):
    return Line(start=(x,y), end=(x+len,y))

def cage(desc, opt):
    hspace = opt.hspace
    vspace = opt.vspace
    mod = opt.mod
    res = container.g(stroke="black;stroke-width=1;stoke-linecap=round", transfrom=Transform.translate(0,vspace/4))
    
    res.add(hline(hspace))
    res.add(vline(vspace/2))
    res.add(hline(hspace, 0, vspace/2))
    
    i = opt.index*opt.mod
    j = opt.mod
    
    for :
        if j == opt.mod or :
            res.add(vline(vspace/2, j*(hspace/mod)))
        else:
            res.add(vline(vlace/16),j*(hspace/mod))
            res.add(vline(vlace/16),j*(hspace/mod), vspace*7/16)

    return res

def labels(desc, opt):
    ret = container.g(text-anchor=middle)
    ret.add(labelArr(desc, opt))
    return ret
