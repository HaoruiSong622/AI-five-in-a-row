spreadLimit = 1
searchdeep = 2
countlimit = 20
star = False
cache = True
ONE = 10
TWO = 100
THREE = 1000
FOUR = 100000
FIVE = 10000000
BLOCKED_ONE = 1
BLOCKED_TWO = 10
BLOCKED_THREE = 100
BLOCKED_FOUR = 10000

com = 1  # role
hum = 2  # role
empty = 0  # role
# this line is done on my ipad.

def reverse(role):
    if role == com:
        return hum
    return com
