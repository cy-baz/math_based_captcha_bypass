# Math capture bypass script

## Brief description
A tool to brute force a login page while solving math based captcha.
This tool accepts a variety of parameters to make it easier to be a flexible tool which can be customized on the go to bypass simple math based captcha on login pages.

## Requirements / Limitations
- This python program uses the following libraries:
 - Requests
 - argparse
- The equation needs to be in plain text on the web application
- The operator (i.e. +) needs to have a space before or after it for them to be separated
- The string used to identify the equation may not work properly if it is not unique (i.e. occurs more than once in the response)

## Quick Examples
- Specifying the login page, characters used after the equation is// specified, user and password files.
```sh
python3 math_based_captcha_bypass.py  -l http://TheVulnerableApplication/login -m "= ?" -u users.txt -p pass.txt
```
- Specifying the login page, characters after the equation, character offset start before the specified characters, user and pass file, parameter names for user, password and captcha request
```sh
python3 math_based_captcha_bypass.py  -l http://TheVulnerableApplication/login -m "= ?" -off 15 -u users.txt -p pass.txt -up username -pp password -cp captcha
```

## Parameters Overview
Some parameters are straightforward such as:
```py
-l : The URL to send the login request to
-u : The file with usernames in it (separated on each line)
-p : The file with passwords in it (separated on each line)
```
Then there are parameters used to declare the name of the parameters needed for the request:
```py
-up: Parameter name for the username value
-pp: Parameter name for the password value
-cp: Parameter name for the captcha value 
```
Finally, there are the parameters which tweak what the program looks for to help make sure the requests work as expected:
```py
-e: The error messsage which occurs when the username/password is incorrect
-m: The string that occurs AFTER the equation is mentioned
  - For example: if the equation is "6 + 6 = ?". "= ?" is what follows the equation that is needed
-off: The number of characters to look at before/after the string that is used to find the equation.
  - This one might take some trial and error as it should only pull out the equation (i.e. '6 + 4').
-d : Direction either 'before' or 'after' the specified string (-m) is used
  - By default, it is 'before'
```
