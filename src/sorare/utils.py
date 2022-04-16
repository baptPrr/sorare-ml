from requests import get as get
from requests import post as post
import json
import bcrypt


def sorare_authenticate(email, pwd, two_fa_code):
    r = get(f'https://api.sorare.com/api/v1/users/{email}')
    response = json.loads(r.content)

    # get salt and hash with password
    salt = response['salt'].encode('utf8')
    
    pwrd = pwd.encode('utf8')
    hashed = bcrypt.hashpw(pwrd, salt).decode('utf8')


    # get csfr
    csrf = r.headers["CSRF-TOKEN"]
    headers = {
        "x-csrf-token": csrf
    }

    
# # login
    url = 'https://api.sorare.com/graphql'
    login_query = """
    mutation SignInMutation($input: signInInput!) {
    signIn(input: $input) {
        currentUser {
        slug
        jwtToken (aud: \"sorareml-baptPrr\") { token expiredAt }
        __typename
        }
        otpSessionChallenge
        errors {
        path
        message
        __typename
        }
        __typename
    }
    }
    """
        
    variables = {
    "input": {
        "email": email,
        "password": hashed
    }
    }

    p = post(url, json={'query': login_query, 'OperationName': 'SignInMutation', 'variables': variables}, headers=headers)

    response = json.loads(p.content)
    otpSessionChallenge = response['data']['signIn']['otpSessionChallenge']
  

    variables = {
        "input": {
            "otpSessionChallenge": otpSessionChallenge,
            "otpAttempt": two_fa_code
        }
    }
    p = post(url, json={'query': login_query, 'OperationName': 'SignInMutation', 'variables': variables}, headers=headers)
    response = json.loads(p.content)
    token = response['data']['signIn']['currentUser']['jwtToken']['token']

    return token
    

# email = "my@email.com"

# r = get(f'https://api.sorare.com/api/v1/users/{email}')
# response = json.loads(r.content)

# # get salt and hash with password
# salt = response['salt'].encode('utf8')
# pwrd = "mypassword".encode('utf8')
# hashed = bcrypt.hashpw(pwrd, salt).decode('utf8')

# # get csfr
# csrf = r.headers["CSRF-TOKEN"]
# headers = {
#     "x-csrf-token": csrf
# }

# # login
# url = 'https://api.sorare.com/graphql'
# login_query = """
# mutation SignInMutation($input: signInInput!) {
#   signIn(input: $input) {
#     currentUser {
#       slug
#       __typename
#     }
#     otpSessionChallenge
#     errors {
#       path
#       message
#       __typename
#     }
#     __typename
#   }
# }
# """

# variables = {
#   "input": {
#     "email": email,
#     "password": hashed
#   }
# }

# p = post(url, json={'query': login_query, 'OperationName': 'SignInMutation', 'variables': variables}, headers=headers)