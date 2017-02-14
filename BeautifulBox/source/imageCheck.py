#encoding=utf8
import re, sys, os
import Image

assert file("imageCheck.py", "rb").read().find("\t") == -1
#searchx(fpath+"/"+_dir.decode("utf8"))
ignorelist = (".svn", ".DS_Store", "documents", )

sourceignorelist = file("imageCheckIgnore.txt", "rb").read().split()
print "sourceignorelist", sourceignorelist

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

xxpset = set()
def xxp(fname, bigimgset=None):
    if fname in xxpset: return
    xxpset.add(fname)

    image = Image.open(fname)
    #print image.size, image.getpixel((0, 0))

    if image.size == (768, 1024): return
    if image.size[0] == 768: return
    if fname in ("Default-568h@2x.png", ):
        return
    if fname.split("/")[-1] in file("imageCheckIgnore.txt", "rb").read().split():
        return
    assert image.size[0] <= 640, fname + " -- %dx%d"%image.size
 
    imagesizectrl = 1024 * 51 / 4.0 # 51KB
    if image.size[0] < imagesizectrl**0.5 and image.size[1] < imagesizectrl**0.5:
        return
    if image.size[0] * image.size[1] < imagesizectrl:
        return

    imagesizectrl = 1024 * 101 / 4.0 # 101KB
    if image.size[0] < imagesizectrl**0.5 or image.size[1] < imagesizectrl**0.5:
        return
    if image.size[0] * image.size[1] < imagesizectrl:
        return
    
    print "%-60s"%fname, image.size, "\t", "%.2f"%(image.size[0]*image.size[1]*4.0/1024,), "KB", "\t",
    print "%.2f"%(os.path.getsize(fname)*1.0/1024,), "KB"
    if bigimgset: bigimgset.add(fname.split("/")[-1].split(".")[0])
    #if image.size[0]*image.size[1] >= 480*600: assert fname.endswith(".jpg"), fname
    
        
def findfileindex(paths, filemap, fileset, filetargetset):
    #print paths, filemap, fileset, filetargetset
    #print paths
    if not paths: return
    if type(paths) == list:
        for temp in paths:
            findfileindex(temp, filemap, fileset, filetargetset)
        return
    assert type(paths) == str, paths
    fpath = paths
    
    rootdir = fpath
    rootdirbak = rootdir[:]
    while rootdir and type(rootdirbak)==str and not os.path.exists(rootdir) and rootdir.startswith("../"):
        rootdir = rootdir[3:]
    if type(rootdirbak)==str and not os.path.exists(rootdir):
        rootdir = rootdirbak
    fpath = rootdir
    
    for _dir in ("ShareSDK", "Alixpay.bundle"):
        if fpath.find("/"+_dir+"/") != -1:
            return
    #print "fapth", fpath
    if os.path.isfile(fpath):
        fname = fpath.split("/")[-1]
        if not fname in filetargetset:
            return
        if fname in ("main.m", ):
            return
        if fname.split(".")[-1] in ("md", "strings"):
            return
        if fname in fileset:
            pass
            #print filemap[fname], mkmd5fromfile(filemap[fname])
            #print fpath, mkmd5fromfile(fpath)
        if fname in filemap and filemap[fname] <> fpath:
            assert not fname in fileset, filemap[fname] + " / " + fpath
        #print fname, fpath
        fileset.add(fname)
        filemap[fname] = fpath
    elif os.path.isdir(fpath):
        #print "dir", fpath
        for _dir in os.listdir(fpath):
            if _dir.endswith(".framework"):
                continue
            if not _dir in ignorelist:
                findfileindex(fpath+"/"+_dir, filemap, fileset, filetargetset)
    else:
        temp = findfile(fpath.split("/")[-1], ".")
        assert temp, fpath
        findfileindex(temp, filemap, fileset, filetargetset)

