#encoding=utf8
import os, re, sys
import Image

print sys.argv, "xxk"
def analyze(path, page, mfile, hfile):
    props = re.findall("@\\s*property.*?;", page.replace("//@property", "//"))
    if not props:
        return
    
    if page.find("YMallJsonObj"):
        assert not re.findall("objectForKey\\s+:", page), path

    allok = True
    failpage = ""
    for prop in props:
        temp = re.findall("(\\(.*?\\)).*?([a-zA-Z0-9_]+)\\s*;", prop)
        if not temp:
            if prop.find("indexChangeBlock") != -1:
                continue
            if prop == "@property \"];":
                continue
            if re.findall("@property [a-zA-Z0-9_<>]+ [a-zA-Z0-9_*]+;", prop):
                continue

        if temp == [] and re.findall("@[a-zA-Z0-9_]+\\s*[a-zA-Z0-9_]+\\s*[a-zA-Z0-9_]+\\s*;", prop.strip()):
            continue

        xxxlist = "".join(temp[0][0].replace("(","").replace(")","").split()).split(",") # 分割属性。
        xxxlist = [xk.split("=")[0] for xk in xxxlist if xk.split("=")[0]]
        for kk in ("nonatomic", "assign", "readonly", "readwrite", "getter", "unsafe_unretained", "weak", "setter", "atomic"):
            if kk in xxxlist: xxxlist.remove(kk)
        for kk in xxxlist:
            assert kk in ("strong", "copy", "retain"), kk
        if not xxxlist:
            continue
        #print xxxlist
        print temp, prop, path
        assert len(temp) == 1
        assert len(temp[0]) == 2
        if not re.findall("@\\s*implementation", page):
            continue

        localvar = "_" + temp[0][1]
        selfvar = temp[0][1]
        akkkk = re.findall("@\\s*synthesize.*?[^a-zA-Z0-9_]"+selfvar+"\\s*=\\s*([a-zA-Z0-9_]+)", page)
        if akkkk:
            localvar = akkkk[0].strip()
        akkkk = re.findall("@\\s*synthesize\\s+"+selfvar+"\\s*;", page)
        if akkkk:
            localvar = temp[0][1].strip()
        akkkk = re.findall("@\\s*synthesize\\s+.*?,.*?;", page)
        if akkkk:
            for xx in akkkk:
                xx = "synthesize".join(xx.split("synthesize")[1:])
                assert re.findall("^[a-zA-Z0-9_=,;\\s]+$", xx), xx
                for x in xx.replace(";",",").split(","):
                    x = x.strip()
                    if not x: continue
                    if x.find("=") == -1:
                        if x.strip() == selfvar: localvar = selfvar
                        continue
                    assert len(x.split("=")) == 2
                    if x.split("=")[0]==selfvar: localvar = x.split("=")[1].strip()
                    continue
        assert re.findall("^[a-zA-Z0-9_]+$", localvar), localvar

        print "***" * 10
        dealloc_open = False
        super_dealloc_find = False
        dealloc_page = ""
        check_ok = False
        
        last_not_empty_line = ""
        setfunc_begined = False
        for line in page.split("\n"):
            
            # 崩溃不管，崩溃会直接暴漏，主要是 泄漏问题。。。。
            # 成员。如果self。必须对称；否则，...
            # FUNC。
            # reassign。YRC。。。
            tempx = re.findall(r"([a-zA-Z0-9_]+\..*?=.*?alloc.*?init.*?;)", line)
            if tempx:
                print tempx
                assert re.findall("release", tempx[0]), path + " " + tempx[0]
            tempx = re.findall(r"([a-zA-Z0-9_]+\..*?=.*?retain.*?;)", line)
            if tempx:
                print tempx
                assert re.findall("release", tempx[0]), path + " " + tempx[0]
            tempx = re.findall("retain\\s*\\]", line)
            if tempx:
                print tempx, line
                assert not line.strip().startswith("self."), path + " " + tempx[0]
            
            
            if re.findall("-.*?void.*?set"+selfvar[:1].upper()+selfvar[1:]+"\\s*?:", line):
                assert not setfunc_begined, last_not_empty_line
                setfunc_begined = True
            if setfunc_begined:
                temp = re.findall("\\s"+localvar+"\\s*?=", line)
                if temp:
                    print temp, last_not_empty_line
                    assert (re.findall(localvar+"\\s+release", last_not_empty_line) or
                            re.findall("YRelease\\("+localvar+"\\)", last_not_empty_line)
                            ), path
            if setfunc_begined and line.strip() == "}":
                setfunc_begined = False
                last_not_empty_line = ""
            if line.strip() and setfunc_begined:
                last_not_empty_line = last_not_empty_line +" "+ line.strip()
        
        
            if re.findall("-\\s*\\(\\s*void\\s*\\)\\s*dealloc", line):
                dealloc_open = True
                super_dealloc_find = False
                dealloc_page = ""
            
            if dealloc_open: print line
            if dealloc_open: dealloc_page=dealloc_page+"\n" + line.strip()
            
            # for memo xx ===
            for xfile in (mfile, hfile):
                if not "xxk" in sys.argv:
                    continue
                if not os.path.exists(xfile):
                    continue
                fxpage = file(xfile, "rb").read()
                bakpage = fxpage[:]
                #xxxo = re.findall("\\sself." + selfvar + "\\s*=[^=]", fxpage)
                #print xxxo
                xxxo = re.findall("(\n\\s*" + localvar + "\\s*=[^=])", fxpage)
                if not xxxo: continue
                xxxo = list(set(xxxo))
                print xxxo
                for xxx in xxxo: # @synthesize
                    #fxpage = fxpage.replace(xxx, "assert(!"+localvar + ");YRelease("+localvar+");"+localvar+xxx.split(localvar)[-1])
                    fxpage = fxpage.replace(xxx, ""+xxx.split(localvar)[0]+"YRC("+localvar+")"+xxx.split(localvar)[-1])
                #@synthesize assert(!object);YRelease(object);object=object;
                #xxxo = re.findall("synthesize\\s+assert\\(\\!%s\\);YRelease\\(%s\\);" % (localvar, localvar), fxpage)
                xxxo = re.findall("synthesize\\s+YRC\\(%s\\)" % (localvar,), fxpage)
                for xxx in xxxo:
                    #fxpage = fxpage.replace(xxx, xxx.split("assert")[0])
                    fxpage = fxpage.replace(xxx, xxx.split("YRC")[0]+localvar)
                if bakpage <> fxpage:
                    foutx = file(xfile, "wb")
                    foutx.write(fxpage)
                    foutx.close()
            # end memo

            if dealloc_open and not check_ok:
                xxk = re.findall("^\\s*YRelease\\("+localvar+"\\)", line)
                if xxk:
                    check_ok = True
                    index = page.find(xxk[0])
                    page = page[:index] + page[index+2:] # 避免两个一样的变量
                xxk = re.findall("^\\s*self."+selfvar+"\s*=\s*nil;", line)
                if xxk:
                    check_ok = True
                    index = page.find(xxk[0])
                    page = page[:index] + page[index+2:] # 避免两个一样的变量
                xxk = re.findall("^\\s*\\["+localvar+"\\s+"+"release\\];\\s*"+localvar+"\\s*=\\s*nil;", line)
                if xxk:
                    check_ok = True
                    index = page.find(xxk[0])
                    page = page[:index] + page[index+2:] # 避免两个一样的变量

            if re.findall("\\[\\s*super\\s+dealloc\\s*\\]", line):
                super_dealloc_find = True

            if line.find("}") != -1 and dealloc_open:
                dealloc_open = False
                assert super_dealloc_find
                
                # 不能有两非空行是一样的，避免同一个文件两个类出现同一个须要释放的变量。
                xxxtemp = [xx.strip() for xx in dealloc_page.split("\n") if xx.strip()]
                assert len(xxxtemp) == len(set(xxxtemp)), dealloc_page
                
                dealloc_page = "".join(dealloc_page.split())
                #print dealloc_page
                assert dealloc_page.endswith("[superdealloc];}") or dealloc_page.endswith("[superdealloc];#endif}")

        if not check_ok:
            print path, localvar
            allok = False
            #failpage = failpage + "\n" + "self."+selfvar+" = nil;"
            failpage = failpage + "\n" + "YRelease("+localvar+");"

    if not allok:
        print """\n\n\n-(void) dealloc
            {"""
        print failpage.lstrip(), """\n[super dealloc];
            }""", "\n\n\n"
    assert allok, path


