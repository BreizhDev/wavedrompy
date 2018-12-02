import svgwrite
from attrdict import AttrDict
# Extracted from 685722458ce0b3b82a672bd15b73d0fedfb8b284
# https://github.com/drom/bitfield/commit/685722458ce0b3b82a672bd15b73d0fedfb8b284
class Bitfield(object):
    container = AttrDict({
        "defs": svgwrite.container.Defs,
        "g": svgwrite.container.Group,
        "marker": svgwrite.container.Marker,
        "use": svgwrite.container.Use,
        "style": svgwrite.container.Style
    })
    element = AttrDict({
        "rect": svgwrite.shapes.Rect,
        "path": svgwrite.path.Path,
        "text": svgwrite.text.Text,
        "tspan": svgwrite.text.TSpan,
        "line": svgwrite.shapes.Line,
    })
    opt = AttrDict({
        #"index":  0,
        "bigendian": True,
        "hspace": 640,
        "vspace": 80,
        "lanes":  2,
        "bits":   32,
        #"mod":    0,
        "fontsize":   14,
        "fontfamily": 'sans-serif',
        "fontweight": 'normal',
    })

    @staticmethod
    def typeStyle(t=""):
        style = {
            "2":0,
            "3":80,
            "4":170,
            "5":45,
            "6":126,
            "7":215,
        }
        if(t in style):
            return ';fill:hsl({},100%,50%)'.format(style[t])
        else:
            return ''

    def labelArr(self,desc, opt):
        step = opt.hspace / opt.mod
        bits = self.container.g()
        bits.translate(step/2, opt.vspace/5)
        names = self.container.g()
        names.translate(step/2, opt.vspace/2+4)
        attrs = self.container.g()
        attrs.translate(step/2, opt.vspace)
        blanks = self.container.g()
        blanks.translate(0, opt.vspace/4)
        fontsize = opt.fontsize
        fontfamily = opt.fontfamily
        fontweight = opt.fontweight

        for e in desc:
            lsbm = 0
            msbm = opt.mod - 1
            lsb = opt.index * opt.mod
            msb = (opt.index + 1) * opt.mod - 1
            if (e["lsb"] // opt.mod) == opt.index:
                lsbm = e["lsbm"]
                lsb = e["lsb"]
                if (e["msb"] // opt.mod) == opt.index:
                    msb = e["msb"]
                    msbm = e["msbm"]
            else:
                if (e["msb"] // opt.mod) == opt.index:
                    msb = e["msb"]
                    msbm = e["msbm"]
                else:
                    continue

            # bits.push(['text', {
            #      x: step * (opt.mod - lsbm - 1),
            #     'font-size': fontsize,
            #     'font-family': fontfamily,
            #     'font-weight': fontweight
            #     }, lsb.toString()]);

            bits.add(self.element.text(
                lsb,
                insert=((step * (opt.mod - lsbm - 1)),0),
                font_size = fontsize,
                font_family = fontfamily,
                font_weight = str(fontweight)))

            if (lsbm != msbm):
            # bits.push(['text', {
            #     x: step * (opt.mod - msbm - 1),
            #     'font-size': fontsize,
            #     'font-family': fontfamily,
            #     'font-weight': fontweight
            # }, msb.toString()]);
                bits.add(self.element.text(
                    msb,
                    insert=((step * (opt.mod - msbm - 1)),0),
                    font_size = fontsize,
                    font_family = fontfamily,
                    font_weight = fontweight))

            if "name" in e:
                # lText = tspan.parse(e.name);
                # lText.unshift({
                #     x: step * (opt.mod - ((msbm + lsbm) / 2) - 1),
                #     'font-size': fontsize,
                #     'font-family': fontfamily,
                #     'font-weight': fontweight
                # });
                # lText.unshift('text');
                # names.push(lText);
                txt = self.element.text('',
                    insert=((step * (opt.mod - ((msbm + lsbm) / 2) - 1)),0),
                    font_size = fontsize,
                    font_family = fontfamily,
                    font_weight = fontweight)
                txt.add(self.element.tspan(e["name"]))
                names.add(txt)

            if ("type" in e) or not ("name" in e):
                blanks.add(self.element.rect(
                    style = 'fill-opacity:0.1;' + self.typeStyle(str(e.get("type"))),
                    insert = (step * (opt.mod - msbm - 1), 0),
                    size = (step * (msbm - lsbm + 1), opt.vspace / 2)
                ))
            if "attr" in e:
                # attrs.add(self.element.tspan(
                #     e["attr"],
                #     x = str(int(step * (opt.mod - ((msbm + lsbm) / 2) - 1))),
                #     font_size = fontsize,
                #     font_family = fontfamily,
                #     font_weight = fontweight
                # ))
                attrstxt = self.element.text('',
                    insert=(step * (opt.mod - ((msbm + lsbm) / 2) - 1),0),
                    font_size = fontsize,
                    font_family = fontfamily,
                    font_weight = fontweight
                )
                attrstxt.add(self.element.tspan(e["attr"]))
                attrs.add(attrstxt)
        res = self.container.g()
        res.add(blanks)
        res.add(bits)
        res.add(names)
        res.add(attrs)
        return res


    def vline(self,len,x=0 ,y=0):
        return self.element.line(start=(x,y), end=(x,y+len))


    def hline(self,len,x=0 ,y=0):
        return self.element.line(start=(x,y), end=(x+len,y))


    def cage(self,desc, opt):
        hspace = opt.hspace
        vspace = opt.vspace
        mod = opt.mod
        res = self.container.g(stroke="black",stroke_width=1,stroke_linecap="round")
        res.translate(0,vspace/4)

        res.add( self.hline(hspace) )
        res.add( self.vline(vspace/2) )
        res.add( self.hline(hspace, 0, vspace/2) )

        i = opt.index*opt.mod
        j = opt.mod

        for j in reversed(range(1,int(opt.mod)+1)):
            if j == opt.mod or any(e["lsb"] == i for e in desc):
                res.add(self.vline(vspace/2, j*(hspace/mod)))
            else:
                res.add(self.vline(vspace/16,j*(hspace/mod)))
                res.add(self.vline(vspace/16,j*(hspace/mod), vspace*7/16))
            i = i + 1

        return res

    def labels(self,desc, opt):
        ret = self.container.g(text_anchor="middle")
        ret.add(self.labelArr(desc, opt))
        return ret

    def lane(self,desc, opt):
        res = self.container.g()
        res.translate(
            tx = 4.5,
            ty = (opt.lanes - opt.index - 1) * opt.vspace + 0.5
        )
        res.add(self.cage(desc, opt))
        res.add(self.labels(desc, opt))
        return res


    @staticmethod
    def isIntGTorDefault(val, min, default):
        if val > min:
            return val
        else:
            return default

    def render(self, desc, opt):
        opt.vspace = self.isIntGTorDefault(opt.vspace, 19, 80)
        opt.hspace = self.isIntGTorDefault(opt.hspace, 39, 640)
        opt.lanes = self.isIntGTorDefault(opt.lanes, 0, 2)
        opt.bits = self.isIntGTorDefault(opt.bits, 4, 32)
        opt.fontsize = self.isIntGTorDefault(opt.fontsize, 5, 14)

        opt.bigendian = opt.bigendian or False
        opt.fontfamily = opt.fontfamily
        opt.fontweight = opt.fontweight

        res = svgwrite.Drawing(
            size = ((opt.hspace + 9),(opt.vspace * opt.lanes + 5)),
        )
        res.viewbox(
            minx=0,
            miny=0,
            width=(opt.hspace + 9),
            height=(opt.vspace * opt.lanes + 5)
        )

        lsb = 0
        mod = opt.bits // opt.lanes
        opt.mod = mod

        for e in desc:
            e["lsb"] = lsb
            e["lsbm"] = lsb % mod
            lsb = lsb +e["bits"]
            e["msb"] = lsb - 1
            e["msbm"] = e["msb"] % mod

        for i in range(opt.lanes):
            opt.index = i
            res.add(self.lane(desc,opt))

        return res

if __name__ == "__main__":
    x = Bitfield()
    opt = x.opt
    desc = [
    { "name": "IPO",   "bits": 8, "attr": "RO" },
    {                  "bits": 7 },
    { "name": "BRK",   "bits": 5, "attr": "RW", "type": 4 },
    { "name": "CPK",   "bits": 1 },
    { "name": "Clear", "bits": 3 },
    { "bits": 8 }
]
    d = x.render(desc,opt)
    d.save(pretty=True)