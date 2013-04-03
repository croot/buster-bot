#===istalismanplugin===
# -*- coding: utf-8 -*-

# by Evgеn (xmpp:allertvitter@conference.qip.ru)

import re,urllib

masteroff={}

z=''

def masteroff_urllib(type,source,params):
        a = urllib2.Request("http://masteroff.org/search.php", params)
        a.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
	h3 = urllib2.urlopen(a).read()
	#= urllib.urlopen("http://ma params).read()
	global z
	z=h3
	if h3.count('<td align=center><p style=')>=1:
		h1 = u'Результаты поиска:\nНомер\tИсполнитель\t\t\tПесня\t\t\tАльбом\n'
		k=h3.count('<td align=center><p style=')
		i=1
		if source[1] in masteroff:
			del masteroff[source[1]]
		if not source[1] in masteroff:
			masteroff[source[1]]={}
		while i <= k:
			od = re.search('<td align=center><p style=',h3)
			h3 = h3[od.end():]
			h2 = h3[:re.search('</a>',h3).start()]
			h2 = h2.split('>')
			h2 = h2[2]
			h2=unicode(h2,'windows-1251')
			h1=h1+str(i)+u'.  '+h2
			od = re.search('</td>',h3)
			h3 = h3[od.end():]
			h2 = h3[:re.search('</a>',h3).start()]
			h2 = h2.split('>')
			h4=h2[2].replace('<a href=', '').replace("'", '').strip()
			h2 = h2[3]
			h2=unicode(h2,'windows-1251')
			masteroff[source[1]][i]=h4
			h1=h1+u'\t'+h2
			od = re.search('</td>',h3)
			h3 = h3[od.end():]
			h2 = h3[:re.search('</a>',h3).start()]
			h2 = h2.split('>')
			h2 = h2[3]
			h2=unicode(h2,'windows-1251')
			h1=h1+u'\t'+h2+u'\n'
			i+=1
		reply(type,source, h1)
	else:
		reply(type,source, u'не найдено')

def open_masteroff(type,source,parameters):
	if not parameters:
		reply(type,source,u'я мысли читать не умею!')
		return
	w=parameters.strip().split(' ',1)
	if len(w)==1:
		params = urllib.urlencode({'q' : parameters[:100].encode('windows-1251')})
		masteroff_urllib(type,source,params)
	if len(w)>1:
		if w[0].strip().lower()==u'номер':
			if w[1].isdecimal() == True:
				w[1] = int(w[1])
				if w[1] in masteroff[source[1]]:
					h3 = urllib.urlopen(masteroff[source[1]][w[1]]).read()
					if h3.count('<td valign=')>=1:
						od = re.search("<p class='songttl'>",h3)
						h3 = h3[od.end():]
						h2 = h3[:re.search('</p>',h3).start()]
						h2=unicode(h2,'windows-1251')
						h1=h2+u'\n'
						od = re.search("<pre class='songtext'>",h3)
						h3 = h3[od.end():]
						h2 = h3[:re.search('</pre>',h3).start()]
						h2=unicode(h2,'windows-1251')
						h1=h1+h2
						reply(type,source, h1)
					else:
						reply(type,source, u'Видно сменили разметку на сайте')
				else:
					reply(type,source, u'Такого номера нет и вывести я ничего не могу')
			else: 
				reply(type,source, u'Пиши число, а не ерунду всякую')
		elif w[0].strip().lower()==u'исполнитель':
			rt=w[1]
			params = urllib.urlencode({'q' : rt[:100].encode('windows-1251'), 'where' : 'artist'})
			masteroff_urllib(type,source,params)
		elif w[0].strip().lower()==u'название':
			rt=w[1]
			params = urllib.urlencode({'q' : rt[:100].encode('windows-1251'), 'where' : 'song'})
			masteroff_urllib(type,source,params)
		elif w[0].strip().lower()==u'строка':
			rt=w[1]
			params = urllib.urlencode({'q' : rt[:100].encode('windows-1251'), 'where' : 'text'})
			masteroff_urllib(type,source,params)
		else:
			params = urllib.urlencode({'q' : parameters[:100].encode('windows-1251')})
			masteroff_urllib(type,source,params)

register_command_handler(open_masteroff, 'текст_песни', ['все'], 11, 'Показывает текст песни', '\nтекст_песни исполнитель Газманов - будет искать среди исполнителей Газманова\nтекст_песни название Паруса - будет искать Паруса в названии песен\nтекст_песни строка лёд - будет искать лёд в строках из песни\nтекст_песни Король и Шут - будет искать везде Король и Шут, т.е. в исполнителе, в названии песни и в строках из песни\nтекст_песни номер 1 - выдает текст песни из найденных под номером 1', ['текст_песни Газманов\n  >>  текст_песни Король и Шут\n  >>  текст_песни исполнитель Пугачева\n  >>  текст_песни название Мэри\n  >>  текст_песни строка лёд\n  >>  текст_песни номер 1'])