abspathset = set()

def removeMoreEmptyLine(path):
    if not os.path.exists(path):
        return
    fin = file(path, "rb")
    page = fin.read()
    fin.close()
    pagebak = page[:]
    page = page.replace("\n\n\n\n\n", "\n\n\n\n").replace("\n\n\n\n\n", "\n\n\n\n").replace("\n\n\n\n\n", "\n\n\n\n").replace("\n\n\n\n\n", "\n\n\n\n")
    if page <> pagebak:
        fout = file(path, "wb")
        fout.write(page)
        fout.close()

def doCheckFile(path):
    hfile = ".".join(path.split(".")[:-1])+".h"
    mfile = ".".join(path.split(".")[:-1])+".m"
    removeMoreEmptyLine(hfile)
    removeMoreEmptyLine(mfile)
    if hfile in abspathset:
        return
    abspathset.add(hfile)

    page = ""
    if os.path.exists(hfile):
        page = page +"\n\n"+ file(hfile, "rb").read()+"\n\n"
    if os.path.exists(mfile):
        page = page +"\n\n"+ file(mfile, "rb").read()+"\n\n"
    analyze(path, page, mfile, hfile)

def doCheck(path):
    if path.split(".")[-1] in ("xcodeproj", "build",):
        return
    if path.split("/")[-1] in ("MAZeroingWeakRef-master", "OpenUDID-master",
                               "AESCrypt", "CocoaSecurity",
                               "RESideMenu", "documents",
                               # for ARC ...
                               "SGActionView", "MLEmojiLabel",
                               "SettingsViewController.m", "SettingsViewController.h",
"CoinImageView.h", "CoinImageView.m", "AdvertiseView", "AdvertiseView.h", "AdvertiseView.m",
                               "AdvertiseDataManager", "AdvertiseDataManager.h", "AdvertiseDataManager.m",
                               "QQConnectSDK", "Reference"):
        return
    if os.path.isdir(path):
        for temp in os.listdir(path):
            if not temp in (".svn",): doCheck(path+"/"+temp)
        return
    if path.split(".")[-1] in ("png", "jpeg", "jpg", "gif",
                               "DS_Store", "framework",
                               "py", "sh", "c", "txt",
                               "a", "json", "mp3",
                               "plist", "pch", "strings",
                               "default", "entitlements"):
        return
    if path.split("/")[-1].find(".")==-1: return

    if path.split(".")[-1] in ("h", "m", "mm",):
        doCheckFile(path)
        return
    assert False, path

