def mask_email(email):
    at_index =  email.find('@')
    if at_index <= 2:
        return at_index * '*' + email[at_index:]

    return email[:2] + (at_index - 2) * '*' + email[at_index:]

def mask_phone(phone):
    return phone[:3] + (len(phone) - 5) * '*' + phone[-2:]

def mask_cccd(cccd):
    return cccd[:3] + (len(cccd) - 5) * '*' + cccd[-2:]

def mask_address(address):
    if len(address) <= 6:
        return len(address) * '*'
    return address[:6] + (len(address) - 6) * '*'