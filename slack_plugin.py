import collectd
from slackclient import SlackClient

slacktoken = None
slackchannel = None
botname = None

def config(conf):
    global slacktoken, slackchannel, botname

    for node in conf.children:
        key = node.key.lower()
        val = node.values[0]
        if key == 'slacktoken':
            slacktoken = val
        elif key == 'slackchannel':
            slackchannel = val
        elif key == 'botname':
            botname = val
        else:
            collectd.warning('Slack Plugin: Unknown config key: {0}'.format(key))
            continue

def send_slack(message):
    sc = SlackClient(slacktoken)
    sc.api_call("chat.postMessage", channel=slackchannel, text=message,username=botname, icon_emoji=':robot_face:')


def slack_notification(notification, data=None):
    message = notification.message
    if notification.severity == collectd.NOTIF_FAILURE:
        severity = 'FAILURE'
    elif notification.severity == collectd.NOTIF_WARNING:
        severity = 'WARNING'
    elif notification.severity == collectd.NOTIF_OKAY:
        severity = 'OKAY'
    else:
        severity = 'UNKNOWN'
    send_slack(message)
    collectd.info("Notification is sent to slack... Severity =  {0}, Message = {1}".format(severity,message))

collectd.register_config(config)
collectd.register_notification(slack_notification)


collectd.info("Slack plugin...LOADED")