files = {
"framework": set(),
"dylib": set(),
"a": set(),
}
def delfile(dirx, page):
    if os.path.isfile(dirx):
        if page.find(dirx.split("/")[-1]) == -1 and dirx.split(".")[-1] in ("h", "m", "mm",):
            if dirx.find(".framework/")==-1: os.remove(dirx)
    if os.path.isdir(dirx):
        for kx in os.listdir(dirx):
            if kx in ("MAZeroingWeakRef-master",):
                continue
            delfile(dirx+"/"+kx, page)

    xlist = re.findall("/\\* ([^\\s]+) in ([^\\s]+) \\*/", page)
    for x, y in xlist:
        if x.split(".")[-1] in ("m", "h", "mm", "png", "gif", "md", "png", "jpeg", "jpg", "mp3",
                                "py", "default", "strings", "xcassets", "json",
                                "plist", "pch", "strings", "bundle", "txt", "c", "tbd"):
            continue
        if x.split(".")[-1] in ("framework", "dylib", "a"):
            files[x.split(".")[-1]].add(x)
            continue
        print x, y
        assert False

def check(dirx, dodel):
    #dirx = os.path.abspath(dirx)
    temp = [x for x in os.listdir(dirx) if x.endswith(".xcodeproj")]
    print temp
    assert len(temp) == 1
    xcodeproj_dir = temp[0]
    xcodeproj_page = file(dirx+"/"+xcodeproj_dir+"/"+"project.pbxproj", "rb").read()
    if dodel: delfile(dirx, xcodeproj_page)
    
    assert os.path.exists(dirx)
    print dirx
    for temp in os.listdir(dirx):
        if not temp in (".svn",): doCheck(dirx+"/"+temp)

