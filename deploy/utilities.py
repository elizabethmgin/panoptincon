import datetime

sms = '@ mbarara university for 5'
sms2 = '@ makere uni comp sci dept for 2'
sms3 = '@ home'
sms4 = '@mbarara for 7'
sms5 = '@garden city for 9'
sms6 = '@unicef'
sms7 = '@unicef for 3'
sms8 = '@ garden city'
sms9 = 'garden city'

smstestlist = [sms,sms2,sms3,sms4,sms5,sms6,sms7,sms8,sms9]

safezones = ['home',
             'unicef',
             'makerere'
             ]

def showlocation(msg):
    if msg[0] == '@':
        #Checks if the string contains 'for', so we can do a datetime delta function.
        if 'for' in msg:
            if msg.split()[-2] == 'for':
                if msg[0:2] == '@ ':
                    return msg.split('for')[0].split('@')[1][1:-1]
                else:
                    return msg.split('for')[0].split('@')[1][0:-1]
            else:
                return "error"
        #These check for safe zones
        elif msg[1:] in safezones:
            return msg[1:]
        elif msg.split()[1] in safezones:
            return msg.split()[1]
        else:
            return "missing a time to return by"
    else:
        return "need an @ sign"

def showtime(msg):
    if 'for' in msg:
        return msg.split('for')[-1][1:]
    elif msg[1:] in safezones:
        return "at safezone: " + msg[1:]
    elif msg.split()[1] in safezones:
        return "at safezone: " + msg.split()[1]
    else:
        return "missing a time to return by"
    

def showtimeandloc(msg):
    if sms[0] == '@':
            return "location: " + showlocation(msg) + " back in: " + showtime(msg)
    else:
        return "need an @ sign"

def calcTime(msg):
    time = int(msg.split('for')[-1][1:])
    timeEntered = datetime.datetime.now()
    timeExpired = timeEntered + datetime.timedelta(hours=time)
    return timeExpired