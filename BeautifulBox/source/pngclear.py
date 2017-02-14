#encoding=utf8
import os, re, sys
import Image

#打开 Xcode中等的Organizer，这个开发者都知道
#找到archive右击, 在finder中显示.
#找到MyApp.app.dSYM文件，拷贝到桌面
#cd命令到MyApp.app.dSYM/Contents/Resources/DWARF
#atos -arch armv7 -o MyApp 0x0000000

cacheimg = "cacheimg"
cacheimgx = "cacheimgx"
notindirs = (".svn", "DerivedData", cacheimg, cacheimgx, "documents",
             "Ctrl/FaceBoard",
             "Default-568h@2x.png", "Default-800-667h@2x.png",
             )
typetails = (".png", ".jpeg", ".jpg", ".gif", ".h", ".m", ".mm", ".pch", ".c")
typeset1 = set()
typeset2 = set()
Controller_setx = set() # :.*?Controller
sameset = set()
Recognizer = set()
UIControlEvent = set()
definetag = set()

def mkmd5fromfile(filename):
    import hashlib
    fobj = open(filename, "rb")
    md5 = hashlib.new("md5")
    while True:
        fb = fobj.read(1024)
        if not fb:
            break
        md5.update(fb)
    fobj.close()
    return md5.hexdigest()


ColectPrintedSetx = set()
def colect(dirx, imgset, pathmap):
        
        if os.path.isdir(dirx) and not dirx.endswith(".bundle"):
                for _dir in os.listdir(dirx):
                        if _dir in notindirs:
                                continue                        
                        _path = dirx + "/" + _dir
                        
                        _path = _path.replace("//", "/").replace("//", "/")
                        for x in notindirs:
                                if x.find("/")!=-1 and _path.endswith(x):
                                        _path = None
                                        break
                        if not _path:
                                continue
                        
                        colect(_path, imgset, pathmap)
                        if _dir.endswith(".png") or _dir.endswith(".jpg") or _dir.endswith(".gif") or _dir.endswith(".jpeg"):
                                assert "".join(_dir.split()) == _dir, dirx

        if os.path.isfile(dirx) or dirx.endswith(".bundle"):

                typeset1.add("."+dirx.split(".")[-1])
                
                for _type in typetails:
                        if not dirx.lower().endswith(_type):
                                continue
                        assert dirx.endswith(_type)
                        assert dirx == "".join(dirx.split()), dirx
                        
                        image = dirx.split("/")[-1].split("\\")[-1]
                        if image in imgset:
                                md5_1 = mkmd5fromfile(dirx)
                                md5_2 = mkmd5fromfile(pathmap[image])
                                assert not image in imgset, ("\n"+dirx+" -- %s"%md5_1+
                                                     "\n"+pathmap[image]+" -- %s"%md5_2+
                                                     "\n -- %s" % (md5_1==md5_2))
                        pathmap[image] = dirx
                        imgset.add(image)

                        image2xPath = None
                        image1xPath = None
                        if dirx.find("@2x") != -1:
                                image2xPath = dirx
                                image1xPath = image2xPath.replace("@2x","")
                                assert os.path.exists(image1xPath), "--"+image1xPath + ", " + dirx
                        else:
                                image1xPath = dirx
                                image2xPath = ".".join(dirx.split(".")[:-1]) +"@2x."+ dirx.split(".")[-1]
                        if os.path.exists(image1xPath):
                                size = os.path.getsize(image1xPath)
                                if image1xPath.split(".")[-1] not in ("h", "m", "c"):
                                        if not image1xPath in ColectPrintedSetx:
                                                print image1xPath
                                                ColectPrintedSetx.add(image1xPath)
                                assert size < 1024*1024, image1xPath
                        if os.path.exists(image2xPath):
                                size = os.path.getsize(image2xPath)
                                if image2xPath.split(".")[-1] not in ("h", "m", "c"):
                                        if not image2xPath in ColectPrintedSetx:
                                                print image2xPath
                                                ColectPrintedSetx.add(image2xPath)
                                assert size < 1024*1024, image2xPath

                        image1 = None
                        image2 = None
                        if os.path.exists(image1xPath):
                                try:
                                        image1 = Image.open(image1xPath)
                                        if re.findall("/[0-9]+.[0-9]+\.png", image1xPath):
                                                tempx = re.findall("/([0-9]+)[A-Za-z]([0-9]+)\.[pP][nN][gG]", image1xPath)
                                                print tempx[0], image1.size
                                                assert (image1.size[0]==(int)(tempx[0][0]) and
                                                        image1.size[1]==(int)(tempx[0][1])), image1xPath
                        
                                except IOError:
                                        pass
                        if os.path.exists(image2xPath):
                                try:
                                        image2 = Image.open(image2xPath)
                                except IOError:
                                        pass
                                
                        if image1 and image2:
                                if (abs(image1.size[0] * 2 - image2.size[0])<=1 and
                                    abs(image1.size[1] * 2 - image2.size[1])<=1):
                                        continue
                                if image2xPath.split("/")[-1] in ("cb_box_off@2x.png",
                                                   "cb_box_on@2x.png", "cb_glossy_off@2x.png", "cb_glossy_on@2x.png",
                                                   "cb_mono_off@2x.png", "cb_mono_on@2x.png",
                                                "shadow_low@2x.png", "shadow_low_notch@2x.png", "shadow_top@2x.png",
                                                "shadow_top_notch@2x.png"):
                                        continue
                                if image2xPath.split("/")[-1] in (
                                                ): # backup code...
                                        copy2tempdir(image1xPath)
                                        copy2tempdir(image2xPath)
                                        continue
                                if (abs(image1.size[0] - image2.size[0])<=1 and
                                                abs(image1.size[1] - image2.size[1])<=1):
                                        sameset.add(image1xPath)
                                assert (abs(image1.size[0] * 2 - image2.size[0])<=1 and
                                        abs(image1.size[1] * 2 - image2.size[1])<=1) or (abs(image1.size[0] - image2.size[0])<=1 and
                                                                                         abs(image1.size[1] - image2.size[1])<=1), (
                                        "(%d,%d)/(%d,%d)"%
                                        (image1.size[0], image1.size[1],
                                         image2.size[0], image2.size[1],)) + image2xPath
                        
