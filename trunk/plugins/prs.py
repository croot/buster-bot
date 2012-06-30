# -*- coding: utf-8 -*-

def hnd_prs_access(groupchat, nick, aff, role, cljid):
    if not groupchat in GROUPCHATS:
        return
    jid = get_true_jid(groupchat+'/'+nick)
    if jid in GLOBACCESS:
        return
    acc_aff, acc_role = 0, 0
    if role in ROLES:
        acc_role = ROLES[role]
    else:
        acc_role = 0
    if aff in AFFILIATIONS:
        acc_aff = AFFILIATIONS[aff]
    else:
        acc_aff = 0
    access = acc_aff+acc_role
    global ACCBYCONF
    try: level = int(access)
    except: level = 1
    if not ACCBYCONF.has_key(groupchat):
        ACCBYCONF[groupchat] = {}
    if not ACCBYCONF[groupchat].has_key(jid):
        ACCBYCONF[groupchat][jid]=jid
        ACCBYCONF[groupchat][jid]=level 
			

def check_s2s(cljid):
    db=eval(read_file('dynamic/chatroom.list'))
    if cljid in db.keys() and db[cljid]:
        for gch in db[cljid].keys():
            packet = IQ(CLIENTS[cljid], 'get')
            packet.addElement('query', 'jabber:iq:version')
            packet.addCallback(s2s_result_handler, gch, cljid)
            reactor.callFromThread(packet.send, gch+'/'+get_bot_nick(gch))
    reactor.callLater(480, check_s2s, cljid)

def s2s_result_handler(gch, cljid, x):
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if not ' '.join(code) in ['405']:
            threading.Timer(60, join(gch, get_bot_nick(gch), cljid))

register_stage0_init(check_s2s)
register_join_handler(hnd_prs_access)
