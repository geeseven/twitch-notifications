# twitch-notifications

This script uses the [Twitch API][0] to check for channels that recently went live and send notifications to any services supported by [apprise][1].  Some examples include Discord, Slack and Twilio.  See the [apprise wiki][2] for a full list and configuration information.

## Example notification

Each service acts a little different as they have different features.  The script has been designed for a lowest common denominator so that important information will make to most/all services.  It will send the following:

```
title: "Twitch"
body: "channel is now streaming category."
```

If multiple channels start at about the same time, they will be grouped together.  Here is an example notification using the 'dbus://' service along with the [dunst][3] notification-daemon.

![notification](https://i.imgur.com/Cvb1tqS.png)

Here is the dunst configuration used for this example.

```dosini
[Twitch]
    summary = "Twitch"
    new_icon = /path/to/twitch-icon.png
    background = "#6441A4"
```

## Setup and usage

- Download or clone this repository. 
- Install the [apprise][1] Python module.
- Copy `config-example.yml` to `config.yml`
- Edit `config.yml`
- Test `twitch-notifications.py`
- Set up systemd timer or cronjob

## Troubleshooting

To verify apprise syntax is correct use the `apprise` [cli application][4].  The service wiki page will give good examples, like [Discord][5].

Temporally increasing the offset value in `config.yml` to something like 600 can also be handy when troubleshooting.


[0]: https://dev.twitch.tv/
[1]: https://github.com/caronc/apprise
[2]: https://github.com/caronc/apprise/wiki
[3]: https://dunst-project.org/
[4]: https://github.com/caronc/apprise#command-line
[5]: https://github.com/caronc/apprise/wiki/Notify_discord#example
