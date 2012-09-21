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
sms10 = '@ art center for forever'
sms11 = '@ garden city for 26'
sms12 = '@ art center For 12'
sms13 = '@ art center 4 12'
sms14 = '@ art center 4 4'


smstestlist = [sms,sms2,sms3,sms4,sms5,sms6,sms7,sms8,sms9,sms10,sms11,sms12,sms13,sms14]

safezones = ['home',
             'unicef',
             'makerere'
             ]

def change4tofor(msg):
    if '4' in msg:
        newmsg = ' '.join(msg.split()[:-2]) + " " + msg.split()[-2].replace('4','for') + " " + msg.split()[-1]
        return newmsg
#    elif '4' in msg.split():
#        newmsg = ' '.join(msg.split()[:-2]) + 
#        return msg.split()[-2].replace('4','for')
    elif 'for' in msg.lower().split():
        return msg.lower()
    else:
        return msg.lower()

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
                return "Error: Unspecified"
        #These check for safe zones
        elif msg[1:] in safezones:
            return msg[1:]
        if msg[2:] in safezones:
            return msg[2:]
        elif msg[1:] not in safezones:
            return "Error: Not a recognized safe zone"
        elif msg.split()[1] in safezones:
            return msg.split()[1]
        else:
            return "Error: Missing a time to return by"
    else:
        return "Error: Need an @ sign"

def showtime(msg):
    if 'for' in msg.lower():
        try:
            if int(msg.lower().split('for')[-1][1:]) <= 24:
                return msg.lower().split('for')[-1][1:]
            elif int(msg.lower().split('for')[-1][1:]) > 24:
                return "Error: Please input a time 24 hours or less"
            elif msg.split()[1] in safezones:
                return "at safezone: " + msg.split()[1]
            else:
                return "Error: Unspecified"
        except:
            return "Error: Missing a time to return by"
    elif msg[1:] in safezones:
        return "at safezone: " + msg[1:]
    if msg[2:] in safezones:
        return "at safezone: " + msg[2:]
    else:
        return "Error: Missing a time to return by"
    

def showtimeandloc(msg):
    msg = change4tofor(msg)
    location = showlocation(msg)
    if location.split()[0] == "Error:":
        return location
    else:
        time = showtime(msg)
        if time.split()[0] == "Error:":
            return time
        elif time.split()[1] == 'safezone:':
            return time
        else:
            combo = {}
            combo = {'location':location,'hours':time}
            return combo

if sms[0] == '@':
        return "location: " + showlocation(msg) + " back in: " + showtime(msg)
else:
    return "need an @ sign"

def calcTime(msg):
    time = int(msg.split('for')[-1][1:])
    timeEntered = datetime.datetime.now()
    timeExpired = timeEntered + datetime.timedelta(hours=time)
    return timeExpired