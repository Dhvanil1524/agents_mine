import requests
import json

# ================= CONFIGURATION =================
VTIGER_URL = "https://granimals1.od2.vtiger.com/webservice.php"
USERNAME = "dhvanil.prajapati@granimals.com"
ACCESS_KEY = "WY28fQy2zefMPxl"  # usually from Vtiger CRM
# ==================================================

def get_challenge():
    """Get the challenge token from Vtiger"""
    params = {"operation": "getchallenge", "username": USERNAME}
    resp = requests.get(VTIGER_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data["success"]:
        return data["result"]["token"]
    else:
        raise Exception(f"Challenge failed: {data}")

def login(token):
    """Login and get sessionName"""
    import hashlib
    key = hashlib.md5((token + ACCESS_KEY).encode()).hexdigest()
    params = {
        "operation": "login",
        "username": USERNAME,
        "accessKey": key
    }
    resp = requests.get(VTIGER_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data["success"]:
        return data["result"]["sessionName"]
    else:
        raise Exception(f"Login failed: {data}")

def lookup(session_name, search_type, value, search_in):
    """
    Perform a lookup on Vtiger
    search_type: 'phone' or 'email'
    value: the phone/email value
    search_in: dictionary like {"Contacts":["mobile","phone"]}
    """
    params = {
        "operation": "lookup",
        "sessionName": session_name,
        "type": search_type,
        "value": value,
        "searchIn": json.dumps(search_in)  # auto JSON encode
    }
    resp = requests.get(VTIGER_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def main():
    phone_number = input("Enter phone number to lookup: ")
    try:
        token = get_challenge()
        session = login(token)
        # Example: search only Contacts module fields 'mobile' and 'phone'
        search_in = {"Contacts": ["mobile", "phone"]}
        result = lookup(session, "phone", phone_number, search_in)
        print(json.dumps(result, indent=2))
        # Save to file if needed
        with open("vtiger_lookup.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            print("Saved to vtiger_lookup.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
