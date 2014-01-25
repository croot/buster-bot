# -*- coding: utf-8 -*-

ANTIDUBL = {}

def antidublicat_prs(x, cljid):
        global ANTIDUBL
        try:
                fr = x['from']
                fr = fr.split('/')
        except: return
        if not fr[0] in GROUPCHATS:
                return
        if not fr[0] in ANTIDUBL:
                ANTIDUBL[fr[0]]={'t':time.time(),'c':cljid}
                return
        if ANTIDUBL[fr[0]]['c']!=cljid and time.time()-ANTIDUBL[fr[0]]['t']<1.2:
                db=eval(read_file('dynamic/chatroom.list'))
                for c in db.keys():
                        if fr[0] in db[c].keys():
                                leave(fr[0], 'confilct', (cljid if c!=cljid else ANTIDUBL[fr[0]]['c']))
        ANTIDUBL[fr[0]]={'t':time.time(),'c':cljid}

register_presence_handler(antidublicat_prs)