def findfile(fname, rootdir=None):
    if not rootdir:
        return findfile(fname, ".")
    
    rootdirbak = rootdir[:]
    while rootdir and type(rootdirbak)==str and not os.path.exists(rootdir) and rootdir.startswith("../"):
        rootdir = rootdir[3:]
    if type(rootdirbak)==str and not os.path.exists(rootdir):
        rootdir = rootdirbak
    
    rootdirs = None
    if type(rootdir) == list:
        rootdirs = rootdir
    elif os.path.isdir(rootdir):
        rootdirs = [rootdir+"/"+temp for temp in os.listdir(rootdir) if not temp in ignorelist]
    elif os.path.isfile(rootdir):
        if rootdir.endswith("/"+fname):
            return rootdir
    else: # file not exist!!
        #print fname, rootdir
        xrootdir = findfile(rootdir.split("/")[-1], ".")
        assert xrootdir, rootdir
        return findfile(fname, xrootdir)
        
    if not rootdirs:
        return None
    
    result = None
    for tempdir in rootdirs:
        #if tempdir.endswith("/"+fname) and False:
        #    assert not result, result
        #    result = tempdir
        temp = findfile(fname, tempdir)
        if temp:
            assert not result, result
            result = temp
    return result
    
def orgpath(path):
    while path.startswith("\""):
        path = path[1:]
    while path.endswith("\"") or path.endswith(",") or path.endswith(";") or path.endswith("*") or path.endswith("/"):
        path = path[:-1]
    return path

def checkfpath(fpath):
    assert "".join(fpath.split()) == fpath, fpath
    assert(fpath.split(".")[-1] == fpath.split(".")[-1].lower()), fpath


def checkimage(fpath):
    assert os.path.isfile(fpath)
    checkfpath(fpath)
    
    #assert fpath.find("_un@") == -1 and fpath.find("_un.") == -1, fpath
    #assert fpath.find("_sp@") == -1 and fpath.find("_sp.") == -1, fpath
    assert fpath.split(".")[-1] in ("py", "png", "jpg", "jpeg", "gif", "json", "txt"), fpath
    if fpath.split(".")[-1] in ("py", "txt"):
        return
        
    fname = fpath.split("/")[-1]
    assert len(fname.split(".")) == 2
    x1 = fname.replace("@2x", "")
    x2 = x1.split(".")[0] + "@2x." + fname.split(".")[1]
    #print "%-50s"%x1, "%-50s"%x2, fpath
    #print fpath
    
    for temp in ("FaceBoard", "ShareSDK", "Alixpay.bundle"):
        if fpath.find("/"+temp+"/") != -1:
            return

    path1 = "/".join(fpath.split("/")[:-1])+"/"+x1
    path2 = "/".join(fpath.split("/")[:-1])+"/"+x2
    #print path1, os.path.exists(path1), path2, os.path.exists(path2)
    
    tempre = re.findall("[0-9]+[^0-9][0-9]+\\.[a-z]+", fname)
    if tempre:
        imagesizere = re.findall("([0-9]+)", tempre[0])
        image = Image.open(path1)
        print fname, tempre, imagesizere, image.size
        assert image.size[0] == int(imagesizere[0])
        assert image.size[1] == int(imagesizere[1])
    
    if os.path.exists(path1): xxp(path1)
    if os.path.exists(path2): xxp(path2)
    
    
    if os.path.exists(path1) and os.path.exists(path2):
        
        assert not fname.startswith("taobao_head_")
        if x1 in ("", ): return
        
        image1 = Image.open(path1)
        image2 = Image.open(path2)
        strinfo = "%dx%d" % image1.size + " %dx%d" % image2.size + " " + fpath
        #print strinfo
        assert abs(image1.size[0]*2 - image2.size[0])<=1 or image1.size[0]==image2.size[0], strinfo
        assert abs(image1.size[1]*2 - image2.size[1])<=1 or image1.size[1]==image2.size[1], strinfo
        return
    
    elif os.path.exists(path1):
        
        #assert not fname.startswith("taobao_head_")
        pass
            
    #http://www.pythonware.com/library/pil/handbook/index.htm
    elif os.path.exists(path2):
        
        assert not fname.startswith("taobao_head_")
        
        #os.rename(x1, x2)
        #im = Image.open(x2)
        #im = im.resize((im.size[0]/2, im.size[1]/2), Image.ANTIALIAS) # best down-sizing filter
        #im.save(x1, 'PNG')
        
        if fname in ("Default-568h@2x.png", ):
            return

        print fname, fpath
        assert False, fpath

    else:
        print fname, fpath
        assert False, fpath


