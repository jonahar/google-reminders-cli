# google-reminders-cli

**google-reminders-cli** is a simple tool for interacting with _Google reminders_ from the command line.
It allows creating, deleting and watching reminders

Run with `-h` to see all supported actions, acceptable time formats, etc.

On the first run, a consent screen will open in the browser to aquire permission 
to access the user's reminders.

App API keys are provided in a separate file, so you may either use them or easily change 
them with your own keys.


## Usage examples
Create a reminder interactively:
```
$ python3 remind.py -i
What's the reminder: Pay bills
When do you want to be reminded: tomorrow at 4pm

"Pay bills" on Sun, Jun 02 2019, 16:00

Do you want to save this? [Y/n] y
Reminder set successfully:
2019-06-02 16:00: Pay bills ; id="cli-reminder-1559389411.7416472"
```

or using command line arguments:
```
$ python3 remind.py -c "Pay bills" "tomorrow 17:45"
Reminder set successfully:
2019-06-02 17:45: Pay bills ; id="cli-reminder-1559389443.0839736"
```


**Disclaimer**: Currently there is no official API for _Google Reminders_, so instead, 
this tool imitates a browser request. This may cause google-reminders-cli to stop 
function correctly at any time.
