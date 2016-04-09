import core.Time_lib
import core.Config
import core.Logs as logs

logs.add_log("Program started.")
core.Config.load_config()
i = 2
while i != 5000000:
    i += 1
logs.add_log("Program finished. Time: " + core.Time_lib.time_from_start())