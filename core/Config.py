"""
    Config.py
    Загрузчик конфигурации
"""
import configparser
import core.Logs as Logs
import os.path

CONFIG_FILE_NAME = "core/config.ini"
# Секция в ini файле из которой будут взяты параметры
USED_SECTION = "Default"
SEPARATOR = "\n-------------------------\n"


def exist(file):
    return os.path.exists(file)


def load_config():
    Logs.add_log("Loading config.")
    cfg = configparser.ConfigParser()
    cfg['Default'] = {'xml_file_name': 'Posts.xml',
                      'css_file_name': 'style.css',
                      'css': 'true',
                      'minimal_frequency': 5,
                      'output_limit': 100,
                      'title': 'Main'}
    cfg['Params'] = {}
    config = cfg['Default']
    params = cfg['Params']
    try:
        if not cfg.read(CONFIG_FILE_NAME, encoding='utf-8'):
            Logs.add_log('Configuration file not found.')
        section = USED_SECTION
        if not (section in cfg):
            section = 'Default'
    except configparser.ParsingError:
        Logs.add_log('Invalid configuration file.')
        section = 'Default'

    for key in cfg['Default']:
        if not (key in cfg[section]):
            cfg[section][key] = cfg['Default'][key]
    try:
        config = dict(cfg[section])
        params = dict(cfg['Params'])
    except:
        Logs.add_log('Configuration file is broken. Aborted.')
        exit(1)
    if not exist(config['xml_file_name']):
        Logs.add_log('Xml file not found. Aborted.')
        exit(1)
    if config['css'] == 'True':
        if not exist(config['css_file_name']):
            Logs.add_log("Css file not found.")
            config['css'] = False
        else:
            config['css'] = True
            config['style'] = open(config['css_file_name'], 'r').read()
    Logs.add_log('Configuration loaded.')
    return [config, params]
