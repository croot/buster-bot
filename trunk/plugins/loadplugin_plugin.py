#===istalismanplugin===
# -*- coding: utf-8 -*-


def handler_pod_pl(type,source,parameters):
  if not parameters:
    return
  try:
    fp = 'plugins/' + parameters+'_plugin.py'
    i = handlers_load_checker(fp)
  except:
    fp = 'plugins/' + parameters+'.py'
    i = handlers_load_checker(fp)
  if i:
    for x in i:
      if x in globals().keys():
        del globals()[x]
  try:
    fp = file(fp)
    exec fp in globals()
    fp.close()
    reply(type,source,u'ok')
  except:
    reply(type,source,unicode(traceback.format_exc()))

def handlers_load_checker(fp):
  source = read_file(fp)
  list = re.findall('def (.*?)\(', source,  re.IGNORECASE)
  return list

register_command_handler(handler_pod_pl, 'load', ['все'], 99, 'load anywhere plugin', 'load <names plugin>', ['load admin'])

