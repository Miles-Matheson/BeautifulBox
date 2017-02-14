#encoding=utf8
import re, sys, os
import Image

SystemFontOfSize_set = set()
RGBA_set = set()
RGBA_map = {}
RGBA_REPACEx = file("../../Classes/UI/R.h", "rb").read()

ignorelist = (".svn", ".DS_Store", "documents",
              "AlipaySDK.framework",
              "DerivedData", "xcuserdata", "project.xcworkspace", "project.pbxproj",
              "Default-568h@2x.png", );

def listdir(fpath):
        if os.path.isfile(fpath):
                print fpath
        if os.path.isdir(fpath):
                temp = os.listdir(fpath)
                temp.sort()
                for _dir in temp:
                        if not _dir in ignorelist:
                                listdir(fpath+"/"+_dir.decode("utf8"))

def searchx(fpath):
        if os.path.isfile(fpath):
            #assert fpath.find("_un@") == -1 and fpath.find("_un.") == -1, fpath
            #assert fpath.find("_sp@") == -1 and fpath.find("_sp.") == -1, fpath
                #print fpath
                assert fpath.split(".")[-1] in ("py", "png", "jpg", "jpeg", "gif", "txt"), fpath
                if fpath.split(".")[-1] in ("py", "txt"):
                        return
                fname = fpath.split("/")[-1]
                #print fname
                x1 = fname.replace("@2x", "")
                assert len(fname.split(".")) == 2
                x2 = x1.split(".")[0] + "@2x." + fname.split(".")[1]
                print "%-50s"%x1, "%-50s"%x2, fpath
                if (os.path.exists("/".join(fpath.split("/")[:-1])+"/"+x1) and
                    os.path.exists("/".join(fpath.split("/")[:-1])+"/"+x2)):
                        assert not fname.startswith("taobao_head_")
                        if x1 in ("", ):
                                return
                        image1 = Image.open(x1)
                        image2 = Image.open(x2)
                        strinfo = "%dx%d" % image1.size + " %dx%d" % image2.size + " " + fpath
                        assert abs(image1.size[0] * 2 - image2.size[0])<=1 or image1.size[0]==image2.size[0], strinfo
                        assert abs(image1.size[1] * 2 - image2.size[1])<=1 or image1.size[1]==image2.size[1], strinfo
                        return
                elif os.path.exists("/".join(fpath.split("/")[:-1])+"/"+x1):
                        #assert not fname.startswith("taobao_head_")
                        if fname.startswith("yuike_pathbg_"):
                                return
                        if fname.startswith("taobao_head_"):
                                return
                        if fname.startswith("weibo_image_"):
                                return
                        if fname.startswith("yuike_dim_code.png"):
                                return
                        if fname.startswith("yuike_item_bg_alphax_"):
                                return

#os.rename(x1, x2)
#im = Image.open(x2)
#im = im.resize((im.size[0]/2, im.size[1]/2), Image.ANTIALIAS) # best down-sizing filter
#im.save(x1, 'PNG')

#assert False, fpath
                        return
                elif os.path.exists("/".join(fpath.split("/")[:-1])+"/"+x2):
                        assert not fname.startswith("taobao_head_")
                        assert False, fpath
                else:
                        assert False, fpath
                        print fname
                
        if os.path.isdir(fpath):
                for _dir in os.listdir(fpath):
                        if not _dir in ignorelist:
                                searchx(fpath+"/"+_dir.decode("utf8"))

