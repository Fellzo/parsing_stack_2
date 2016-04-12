"""
    Html_writer.py
    Генерация html кода
"""

import core.Logs as Logs

"""
    Формирует строку вида <%tag_name% attrs>content</%tag_name%>
"""


def make_tag(tag, contain, attrib=""):
    return "<%s %s>\n%s\n</%s>\n" % (tag, attrib, contain, tag)


def write_html(output_data, configs):
    Logs.add_log("Html generation started.")
    output_sorted = []
    sort = sorted(output_data, key=lambda x: output_data[x]) # Сортировка по количеству содержательных тегов
    sort = sort[::-1]
    for post in sort:  # Создание списка для вывода постов
        output_sorted.append((post, output_data[post]))

    html = open(configs["output_file_name"], "w")  # файл с версткой
    link = "http://%s.stackexchange.com/questions/" % configs["prefix"]
    limit = min(int(configs["output_limit"]), len(output_sorted))  # Кол-во выводимых постов

    # Заголовок и шапка таблицы
    out = make_tag("h2", "Parsing site: %s" % configs["prefix"] + ".stackexchange.com")
    out += make_tag("tr", make_tag("td", "#") + make_tag("td", "Id") +
                    make_tag("td", "Links") + make_tag("td", "Meaningful tags"))

    # Генерации таблицы
    for i in range(limit):
        post_link = (link + "%s/") % output_sorted[i][0]    # Ссылка на пост
        # Генерация строки таблицы вида Номер Id Link Кол-во содержательный тегов в посте
        content = make_tag("td", str(i + 1)) + make_tag("td", output_sorted[i][0])
        content += make_tag("td", make_tag("a", "Link", attrib="href='%s' target='_blank'" % post_link))
        content += make_tag("td", str(output_sorted[i][1]))
        out += make_tag("tr", content)   # строка таблицы с информацией о посте

    out = make_tag("table", out, attrib="class='bordered'")     # Добавление тега таблицы
    out = make_tag("body", out)     # Обертка таблицы в тег body

    # Генерация стилей
    css = ""
    if configs["css"]:  # Если css включен в настройках проверяется способ привязки к файлу
        if configs["css_type"] == "inline":
            css = make_tag("style", configs['style'])
        else:
            css = make_tag("link", "", attrib="type='text/css' rel='stylesheet' href='%s'" % configs['css_file_name'])

    # Генерация содержания head тега
    head = make_tag("head", make_tag("meta", "", attrib="charset='utf-8'") + make_tag("title", configs["title"]) + css)
    out = make_tag("html", (head + out).replace("\n\n", "\n"))

    # Вывод и логгирование
    html.writelines(out)
    Logs.add_log("Html generation finished.")
