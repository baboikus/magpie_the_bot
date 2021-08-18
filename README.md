# Attention. There is still some work to be done.

## And what is this bot for?
Magpie is telegram bot for team selfmanegement and effective collaboration

## Quickest start
You need python3 installed.

    $ pip install python-telegram-bot --upgrade
    $ git clone https://github.com/baboikus/magpie_the_bot.git
    $ cd magpie_the_bot
    $ touch TOKEN
    
Put your token key from telegram BotFather into new TOKEN file and then just run bot.py

    $ python bot.py

## Commands description
    /events  - show all important performers and tasks events.

    /daily_report  - show daily report describing probable risks and predictive analytics.

    /help  - show full description for complete list of commands.

    /backlog  - show current backlog.

    /task_add <task_id> [<tag1> ... <tagN>] - add task <task_id> with specific tags <tag1>, ... , <tagN> to current backlog.

    /task_start <task_id> - start new working session on the task <task_id>.

    /task_stop <task_id> - stop current working session on the task <task_id>.

    /tag_add <task_id> [<tag1> ... <tagN>] - add set of tags <tag1>, ... , <tagN> to task <task_id>.

## FAQ
tbd