#http://www.pythonware.com/library/pil/handbook/index.htm
def main(imagepath, whsplit, xregular):
        image = Image.open(imagepath)
        assert image <> None and whsplit in ("wsplit", "hsplit")
        print image.size
        size = image.size 

        if whsplit == "hsplit":
                kw = size[0]
                kh = size[0]
                if xregular == "grid":
                        kh = kw
                else:
                        num = int(xregular)
                        assert num >= 3
                        kh = size[1] / num

                topimage = Image.open(imagepath).resize((kw, kh))
                midimage = Image.open(imagepath).resize((kw, 1))
                bottomimage = Image.open(imagepath).resize((kw, kh))
                for x in range(kw):
                        midimage.putpixel((x, 0), image.getpixel((x, kh)))
                        for y in range(kh):
                                topimage.putpixel((x, y), image.getpixel((x, y)))
                                bottomimage.putpixel((x, y), image.getpixel((x, size[1]-kh+y)))
                print topimage.size, midimage.size, bottomimage.size
                topimage.save(imagepath.split(".")[0] + "_top.png")
                midimage.save(imagepath.split(".")[0] + "_midh.png")
                bottomimage.save(imagepath.split(".")[0] + "_bottom.png")

        if whsplit == "wsplit":
                kw = size[1]
                kh = size[1]
                if xregular == "grid":
                        kw = kh
                else:
                        num = int(xregular)
                        assert num >= 3
                        kw = size[0] / num
                
                leftimage  = Image.open(imagepath).resize((kw, kh))
                midimage   = Image.open(imagepath).resize((1, kh))
                rightimage = Image.open(imagepath).resize((kw, kh))
                for y in range(kh):
                        midimage.putpixel((0, y), image.getpixel((kw, y)))
                        for x in range(kw):
                                leftimage.putpixel((x, y), image.getpixel((x, y)))
                                rightimage.putpixel((x, y), image.getpixel((size[0]-kw + x, y)))

                print leftimage.size, midimage.size, rightimage.size
                leftimage.save(imagepath.split(".")[0] + "_left.png")
                midimage.save(imagepath.split(".")[0] + "_midw.png")
                rightimage.save(imagepath.split(".")[0] + "_right.png")
        
def searchimage(fpath, imageset, projectset):
        if os.path.isfile(fpath):
                assert(fpath.split(".")[-1] == fpath.split(".")[-1].lower()), fpath
                if fpath.split(".")[-1] in ("h", "m", "py", "txt",
                                            u'default', u'plist', u'pch', u'pbxproj', u'strings'):
                        return
                if fpath.split("/")[-1].startswith("taobao_head_"):
                        return
                if fpath.split("/")[-1].startswith("yuike_pathbg_"):
                        return
                if fpath.split(".")[-1] in ("png", "jpg", "jpeg", ): #"gif"
                        imageset.add(fpath.split("/")[-1].decode("utf8"))
                        print fpath

        if os.path.isdir(fpath):
                for _dir in os.listdir(fpath):
                        if _dir.endswith(".bundle"): continue
                        if not _dir in ignorelist:
                                searchimage(fpath+"/"+_dir, imageset, projectset)

