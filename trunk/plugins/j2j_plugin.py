# -*- coding: utf-8 -*-

JEY_JEY = 0

def j2j_presence_send(raw, t, s, p):
    global JEY_JEY
    if J2J:
        if not JEY_JEY:
            JEY_JEY=time.time()
        else:
            if time.time()-JEY_JEY>500:
                JEY_JEY=time.time()
            else:
                return
        p = domish.Element(('jabber:client', 'presence'))
        p['to'] = J2J
        reactor.callFromThread(dd, p)

register_message_handler(j2j_presence_send)