Controller_set = set()
Controller_set2 = set()
def removeimg(dirx, imgset):
        if os.path.isdir(dirx):
                for _dir in os.listdir(dirx):
                        if _dir in notindirs:
                                continue 
                        _path = dirx + "/" + _dir
                        
                        _path = _path.replace("//", "/").replace("//", "/")
                        for x in notindirs:
                            if x.find("/")!=-1 and _path.endswith(x):
                                _path = None
                                break
                        if not _path:
                            continue
                        
                        removeimg(_path, imgset)
        if os.path.isfile(dirx):

                if dirx.endswith(".m") or dirx.endswith(".h") or dirx.endswith(".mm"):
                        page = file(dirx, "rb").read() + " "
                        
                        for x in re.findall("@interface.*?:.*?Controller[a-zA-Z0-9_]*", page+" "):
                                Controller_setx.add(x)

                        # "interface *?([a-zA-Z0-9_]+) *?\\: *?NSObject[^B]"
                        # "interface\\s*?([a-zA-Z0-9_]+)\\s*?\\:\\s*?NSObject[^B]"
                        # "interface\\s*?([a-zA-Z0-9_]+)\\s*?\\:\\s*?NSObject[^B]"
                        for x in re.findall("interface *?([a-zA-Z0-9_]+) *?\\: *?NSObject[^B]", page+" "):
                                Controller_set.add(x)
                                #print Controller_set
