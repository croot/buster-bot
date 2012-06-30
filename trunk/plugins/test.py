# -*- coding: utf-8 -*-

def hnd_test(type, source, parameters):
    reply(type, source, u'все путем')

register_command_handler(hnd_test, 'тест', ['все'], 0, 'Тестовая команда.Отвечает все путем', 'тест', ['тест'])
