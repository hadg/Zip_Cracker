#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import zipfile
import sys
import optparse
out=sys.stdout
n1=0
n2=0
def createdict(min,max):
    if(min<=0):
        raise ValueError("The minimum password length must be greater than 0")
    if(max<min):
        raise ValueError("The maximum length must be greater than the minimum password length")
    password_dict=[]
    for i in range(min-1,max):
        o_dict=[chr(c) for c in range(ord('a'),ord('z')+1)]
        o_dict.extend([str(c) for c in range(0,10)])
        n=i
        p_dict=o_dict
        if(n!=0):
            while n>0:
                p_dict=[c+o for c in p_dict for o in o_dict]
                n-=1
        password_dict.extend(p_dict)
    return password_dict
def extractfile(zfile,password):
    global out,n1,n2
    n2+=1
    out.write("\rCompleted(%s/%s)"%(n2,n1))
    out.flush()
    try:
        zfile.extractall(pwd=password)
        print "\nFound Password:"+password
        sys.exit(0)
    except Exception:
        pass
def main():
    parser=optparse.OptionParser('usage: %s [options]'%sys.argv[0])
    parser.add_option('-f',dest='zname',type='string',help="specify zip file")
    parser.add_option('-d',dest='dname',type='string',help="specify dictitonary file")
    parser.add_option('--max',dest='max',type='int',help="password maximum length")
    parser.add_option('--min',dest='min',type='int',help="password minimum length")
    options,argvs =parser.parse_args()
    if(options.dname==None):
        options.dname="d:/dict.txt"
    if(options.zname==None and (options.max==None or options.min==None)):
        print parser.usage
        sys.exit(0)
    elif(options.zname!=None):#crack
        print options
        zname=options.zname
        print zname
        dname=options.dname
        zfile=zipfile.ZipFile(zname)
        dfile=open(dname,'r')
        global n1
        lines=dfile.readlines()
        n1=len(lines)
        for line in lines:
            password=line.strip('\n')
            #t=threading.Thread(target=extractfile,args=(zfile,password,t))
            #t.start()
            extractfile(zfile,password)
    elif(options.min!=None and options.max!=None):
        password_dict=createdict(options.min,options.max)
        d_file=open(options.dname,'w')
        try:
                for c in password_dict:
                    d_file.write(c+'\n')
        except:
            pass
        d_file.close()
        print "[+]write dict file %s done!"%options.dname
if __name__=='__main__':
    main()