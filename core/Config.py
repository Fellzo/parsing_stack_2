"""
    Config.py
    Загрузчик конфигурации
"""


def load_config():
    """
        Функция загрузки параметров из конфигурационного файла
    """
    # Default значения конфигурации
    configs = {"Default": {"logs": True, "logs_file_name": "logs.txt", "xml_file_name": "Posts.xml"}, "Params": {}}
    section = "Default"
    try:
        # Читает данные
        cfg = open("config.ini", "r", encoding='utf-8').read()
        try:
            # Выделение подстроки с используемое секцией
            section = cfg[cfg.index("used_section"):].split('\n')[0]
            section = section.split(' = ')[1]
        except ValueError:
            section = "Default"

        cfg = cfg.split('\n')
        now = "Default"
        for line in cfg:
            line = line.strip()
            if len(line) == 0 or line[0] == ';':
                continue
            if line[0] == '[':
                now = line.strip('[').strip(']')
                # Инициализации новой секции
                configs[now] = {}
            else:
                try:
                    key, val = line.split(" = ", 1)
                    if key == "used_section":
                        continue
                    configs[now][key] = val
                except ValueError:
                    # Если параметр задан в направильном виде (например не задано значение)
                    print("Unknown parameter: ", line)
        # Если в конфигурационном файле отсутсвуте секция с параметрами
        if not (section in configs):
            configs[section] = configs['Default']
            print("Section", section, "is not find in configuration file")
        else:
            # Заполнение недостающих параметров
            for key in configs["Default"]:
                if not (key in configs[section]):
                    configs[section][key] = configs["Default"][key]

    except FileNotFoundError:
        print("Configuration file not found")
    # Возвращает список из конфигурации используемой секции и параметров для
    return [configs[section], configs["Params"]]


print(load_config()[0])
