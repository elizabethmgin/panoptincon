sms = '@ mbarara university for 5 hours'
sms2 = '@ makere uni comp sci dept for 2 hours'
sms3 = '@ home'
sms4 = '@mbarara for 7 hours'
sms5 = '@garden city for 9 hours'

safezones = ['home',
             'unicef',
             'makerere'
             ]

def showlocation(msg):
    if msg[0] == '@':
        if msg[0:2] == '@ ':
            return msg.split('for')[0].split('@')[1][1:-1]
        else:
            return msg.split('for')[0].split('@')[1][0:-1]
    else:
        return "error"

def showtime(msg):
    return msg.split('for')[-1][1:]



def showtimeandloc(msg):
    if sms[0] == '@':
        if 'for' in msg:
            return "location: " + showlocation(msg) + " back in: " + showtime(msg)
        elif

    else:
        return "error"