projectpage = file(findfile("project.pbxproj"), "rb").read()
resources = re.findall("/\\* (.*?) in Resources \\*/", projectpage)
resources = list(set(resources))
resources.sort()
#print "\n".join(resources)
print len(resources)

sourcefiles = re.findall("/\\* (.*?) in Sources \\*/", projectpage)
sourcefiles = list(set(sourcefiles))
sourcefiles.sort()
#print "\n".join(sourcefiles)
print len(sourcefiles)


tempk = re.findall("/\\* (.*?) \\*/", projectpage)
for kx in tempk:
    if len(kx.split()) <= 1:
        continue
    if kx.split()[0] in ("Supporting", "Build", "Project", "Begin", "End"):
        continue
    assert len(kx.split()) == 3, kx
    assert kx.split()[1] == "in", kx
tempk = [kx.split()[-1] for kx in tempk if len(kx.split()) >= 2 and kx.split()[-2] == "in"]
tempk = list(set(tempk))
print tempk
assert tempk == ['Sources', 'Resources', 'Frameworks']

sources = re.findall("/\\* ([^\\s]*?) \\*/", projectpage)
sources = list(set(sources))
sources.sort()
#print "\n".join(sources)
print len(sources)
#print sourcefiles
for mfile in sourcefiles[:]:
    if mfile.endswith(".m"):
        hfile = mfile[:-2] + ".h"
        sourcefiles.append(hfile)
sourcefiles.remove('main.h')
sourcefiles.sort()
#print sourcefiles


paths = re.findall("[^a-zA-Z0-9_](\"?\\.\\./.*?)\s", projectpage)
paths = [orgpath(path) for path in paths]
paths = list(set(paths))
paths.sort()
print "\n".join(paths)
paths.append(".")


SystemFontOfSize_set = set()
RGBA_set = set()
RGBA_map = {}
RGBA_REPACEx = file(findfile("R.h"), "rb").read()
SourceImageSet = set()

def checksourcefile(fpath):
    checkfpath(fpath)

    data = file(fpath, "rb").read()
    page = data.decode("utf8")
    assert page, fpath
    #print fpath
    assert not re.findall(r"imageNamed\s*:\s*@\"[^.]+\"", page), re.findall(r"imageNamed\s*:\s*@\"[^.]+\"", page)
    assert not re.findall(r"imageNamedStr\s*:\s*@\"[^.]+\"", page), re.findall(r"imageNamedStr\s*:\s*@\"[^.]+\"", page)
    
    for temp in re.findall("@\"([^\"]+?\\.(png|jpg|jpeg))\"", page):
        #if temp: print temp[0]
        xxname = temp[0]
        xyname = xxname.split(".")[0] + "@2x." + xxname.split(".")[-1]
        SourceImageSet.add(xxname)
        SourceImageSet.add(xyname)
        SourceImageSet.add((xxname).encode("utf8"))
        SourceImageSet.add((xyname).encode("utf8"))
        SourceImageSet.add(xxname.split(";")[-1])
        SourceImageSet.add(xyname.split(";")[-1])
        SourceImageSet.add((xxname).encode("utf8").split(";")[-1])
        SourceImageSet.add((xyname).encode("utf8").split(";")[-1])

    rgba = re.findall(r"RGBA?\s*\(\s*[0-9a-zA-Z_.]+\s*,\s*[0-9a-zA-Z_.]+\s*,\s*[0-9a-zA-Z_.]+.*?\)", page)
    if rgba and not fpath.endswith("/R.h"):
        #print rgba
        pagebak = page[:]
        for temp in rgba:
            RGBA_set.add(temp)
            RGBA_map[temp] = fpath
        for temp in re.findall(r"#\s*define\s+([A-Z0-9_]+)\s+(.*?RGB.*?)\n", "\n"+RGBA_REPACEx+"\n\n"):
            #print temp
            RGBA_set.add(temp[1].strip() + "  --  " + temp[0].strip())
            page = page.replace(temp[1].strip(), temp[0].strip())
        if page <> pagebak:
            fout = file(fpath, "wb")
            fout.write(page.encode("utf8"))
            fout.close()

    font = re.findall(r"ystemFontOfSize\s*:\s*.*?\]", page)
    if font:
        #print font
        for temp in font:
            SystemFontOfSize_set.add(temp)


    for itemp in resources:
        fname = itemp.split("/")[-1].decode("utf8")
        continue
    
        x1 = fname.replace("@2x", "")
        assert len(fname.split(".")) == 2, fname
        x2 = x1.split(".")[0] + "@2x." + x1.split(".")[1]
        xx = x1.split(".")[0]
        #print x1, x2, xx
        if page.find("\""+xx) != -1 and False: # and not re.findall("^[0-9]{3}$", xx):
            if re.findall(xx+u"[^ :,a-zA-Z0-9_.]", page): # and xx not in ("button_ok", u"关于", ):
                #print re.findall(xx+"[^ :,]", page)
                #print xx, "%r" % xx, x1, x2
                assert (page.find(x1) != -1 or page.find(x2) != -1), "%r" % xx + " " + fpath
        if (page.find(x1) != -1 or page.find(x2) != -1 or page.find(xx) != -1):
            pass#imageset.remove(itemp)
            #removeimage(fpath, imageset)


