from sorare.utils import sorare_authenticate

email = "baptiste_poirier@yahoo.fr"
with open(r"C:\Users\bapti\Documents\sorare-ml\docs\const.txt", encoding="UTF-8") as f:
    lines = f.readlines()
pwd = lines[0]
two_fa_code = input("Enter 2FA code : ")


token_graphQL = sorare_authenticate(email, pwd, two_fa_code)
print(token_graphQL)