import collectd
from pygtail import Pygtail
from slackclient import SlackClient
from pyparsing import Word, Suppress, Combine, nums, Regex

# Log Parser
class LogParser(object):
  def __init__(self):
    ints = Word(nums)
    year = Combine(ints + "-" + ints + "-" + ints)
    time  = Combine(ints + ":" + ints + ":" + ints)
    timestamp = Suppress("[") + year + time + Suppress("]")
    message = Regex(".*")
    self.__pattern = timestamp + message

  def parse(self, line):
    parsed_string = self.__pattern.parseString(line)
    parsed_message              = {}
    parsed_message["message"]   = parsed_string[2]

    return parsed_message

def read(data=None):
    n = collectd.Notification()

    n.host = "archlinux"
    n.plugin = "df"
    n.type_instance='free'
    n.type='percent_bytes'
    n.plugin_instance='root'

    if (n.severity == 0):
        n.severity = 0
    elif (n.severity == 1):
        n.severity = 1
    elif (n.severity == 2):
        n.severity = 3
    else:
        n.severity = 4

    parser = LogParser()

    token = "your token"
    sc = SlackClient(token)

    for line in Pygtail("/var/log/collectd.log"):
        if "FAILURE" in line:
            log = parser.parse(line)
            sc.api_call(
                "chat.postMessage", channel="#devops", text=log['message'],
                username='CollectdBot', icon_emoji=':robot_face:')
    # send to collectd
    n.dispatch()


collectd.register_read(read)

# example
# Notification: severity = FAILURE, host = archlinux, plugin = df, plugin_instance = root, type = percent_bytes,
# type_instance = free, message = Host archlinux, plugin df (instance root)
# type percent_bytes (instance free): Data source "value" is currently 34.819561. That is below the failure threshold of 60.000000.
