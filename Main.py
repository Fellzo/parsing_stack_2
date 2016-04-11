import core.Logs as Logs
import core.Parser as Parser
import core.Time_lib as Time_lib
import core.Config as Config
import core.Html_writer as Html


output_data = {}
Logs.add_log(Config.SEPARATOR + "Program started.")
configs = Config.load_config()
output_data[configs[0]['prefix']] = Parser.parse(configs[1], configs[0])    # Сохранение данных для каждого сайта
Html.write_html(output_data[configs[0]['prefix']], configs[0])
Logs.add_log("Program finished. Time: " + Time_lib.time_from_start() + Config.SEPARATOR)