def removeimage(fpath, imageset):
        if os.path.isfile(fpath):
                assert(fpath.split(".")[-1] == fpath.split(".")[-1].lower()), fpath
                if not fpath.split(".")[-1] in ("h", "m", "py", "txt",
                                            u'default', u'plist', u'pch', u'pbxproj', u'strings'):
                        return
                print fpath
                #print file(fpath, "rb").read()
                data = file(fpath, "rb").read()
                page = ""
                while True:
                        try:
                                page = data.decode("utf8")
                                break
                        except:
                                print "error", data[0]
                                data = data[1:]
                                if not data:
                                        assert False
                #print page
                assert not re.findall(r"imageNamed\s*:\s*@\"[^.]+\"", page), re.findall(r"imageNamed\s*:\s*@\"[^.]+\"", page)

                rgba = re.findall("RGBA?\s*\(\s*[0-9.a-zA-Z_]+\s*,\s*[0-9.a-zA-Z_]+\s*,\s*[0-9.a-zA-Z_]+.*?\)", page)
                if (rgba and not fpath.endswith("/R.h") and not fpath.endswith("/image2xcheck.py") and
                            projectset.find("/* %s */"%fpath.split("/")[-1]) >= 0):
                        print rgba
                        pagebak = page[:]
                        for temp in rgba:
                                RGBA_set.add(temp)
                                RGBA_map[temp] = fpath
                        for temp in re.findall("#define\s+(YUIKE_COLOR_[A-Z0-9_]+)\s+(.*?)\n", "\n"+RGBA_REPACEx+"\n\n"):
                                print temp
                                RGBA_set.add(temp[1].strip() + "  --  " + temp[0].strip())
                                page = page.replace(temp[1].strip(), temp[0].strip())
                        if page <> pagebak:
                                fout = file(fpath, "wb")
                                fout.write(page.encode("utf8"))
                                fout.close()
                font = re.findall(r"ystemFontOfSize\s*:\s*.*?\]", page)
                if font:
                        print font
                        for temp in font:
                                SystemFontOfSize_set.add(temp)
                                
                for itemp in imageset:
                        fname = itemp.split("/")[-1]
                        if (not fname in ("Default@2x.png", "Default.png", "Default-568h@2x.png") and
                            not fname in """
                                Stars@2x.jpg Stars.jpg
                                blueArrow.png blueArrow@2x.png
                                backFace@2x.png backFace.png
                                backFaceSelect@2x.png backFaceSelect.png
                                README.md""".split()):
                                pass#assert (fname == fname.lower().replace("ios7", "iOS7").
                                #replace("PopupDialogDafen".lower(), "PopupDialogDafen")), fname
                        x1 = fname.replace("@2x", "")
                        assert len(fname.split(".")) == 2, fname
                        x2 = x1.split(".")[0] + "@2x." + fname.split(".")[1]
                        xx = x1.split(".")[0]
                        #print x1, x2, xx
                        if page.find("\""+xx) != -1: # and not re.findall("^[0-9]{3}$", xx):
                                if re.findall(xx+u"[^ :,.a-zA-Z0-9_]", page) and xx not in (u"关于", u"退款", u"退货"):
                                        print re.findall(xx+"[^ :,]", page)
                                        print xx, "%r" % xx, x1, x2
                                        assert (page.find(x1) != -1 or page.find(x2) != -1), "%r" % xx + " " + fpath
                        if (page.find(x1) != -1 or page.find(x2) != -1 or page.find(xx) != -1):
                                imageset.remove(itemp)
                                removeimage(fpath, imageset)
                                return

        if os.path.isdir(fpath):
                for _dir in os.listdir(fpath):
                        if not _dir in ignorelist:
                                removeimage(fpath+"/"+_dir, imageset)
        

if __name__ == "__main__":
        print sys.argv, "clear/check"
        if "clear" in sys.argv:
                print os.path.abspath(".")
                fpath = os.path.abspath(".")
                assert fpath.count("/beautymall/") == 1

                imageset = set()
                projectpath = fpath.split("/beautymall/")[0] + "/beautymall/"
                projectset = file(projectpath+"/beautymall.xcodeproj/project.pbxproj").read()
                
                searchimage(projectpath, imageset, projectset)
                tempklist = list(imageset)
                tempklist.sort()
                print "\n".join(tempklist)
                removeimage(projectpath, imageset)
                print "===" * 10
                listemp = list(imageset)
                listemp.sort()
                print "\n".join(listemp)
                print "cleared!!"

        if "check" in sys.argv:
                listdir(".")
                print "--" * 50
                searchx(".")
        print "ok"


RGBA_list = list(RGBA_set)
RGBA_list.sort()
#print "\n".join()
for i in RGBA_list:
        if not i:
                continue
        print i, "\t"*2, (RGBA_map[i].split("/beautymall/")[-1] if i in RGBA_map.keys() else "???")
print "--"

Font_list = list(SystemFontOfSize_set)
Font_list.sort()
print "\n".join(Font_list)
print "--"
print sys.argv, "clear/check"

fpage = file(sys.argv[0], "rb").read()
fpage = "\n".join([line.strip() for line in fpage.split("\n") if re.findall("sys.argv[^\\[\\\"]", line)])
print "**" * 10
print fpage.strip()
print
