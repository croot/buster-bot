#===istalismanplugin===
# -*- coding: utf-8 -*-

import ftplib
import os

FTP_BD = 'dynamic/ftp_login.txt'

db_file(FTP_BD, dict)

GLOB_FTP = eval(read_file(FTP_BD))


def hnd_ftp(t, s, p):
        #0 host  1 login 2 pass 3 file 4 dir
        if not p:
                reply(t, s, u'и?')
                return
            
        global GLOB_FTP
        global FTP_BD
        
        z, jid, ss, cnt = None, get_true_jid(s), [], p.count(' ')
        
        if not jid in GLOB_FTP.keys():
            if cnt!=4:
                reply(t, s, u'Синтаксис: host login pass file dir')
                return
            ss = p.split()
        else:
            if cnt==4:
                ss = p.split()
            else:
                if cnt!=1:
                    reply(t, s, u'Укажите имя файла и директорию для загрузки на сервере через пробел!')
                    return
                key = GLOB_FTP[jid]
                ss = [key['host'],key['login'],key['pass'],p.split()[0],p.split()[1]]
        
        
        try: file = open(ss[3], 'rb')
        except:
                reply(t, s, u'Файл '+ss[3]+u' не найден!')
                return
    
        try: ftp = ftplib.FTP(host=ss[0], timeout=60)
        except ftplib.all_errors:
                reply(t, s, u'Нет коннекта с '+ss[0])
                return
        print dir(ftp)
        try: ftp.login(ss[1], ss[2])
        except ftplib.all_errors:
            reply(t, s, u'Проверьте логин и пароль!')
            ftp.quit()
            return
        try:
            ftp.cwd(ss[4])
            z = ftp.storbinary('STOR '+ss[3], file)
        except Exception as err:
            reply(t, s, err.message)
        if z:
                reply(t, s, u'Выполнено!')
        else:
                reply(t, s, u'Что-то пошло не так!')
        if hasattr(ftp,'quit'):
            try: ftp.quit()
            except: pass
        GLOB_FTP[jid]={'host':ss[0],'login':ss[1],'pass':ss[2]}
        write_file(FTP_BD, str(GLOB_FTP))

        
register_command_handler(hnd_ftp, 'ftp', ['фан','инфо','все'], 100, 'Передача файла по фтп. Синтаксис host login password file dir(on server). Вместо папки (dir) можно указать /. После первой закачки запоминает хост логин и пароль, далее можно указывать только имя файла и директорию для закачки.', 'ftp <host> <login> <pass> <file> <dir>', ['ftp ftp.gogi.net gogi 1234 pipec.jpg home'])
