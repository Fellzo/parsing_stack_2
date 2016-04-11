"""
    Html_writer.py
    Генерация html кода
"""
import core.Logs as Logs


def make_tag(tag, contain, attrib=""):
    return "<%s %s>\n%s\n</%s>\n" % (tag, attrib, contain, tag)


def write_html(output_data, configs):
    Logs.add_log("Html generation started.")
    output_sorted = []
    sort = sorted(output_data, key=lambda x: output_data[x])[::-1]  # Сортировка по количеству содержательных тегов
    for post in sort:  # Создание списка для вывода постов
        output_sorted.append((post, output_data[post]))
    html = open(configs["output_file_name"], "w")
    link = "http://%s.stackexchange.com/questions/" % configs["prefix"]
    limit = min(int(configs['output_limit']), len(output_sorted))
    out = make_tag("h2", "Parsing site: %s" % configs["prefix"] + ".stackexchange.com")
    out += make_tag("tr", make_tag("td", "#") + make_tag("td", "Links") + make_tag("td", "Meaningful tags"))  # Верстка
    for i in range(limit):
        post_link = (link + "%s/") % output_sorted[i][0]
        out += make_tag("tr", make_tag("td", str(i + 1)) + make_tag("td", make_tag("a", "Link",
                                                                                   attrib="href='%s' target='_blank'" % post_link)) + make_tag(
            "td", str(
                output_sorted[i][1])))
    out = make_tag("table", out, attrib="class='bordered'")
    out = make_tag("body", out)
    css = ""
    if configs["css"]:
        if configs["css_type"] == "inline":
            css = make_tag("style", configs['style'])
        else:
            css = make_tag("link", "", attrib="type='text/css' rel='stylesheet' href='%s'" % configs['css_file_name'])
    head = make_tag("head", make_tag("meta", "", attrib="charset='utf-8'") + make_tag("title", configs['title']) + css)
    out = make_tag("html", (head + out).replace("\n\n", "\n"))
    html.writelines(out)
    Logs.add_log("Html generation finished.")