def checksource():
    filemap = {}
    fileset = set()
    findfileindex(paths, filemap, fileset, sourcefiles)
    #print filemap
    for source in sourcefiles:
        filetype = source.split(".")[-1]
        if filetype in ("strings", "md", "py", "default", "bundle", "txt", "plist"):
            continue
        assert filetype in ("h", "m", "c", "mm"), filetype
        if source.split("/")[-1] in sourceignorelist:
            continue

        sourcepath = filemap[source]#findfile(source, paths)
        #print sourcepath
        assert source and sourcepath, source
        checksourcefile(sourcepath)

    RGBA_list = list(RGBA_set)
    RGBA_list.sort()
    #print "\n".join()
    for ix in RGBA_list:
        if not ix:
            continue
        print ix, "\t"*2, (RGBA_map[ix].split("/beautymall/")[-1] if ix in RGBA_map.keys() else "???")
    print "--"

    Font_list = list(SystemFontOfSize_set)
    Font_list.sort()
    print "\n".join(Font_list)
    print "--"

def checkimagek(): 
    filemap = {}
    fileset = set()
    findfileindex(paths, filemap, fileset, resources)
    #print paths, filemap, resources
    for resource in resources:
        filetype = resource.split(".")[-1]
        if filetype in ("strings", "md", "py", "default", "bundle", "txt", "plist", "json", "xcassets"):
            continue
        assert filetype in ("png", "jpg", "jpeg", "gif", ), filetype

        resourcepath = filemap[resource]#findfile(resource, paths)
        #print resourcepath
        checkimage(resourcepath)
        assert resource and resourcepath, resource

    #print SourceImageSet
    print u"选中框.png" in SourceImageSet, "选中框.png" in SourceImageSet
    for resource in resources:
        filetype = resource.split(".")[-1]
        if not filetype in ("png", "jpg", "jpeg", "gif", ):
            continue
        if SourceImageSet:
            flag = False
            for temp in ("[0-9]{3}\\.png", "[0-9]{3}@2x\\.png", "[0-9]+x[0-9]+\\.png",
            "Default-568h@2x.png", "Default.png", "Default@2x.png", "Default~ipad.png",
            "cb_[a-z]+_(on|off)(@2x)?.png"):
                if re.findall("^"+temp+"$", resource):
                    flag = True
            for temp in file("imageCheckIgnore.txt", "rb").read().split():
                if re.findall("^"+temp+"$", resource):
                    flag = True
            if flag: continue
            if not resource in SourceImageSet:
                #assert u"评分.png" != resource
                print "remove", resource, filemap[resource]
                os.remove(filemap[resource])
    print "--"

if __name__ == "__main__":
    if "clear" in sys.argv:
        checksource()
    if "check" in sys.argv or True:
        checkimagek()

    print sys.argv, "clear/check"

fpage = file(sys.argv[0], "rb").read()
fpage = "\n".join([line.strip() for line in fpage.split("\n") if re.findall("sys.argv[^\\[\\\"]", line)])
print "**" * 10
print fpage.strip()
print
