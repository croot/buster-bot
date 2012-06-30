# -*- coding: utf-8 -*-

def handler_python_eval(type, source, parameters):
	try:
		return_value = str(eval(parameters))
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	reply(type, source, return_value)

def handler_python_exec(type, source, parameters):
	if '\n' in parameters and parameters[-1] != '\n':
		parameters += '\n'
	try:
		exec unicode(parameters) in globals()
	except:
		reply(type, source, str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1]))


def handler_python_sh(type, source, parameters):
	return_value=''
	if os.name=='posix':
		pipe = os.popen('sh -c "%s" 2>&1' % (parameters.encode('utf8')))
		return_value = pipe.read()
	elif os.name=='nt':
		pipe = os.popen('%s' % (parameters.encode('utf8')))
		return_value = pipe.read().decode('cp866')
	pipe.close
	reply(type, source, return_value)

register_command_handler(handler_python_eval, 'eval', ['суперадмин','все'], 100, 'Расчитывает и показывает заданное выражение питона.', 'eval <выражение>', ['eval 1+1'])
register_command_handler(handler_python_exec, 'exec', ['суперадмин','все'], 100, 'Выполняет выражение питона.', 'exec <выражение>', ['eval pass'])
register_command_handler(handler_python_sh, 'sh', ['суперадмин','все'], 100, 'Выполняет шелл команду.', 'sh <команда>', ['sh ls'])

	
