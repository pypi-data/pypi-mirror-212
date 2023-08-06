import sys
import keyring
import json
from json.decoder import JSONDecodeError
import maskpass

MAX_FRAGMENTS = 10
FRAGMENT_SIZE = 1280

def get_secret(system_instance, user):
    ##set_password example
    ##keyring.set_password("coupa-test", "get_document", {secret}}
    ##retrieve password example
    ##keyring.get_password("coupa-test", "get_document")

    #where user will be username (get_document) and system_instance will be system (coupa-test)

    return_password = keyring.get_password(system_instance, user)
    if return_password:
        try:
            return json.loads(return_password)
        except JSONDecodeError:
            count = 1
            while count < MAX_FRAGMENTS:
                user_with_suffix = f"{user}_{count}"
                password_fragment = keyring.get_password(system_instance, user_with_suffix)
                count += 1
                if not password_fragment:
                    break
                else:
                    return_password = return_password + password_fragment
            try:
                return json.loads(return_password)
            except JSONDecodeError:
                input(f"Found password fragments for type {user} and up to fragment {user_with_suffix} (windows based) but still couldn't load JSON object. Likely malformed credential - try deleting the system/user secret and refreshing. Press enter to exit.")
                sys.exit() #hard error - this shouldn't run as it's a malformed secret
                
    else:   
        return None #no password stored - return None for refreshing of token/cred if required

def print_secret(system, user):
    print(get_secret(system, user))

def delete_secret(system, user):
    try:
        keyring.delete_password(system, user)
        user_list = [f"{user}_{x}" for x in range(1, MAX_FRAGMENTS + 1)]
        delete_secret_fragments(system, user_list)

    except keyring.errors.PasswordDeleteError:
        input(f"Couldn't delete secret for system {system} and user {user}. Press enter to exit")
        sys.exit()

def delete_secret_fragments(system, user_list):
    for user in user_list:
        try:
            keyring.delete_password(system, user)
        except keyring.errors.PasswordDeleteError:
            pass #probably doesn't exist

def write_secret(system, user, secret):
    secret = json.dumps(secret)

    secret_len = len(secret)
    try:
        keyring.set_password(system, user, secret)
        user_list = [f"{user}_{x}" for x in range(1, MAX_FRAGMENTS + 1)]
        delete_secret_fragments(system, user_list)
        print(f"Successfully stored secret for system {system} and user {user}.")
    except: #this is likely windows dying with a secret that's too long
        print(f"Got OSError - resorting to fragments")
        char_count = 0
        try:

            secret_fragment = secret[:FRAGMENT_SIZE]
            secret = secret[FRAGMENT_SIZE:]
            keyring.set_password(system, user, secret_fragment)
            char_count += len(secret_fragment)
            count = 1
        except:
            input(f"Got an error writing secret whilst trying to fragment first secret - likely a value/permission error. Contact script author and press enter to exit.")
            sys.exit()

        while count < MAX_FRAGMENTS: #got here so successfully stored initial fragment

            secret_fragment = secret[:FRAGMENT_SIZE]
            secret = secret[FRAGMENT_SIZE:]
            user_with_suffix = f"{user}_{count}"
            try:
                keyring.set_password(system, user_with_suffix, secret_fragment)
                char_count += len(secret_fragment)
                count += 1
            except:
                input(f"Got an error writing secret whilst trying to user {user} fragment on count {count} - likely a value/permission error. Contact script author and press enter to exit.")
                sys.exit()
            if len(secret) == 0:
                user_list = [f"{user}_{x}" for x in range(count, MAX_FRAGMENTS + 1)]
                delete_secret_fragments(system, user_list)
                print(f"Successfully stored secret for system {system} and user {user} with {count} fragments")
                print(f"Length of original secret = {secret_len} and length of fragments = {char_count}")
                break

def get_user():
    while True:
        user = input("Enter the reference (username equivalent i.e. get_document) for the script to store the key: ").strip()
        if len(user) < 5:
            print("Invalid username - should be more than 5 chars")
        else:
            return user
    
def get_url():
    x = input("Enter a URL (if applicable - otherwise leave blank): ").strip()
    if x == "":
        return None
    else:
        return x

def get_oauth_url():
    x = input("Enter an OAUTH URL (if applicable - otherwise leave blank): ").strip()
    if x == "":
        return None
    else:
        return x

def get_system_instance():
    instance = get_instance()
    return instance["system"]

def get_instance():
    opts = {
        "1": {"name": "Coupa Sandbox", "system": "coupa-sandbox", "url": "https://monash-sandbox.coupahost.com/api", "oauth_url": "https://monash-sandbox.coupahost.com/oauth2"},
        "2": {"name": "Coupa Test", "system": "coupa-test", "url": "https://monash-test.coupahost.com/api", "oauth_url": "https://monash-test.coupahost.com/oauth2"},
        "3": {"name": "Coupa Production", "system": "coupa-production", "url": "https://monash.coupahost.com/api", "oauth_url": "https://monash.coupahost.com/oauth2"},
        "4": {"name": "Other", "system": None, "url": None, "oauth_url": None}
    }
    
    print("Select system below")
    for k, v in opts.items():
        print(f"{k}: {v['name']}")

    while True:
        x = input("Enter value: ")

        if x in opts:
            system_instance = opts[x]["system"]
            break
        else:
            print("Invalid option selected")

    if not system_instance:
        while True:
            opts[x]["system"] = input("Please enter the system to be stored ('e.g. magento-production'): ")
            if opts[x]["system"]:
                break
            
    return opts[x]

def prompt_secret():
    while True:
        password = maskpass.askpass("Enter the api_key / client_secret: ")
        password = password.strip()

        if len(password) > 8:
            return password
        else:
            print("Password appears too short. Please check you copied correctly")    



if __name__ == '__main__':
    menu = {
        "1": "Print secret",
        "2": "Write secret",
        "3": "Delete secret"
        }

    print("Menu")
    for k,v in menu.items():
        print(f"{k}: {v}")
    
    while True:
        opt = input("Select an option: ")
        if opt not in menu:
            print("Invalid option selected")
        else:
            break

    if opt == "1":
        system_instance = get_system_instance()
        user = get_user()
        print_secret(system_instance, user)

    if opt == "2":
        instance = get_instance()
        print(f"Received instance: {instance}")
        user = get_user()
        if not instance["url"]:
            instance["url"] = get_url()
        elif not instance["oauth_url"]:
            instance["oauth_url"] = get_oauth_url
        
        password = prompt_secret()
        secret = {"url": instance["url"], "oauth_url": instance["oauth_url"], "secret": password}
        write_secret(instance["system"], user, secret)

    if opt == "3":
        system_instance = get_system_instance()
        user = get_user()
        delete_secret(system_instance, user)
        print("Successfully deleted secret")


    input("Press enter to exit")
