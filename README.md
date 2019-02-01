# google-reminders-cli

This is a simple tool for creating Google reminders from the command line.
The only supported feature is creating a single reminder in a specified time and 
date, and is done interactively:

```
$ ./remind 
Enter reminder title: Create Github repository for google-reminders-cli
Enter time (yyyy:mm:dd HH:MM): 2019:02:01 14:00            
Reminder set successfully
```

Currently there is no official support for reminders in Google API, so instead this 
tool imitates a browser request.  
App API keys are provided in a separate file and you may either use them or change them with 
your own keys.
