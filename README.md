Description
===========

Collectd plugin to send notifications to Slack.

Dependencies
============

pip install slackclient


Configuration
=============
First, you need to load python plugin.

```
<LoadPlugin python>
     Globals true
</LoadPlugin>
```

Then you can configure slack plugin like

```
<Plugin python>
	ModulePath "/home/cemg/projects/slack-plugin"
	Import "slack_plugin"

        <Module slack_plugin>
        		SlackToken   "SlackWebApiToken"
		        SlackChannel "YourChannelNameHere"
		        BotName   "CollectdBot"
        </Module>
</Plugin>
```

Note:
For token https://api.slack.com/docs/oauth-test-tokens

and to send notifications you need treshold plugin : https://collectd.org/documentation/manpages/collectd-threshold.5.shtml

For example:

```
LoadPlugin "threshold"
<Plugin "threshold">
  <Type "percent_bytes">
    Instance free
    WarningMin 40
    FailureMin 60
    DataSource "value"
  </Type>
</Plugin>

```

Example
=======

```
[2016-08-28 07:55:14] Notification is sent to slack... Severity =  FAILURE, Message = Host archlinux, plugin df (instance root) type percent_bytes (instance free): Data source "value" is currently 17.254183. That is below the failure threshold of 60.000000.

```
![](preview.png)

