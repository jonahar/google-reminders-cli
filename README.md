# google-reminders-cli

This is a simple tool for creating Google reminders from the command line.
The only supported feature is creating a single reminder in a specified time and 
date, and is done interactively:

```
$ ./remind 
What's the reminder: Pay bills
When do you want to be reminded: tomorrow at 4pm

"Pay bills" on Fri, May 10 2019, 16:00

Do you want to save this? [Y/n] y
Reminder set successfully
```

Run `remind -h` to see additional acceptable time formats

On the first run, a consent screen will open in the browser to aquire permission to access the user's reminders.

Currently there is no official support for reminders in Google API, so instead, this 
tool imitates a browser request.  
App API keys are provided in a separate file and you may either use them or change them with 
your own keys.
