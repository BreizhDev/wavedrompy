
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
    pass

def cage(desc, opt):
    pass

def labels(desc, opt):
    pass
