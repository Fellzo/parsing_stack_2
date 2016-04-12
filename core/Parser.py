"""
    Parser.py
    Парсер xml файла
"""

from lxml import etree
import core.Logs as Logs

interesting_posts = []
posts = []
meaningful_tags = {}

"""
    Проверка значения из поста по условию в конфигурации
"""


# compare_value - значение аттрибута от тега, value - значение из конфигурационных параметров
def check_value(compare_value, value, operator):
    try:
        compare_value = int(compare_value)
        value = int(value)
    except ValueError:
        Logs.add_log("Bad parameter.")
        exit("Check configuration file. All parameters values must be int.")
    if operator == "==":
        if value != compare_value:
            return False
    if operator == "!=":
        if value == compare_value:
            return False
    if operator == ">":
        if compare_value < value:
            return False
    if operator == "<":
        if compare_value > value:
            return False
    return True


"""
    Проверка поста на соответсвие входным настройкам
"""


def check_post(post_attr, params):
    post = {}
    for key in post_attr:
        post[key.lower()] = post_attr[key]

    for param in params:
        val, operator = params[param].split("&&")
        if not (param in post):
            return False
        if operator == "+":
            if not (param in post):
                return False
            elif operator == "-" and param in post:
                return False
        else:
            if not check_value(post[param], val, operator):
                return False
    return True


"""
    Получение списка тегов из строки вида <tag1><tag2><tag3>
"""


def parse_tag_string(tag_string):
    tags_list = tag_string.split("><")
    for i in range(len(tags_list)):
        # разворачивает что бы вырезать только последнюю >
        tags_list[i] = tags_list[i].replace("<", "", 1)[::-1]
        # возвращает строку в исходный вид
        tags_list[i] = tags_list[i].replace(">", "", 1)[::-1]
    return tags_list


"""
    Выборка содержательных тегов
"""


def filter_tags(minimal_frequency):
    try:
        bad_tags = []
        minimal_frequency = int(minimal_frequency)
        for tag in meaningful_tags:
            if meaningful_tags[tag] < minimal_frequency:
                bad_tags.append(tag)
        for tag in bad_tags:
            meaningful_tags.pop(tag)
    except ValueError:
        Logs.add_log("Bad frequency value. Aborting")
        exit("Bad frequency value. Check config file")


"""
    Очистка лишних данных после парсинга очередного сайта.
"""


def clear_data():
    global meaningful_tags
    meaningful_tags = {}
    global posts
    posts = []
    global interesting_posts
    interesting_posts = []


"""
    Основная функция парсинга xml файла
"""


def parse(params, config):
    try:
        clear_data()
        Logs.add_log("Parsing %s start." % config["prefix"])
        tree = etree.fromstring(open(config["xml_file_name"], encoding="utf-8").read())
        for line in tree:
            # Выборка всех постов
            if line.attrib["PostTypeId"] == "1":
                posts.append(line.attrib)
        for post in posts:
            # Фильтрация постов
            if check_post(post, params):
                interesting_posts.append(post)
                for tag in parse_tag_string(post["Tags"]):
                    if tag in meaningful_tags:
                        meaningful_tags[tag] += 1
                    else:
                        meaningful_tags[tag] = 1
        output_posts = {}
        filter_tags(int(config["minimal_frequency"]))
        # Генерация отсчета вида key = Id val - количество содержательных тегов
        for post in interesting_posts:
            output_posts[post["Id"]] = 0
            for tag in parse_tag_string(post["Tags"]):
                if tag in meaningful_tags:
                    output_posts[post["Id"]] += 1

        Logs.add_log("Parsing finished. Total parsed lines: %d. Total number of interesting posts: %d. " % (
            len(tree), len(interesting_posts)) + "Total tags: %d." % len(meaningful_tags))
        filter_tags(config["minimal_frequency"])
        Logs.add_log("Meaningful tags: %d." % len(meaningful_tags))
        return output_posts
    except:
        Logs.add_log("Parsing error. Aborting.")
