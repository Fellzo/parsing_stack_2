"""
    Config.py
    Загрузчик конфигурации
"""
import configparser
import core.Logs as logs

CONFIG_FILE_NAME = "core/config.ini"
# Секция в ini файле из которой будут взяты параметры
USED_SECTION = "Default"


def load_config():
    cfg = configparser.ConfigParser()
    cfg['Default'] = {"xml_file_name": "Posts.xml",
                      "css_file_name": "style.css"}
    cfg['Params'] = {"Id": "1&&=="}

    try:
        if not cfg.read(CONFIG_FILE_NAME, encoding='utf-8'):
            logs.add_log("Configuration file not found.")
        section = USED_SECTION
        if not (section in cfg):
            section = 'Default'
    except configparser.ParsingError:
        logs.add_log('Invalid configuration file.')
        section = 'Default'

    for key in cfg['Default']:
        if not (key in cfg[section]):
            cfg[section][key] = cfg['Default'][key]
    try:
        config = dict(cfg[section])
        params = dict(cfg['Params'])
    except:
        logs.add_log('Configuration file are broken. Aborted.')
        exit(-1)
    return [config, params]