if __name__ == "__main__":
    check(".", True)
    # -fobjc-arc
    check("../framework/mcf", False)
    print "ok"
#assert False

libs = []
for key in files.keys():
    print "\n".join(files[key])
    for x in files[key]:
        libs.append(x)


for temp in """
SystemConfiguration.framework
QuartzCore.framework
CoreTelephony.framework
libicucore.dylib
libz.1.2.5.dylib
libstdc++.dylib
libsqlite3.dylib
Security.framework

CoreLocation.framework
MessageUI.framework
CoreMotion.framework
    """.split():
    assert temp in libs, temp
for temp in """
MediaPlayer.framework
CoreText.framework
AssetsLibrary.framework
    """.split():
    assert not temp in libs, temp

for xx in """
    CFNetwork.framework
    AGCommon.framework
    AudioToolbox.framework
    
    Foundation.framework
    MessageUI.framework
    MobileCoreServices.framework
    OpenGLES.framework
    QuartzCore.framework
    Security.framework
    StoreKit.framework
    SystemConfiguration.framework
    UIKit.framework
    
    CoreData.framework
    CoreGraphics.framework
    CoreLocation.framework
    CoreTelephony.framework
    
    libmtasdk.a
    
    libicucore.dylib
    libsqlite3.dylib
    libstdc++.dylib
    libz.1.2.5.dylib
    libz.dylib
    
    SinaWeiboConnection.framework
    TencentWeiboConnection.framework
    TencentOpenAPI.framework
    QQConnection.framework
    QZoneConnection.framework
    libSinaWeiboSDK.a
    libTCWeiboSDK.a
    
    WeChatConnection.framework
    libWeChatSDK.a
    
    libMobClickLibrary.a
    libUMFeedback.a
    
    ShareSDK.framework
    ShareSDKCoreService.framework
    ShareSDKFlatShareViewUI.framework
    ShareSDKShareActionSheet.framework
    ShareSDKiPadDefaultShareViewUI.framework
    ShareSDKiPadSimpleShareViewUI.framework
    ShareSDKiPhoneAppRecommendShareViewUI.framework
    ShareSDKiPhoneDefaultShareViewUI.framework
    ShareSDKiPhoneSimpleShareViewUI.framework
    """.split():
    if xx in libs: libs.remove(xx)
libs = list(set(libs))
libs.sort()
print "***" * 10
print "\n".join(libs)
print "***" * 10


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
print sys.argv, "xxk"
print "ok"

fpage = file(sys.argv[0], "rb").read()
fpage = "\n".join([line.strip() for line in fpage.split("\n") if re.findall("sys.argv[^\\[\\\"]", line)])
print "**" * 10
print fpage.strip()
print
