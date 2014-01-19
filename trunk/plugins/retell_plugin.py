#===istalismanplugin===
# -*- coding: utf-8 -*-

RETELL = {}
RETELL_FILE = 'dynamic/retell.txt'
db_file(RETELL_FILE, dict)

def hnd_retell_msg(r, t, s, p):
        global RETELL
        global RETELL_FILE
        if not s[1] in GROUPCHATS or not p or not s[2]:
                return
        if len(p)>1000:
                return
        if not s[1] in RETELL:
                RETELL[s[1]]={}
        ss = p.split()
        
        if len(ss)>1 and len(ss[0])>=2 and ss[0][:-1] in GROUPCHATS[s[1]]:
                if not GROUPCHATS[s[1]][ss[0][:-1]]['ishere']:
                        p = s[2]+u' написал(а) вам: '+' '.join(ss[1:])
                        if not ss[0][:-1] in RETELL[s[1]].keys():
                                RETELL[s[1]][ss[0][:-1]]=[]
                        if len(RETELL[s[1]][ss[0][:-1]])>20: return
                        
                        RETELL[s[1]][ss[0][:-1]].append(p)
                        write_file(RETELL_FILE, str(RETELL))

register_message_handler(hnd_retell_msg)

def hnd_retell_join(g, n, r, a, cljid):
        if g in RETELL.keys():
                if n in RETELL[g].keys():
                        msg(cljid, g+'/'+n, '\n'.join(RETELL[g][n]))
                        del RETELL[g][n]
                        write_file(RETELL_FILE, str(RETELL))

register_join_handler(hnd_retell_join)

