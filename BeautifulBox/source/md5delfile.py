#encoding=utf8
import re, sys, os
import time, hashlib

def mkmd5fromfile(filename):
    fobj = open(filename, "rb")
    md5 = hashlib.new("md5")
    while True:
        fb = fobj.read(1024)
        if not fb:
            break
        md5.update(fb)
    fobj.close()
    return md5.hexdigest()

fmd5set = set()
fmd5map = {}
def removedup(fpath):
        
        if os.path.isfile(fpath):
                
                fmd5 = mkmd5fromfile(fpath)
                if fmd5 in fmd5set:
                        xxx = list(set(fpath.split("/"))^set(fmd5map[fmd5].split("/")))
                        xxx.sort()

                        print 
                        print fpath, fmd5map[fmd5]
                        print xxx
                        print list(set(fpath.split("/"))-set(fmd5map[fmd5].split("/")))
                        print list(set(fmd5map[fmd5].split("/"))-set(fpath.split("/")))
                        if fpath.find("zfiledir/")!=-1: os.remove(fpath)
                        if os.path.exists(fmd5map[fmd5]):
                                if fmd5map[fmd5].find("zfiledir/")!=-1: os.remove(fmd5map[fmd5])
                                
                else:
                        fmd5set.add(fmd5)
                        fmd5map[fmd5] = fpath
        if os.path.isdir(fpath):
                ldir = os.listdir(fpath)
                ldir.sort()
                for _dir in ldir:
                        _path = fpath + "/" + _dir
                        if _dir not in (".svn", "doc", "bin"):
                                removedup(_path)
                                        
if __name__ == "__main__":
        removedup(".")
        print "ok"
        os.system("@Pause")

fpage = file(sys.argv[0], "rb").read()
fpage = "\n".join([line.strip() for line in fpage.split("\n") if re.findall("sys.argv[^\\[\\\"]", line)])
print "**" * 10
print fpage.strip()
print
