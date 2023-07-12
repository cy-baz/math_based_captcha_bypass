# Math capture bypass script

## Brief description
A tool to brute force a login page while solving math based captcha.
This tool accepts a variety of parameters to make it easier to be a flexible tool which can be customized on the go to bypass simple math based captcha on login pages.

## Requirements / Limitations
- This python program uses the following libraries:
 - Requests
 - argparse
- The equation needs to be in plain text on the web application
- The operator (i.e. +) needs to have a space before or after it for them to be separated.
  - If not, they could probably be separated in the arithmetic() function.
- The string used to identify the equation may not work properly if it is not unique (i.e. occurs more than once in the response)
- The script doesn't check if it is a login page, so wrong urls may cause unusual output.

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
Additionally, there are parameters that help check if the payloads, math and responses are as expected:
```py
-vP: See the payload  used for each brute forcing attempt. This can help see if the credentials and captcha work as expected
-vR: Recieve the response after each bruteforcing attempt. This helps see if the bypass is working (in some cases).
-vM: See what is being interpreted as the equation. If this is wrong, the captcha will not be right. This cab be used to see if the combination of '-m', '-off' and '-d' have found the correct part of the page with the equation.
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
### Example about the parameters that tweak what to look for
- Let's say you have the following line
  ```Please solve: 136 - 64 = ?'''
- In this case the string before and after the equation we need (136 - 64) is unique and only occurs once
- Therefore you the command can be something like
```sh
# Finding the equation before the provided string ( " = ?")
python3 math_based_captcha_bypass.py  -l http://TheVulnerableApplication/login -m " = ?" -off 9

# Finding the equation after the provided string ("Please solve:")
python3 math_based_captcha_bypass.py  -l http://TheVulnerableApplication/login -m "Please solve:" -off 9 -d after
```