# no cached
# APIBase|APIResponse|BaseReq|BaseResp|CDataScanner|CJSONDataSerializer|CJSONDeserializer|CJSONSerializer|CSSPartMatcher|CSSSelector|CSSSelectorMatcher|CSSSelectorPart|CSerializedJSONData|Chunk|Comment|DBConnection|DirectMessage|DownloadHelper|Draft|DummyGapStatus|ElementParser|GAScriptBlockObject|GAScriptEngine|GAScriptMethodSignatures|GAScriptObject|GTMBase64Weibo|HTTPParam|HTTPParamList|JWFolders|NSObjectBase|OAAsynchronousDataFetcher|OAConsumer|OADataFetcher|OAHMAC_SHA1SignatureProvider|OAPlaintextSignatureProvider|OARequestParameter|OAServiceTicket|OAToken|QAsyncHttp|QMutableURLRequest|QOauth|QOauthKey|QSyncHttp|QWeiboAsyncApi|QWeiboRequest|QWeiboSyncApi|RKLBlockEnumerationHelper|RKLLowMemoryWarningObserver|RSSAttachedMedia|RSSCloudService|RSSEntry|RSSFeed|RSSParser|SBJsonBase|SFHFKeychainUtils|Statement|Status|TencentLogin|TencentOAuth|TencentRequest|TencentTargetSelector|URLParser|User|WXApi|WXAppExtendObject|WXEmoticonObject|WXImageObject|WXMediaMessage|WXMusicObject|WXVideoObject|WXWebpageObject|WebViewJavascriptBridge|XMLParsedElement|XMLParsedTree|XMLParser|YBegUserRecommendTask|YBegUserScoringTask|YFolders|YuikeBase

                        objs = re.findall("(\"[^\"\\n]+\")", page)
                        objs = list(set(objs))
                        objs.sort()
                        for obj in objs[:]:
                                if re.findall("\"[·\\[\\]\t\\$a-zA-Z0-9_ .+:\\(\\)=\\-/\\\\#,%@\\?\\|<>;!\\^&'\\*\\{\\}]+\"", obj):
                                        objs.remove(obj)
                                        continue
                                if (re.findall("\"[^ ;]+\\.png\"", obj) or
                                    re.findall("\"[^ ;]+\\.jpg\"", obj)):
                                        objs.remove(obj)
                                        continue
                                if len(obj) <= 3:
                                        objs.remove(obj)
                                        continue
                                if re.findall("\"([@%].)+\"", obj):
                                        objs.remove(obj)
                                        continue

                        objs = [x for x in objs if x<>"".join(x.split())]
                        if objs and False:
                                print
                                print
                                print dirx
                                for x in objs:
                                        print x
                                print len(objs)

                if dirx.endswith("/ClearOldVersionSomething.m"):
                        return
                if dirx.endswith("/TopImageUrlZoom.m"):
                        return
                if dirx.endswith("/Toast+UIView.h"):
                        return
                if dirx.endswith("/ImageCoverData.m"):
                        return
                if dirx.endswith("/YuiKeAppDelegate.m"):
                        return
                
                
                if dirx.endswith(".m") or dirx.endswith(".h") or dirx.endswith(".mm"):
                        page = file(dirx, "rb").read()
                        pagebak = page[:]
                        imgs = list()
                        
                        temp = re.findall("UI[a-zA-Z]+Recognizer", pagebak)
                        if temp: print temp
                        for kk in temp: Recognizer.add(kk)
                        temp = re.findall("UIControlEvent[a-zA-Z]+", pagebak)
                        if temp: print temp
                        for kk in temp: UIControlEvent.add(kk)
                        temp = re.findall(r"#\s*define\s+([a-zA-Z0-9_]+)\s+([0-9a-fA-FxX]{1,})[^0-9a-fA-FxX]", pagebak)
                        if temp: print temp
                        for kk in temp: definetag.add(kk)
                        
                        for tail in typetails:
                                imgstemp = re.findall("(\\@\"[^\"/%%;]+\\%s\")"%tail, page)
                                imgs = list(set(imgs) | set(imgstemp))
                        for img in imgs:
                                if not (img[2:-1] in imgset) and not ("iPhone_"+img[2:-1] in imgset):
                                        page = page.replace(" /*%s*/ nil " % img, img)
                                        page = page.replace(" /*%s*/ nil " % img, img)
                                        page = page.replace(img, "nil")
                        

                        if pagebak <> page:
                                fout = file(dirx, "wb")
                                fout.write(page)
                                fout.close()
                        #print dirx

