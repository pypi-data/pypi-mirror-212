
===========
alert-wing
===========

alert-wing
===========
A Django app to send any exception to a Discord channel.

Introduction
------------
alert-wing is a Django app that allows you to send any exception to various apps, such as Discord. You can easily implement the functionality you need for each app.

Quick start
-----------

1. Add "alert-wing" to your `INSTALLED_APPS` setting in your Django project's settings file:

   .. code-block:: python

        INSTALLED_APPS = [
            ...,
            "alert-wing",
        ]

2. Set the `DISCORD_WEBHOOK_URL` variable in your Django settings. This is the URL of the Discord webhook you want to use for sending exceptions.

3. Use the `DiscordEmbedManager` class to create a Discord Embed object, and then use the `Discord` delivery method to send the exception to your Discord channel using the webhook.

Documentation
-------------

For detailed documentation and usage instructions, please refer to the "docs" directory.

Requirements
------------

- django ~= 4.1.5
- discord.py ~=2.2.3
- requests ~=2.28.2

License
-------

This project is licensed under the MIT License.

Contributing
------------

We welcome contributions! Please refer to the "CONTRIBUTING.md" file for more information.

Bug Reports and Feature Requests
--------------------------------

Please use the GitHub issue tracker to report any bugs or submit feature requests.

Authors
-------

- Mojtaba
- Email: Mojtabadavi14@gmail.com
