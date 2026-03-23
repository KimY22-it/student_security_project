def mask_email(email):
    at_index =  email.find('@')
    if at_index <= 2:
        return at_index * '*' + email[at_index:]

    return email[:2] + (at_index - 2) * '*' + email[at_index:]

def mask_phone(phone):
    return phone[:3] + (len(phone) - 5) * '*' + phone[-2:]

def mask_cccd(cccd):
    return cccd[:3] + (len(cccd) - 3) * '*'

def mask_address(address):
    at_index =  address.find(' ')
    return address[:at_index] + (len(address) - at_index) * '*'
    