def upset(path, imgset1, pathmap):
        page = file(path, "rb").read()
        imgset2 = set()

        for xxx in re.findall("/\\* ([^\\. \"]+\\.[^\\. \"]+) ", page):
                typeset2.add("."+xxx.split(".")[-1])
        for tail in typetails:
                imgset2 = imgset2 | set([x.split("/")[-1] for x in re.findall("/\\* ([^\\. \"]+\\%s) "%tail, page)])
        print
        print "not included:"
        print imgset1-imgset2
        alist = list(imgset1-imgset2)
        for tail in typetails:
                blist = [pathmap[x] for x in alist if x.endswith(tail)]
                blist.sort()
                print
                for x in blist:
                        print x
                        #os.remove(x)
                print len(blist)
        print
        print "include unknow image:"
        print imgset2-imgset1
        #assert imgset2-imgset1 == set([])
        print
        #print "&:"
        #print imgset1&imgset2
        return imgset2

                        
def main(dirxlist, project):
        imgset = set()
        pathmap = {}
        for dirx in dirxlist:
                colect(dirx, imgset, pathmap)
        imgset = upset(project, imgset, pathmap)
        for dirx in dirxlist:
                removeimg(dirx, imgset)

if __name__ == "__main__":
        main([".", "../product"], "./beautymall.xcodeproj/project.pbxproj")
        #main(["../framework/mcf",], "../framework/mcf/mcf.xcodeproj/project.pbxproj")
        print typeset1-set(typetails)
        print typeset2-set(typetails)
        print "ok"

print
print
print 
Controller_list = list(Controller_set-Controller_set2)
Controller_list.sort()
print len(Controller_list)
print "|".join(Controller_list)

def anny(page):
        page = page.strip()
        retx = {}
        for line in page.split("\n"):
                line = line.strip()
                if not line:
                        continue
                a, b = line.split(": ")
                retx[a] = int(b)
        return retx

def printx(ax, bx):
        ax_keys = ax.keys()
        bx_keys = bx.keys()
        all_keys = list(set(ax_keys) | set(bx_keys))
        all_keys.sort()
        for key in all_keys:
                av = ax[key] if key in ax_keys else 0
                bv = bx[key] if key in bx_keys else 0
                if bv - av != 0:
                        print key, "\t%d -> %d = %d" % (av, bv, bv-av)


ax = anny("""Ad: 4
Ads: 1
Parameters: 1
RecommendApp: 6
YkSystem: 1""")

bx = anny("""Ad: 4
YTaskResult: 8
YkOnlineNumber: 1
YkSystem: 1""")

print
print "--"
printx(ax, bx)
print len(Controller_setx)
listemp = list(Controller_setx)
listemp.sort()
print "\n".join(listemp)

print "***" * 10
listtemp = list(sameset)
listtemp.sort()
print "\n".join(listtemp)
print "taskok"


print Recognizer
print UIControlEvent
#print definetag
definetagdict = {}
for x, y in definetag:
        ky = "0"+y if len(y)<2 else y;
        if ky in definetagdict.keys():
                definetagdict[ky].append(x)
        else:
                definetagdict[ky] = []
                definetagdict[ky].append(x)
#print definetagdict
keys = definetagdict.keys()
keys.sort()
for key in keys:
        value = definetagdict[key]
        if len(value) <= 1: continue
        value.sort()
#print "%10s"%key, value

fpage = file(sys.argv[0], "rb").read()
fpage = "\n".join([line.strip() for line in fpage.split("\n") if re.findall("sys.argv[^\\[\\\"]", line)])
print "**" * 10
print fpage.strip()
print
