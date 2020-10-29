# twitch-notifications

This script uses the [Twitch API][0] to check for channels that recently went live and send notifications to any services supported by [apprise][1].  Some examples include Discord, Slack and Twilio.  See the [apprise wiki][2] for a full list and configuration information.

## Setup and useage

- Download or clone this repository. 
- Install the [apprise][1] Python module.
- Copy `config-example.yml` to `config.yml`
- Edit `config.yml`
- Test `twitch-notifications.py`
- Set up systemd timer or cronjob

## Troubleshooting

To verify apprise syntax is correct use the `apprise` [cli application][3].  The service wiki page will give good examples, like [Discord][4].

Temporally increasing the offset value in `config.yml` to something like 600 can also be handy when troubleshooting.


[0]: https://dev.twitch.tv/
[1]: https://github.com/caronc/apprise
[2]: https://github.com/caronc/apprise/wiki
[3]: https://github.com/caronc/apprise#command-line
[4]: https://github.com/caronc/apprise/wiki/Notify_discord#example
