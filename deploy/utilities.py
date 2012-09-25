import datetime
import models
import plivo
#from views import send_txt

from pyparsing import Literal, Group, OneOrMore, Word, StringEnd, SkipTo, Literal, oneOf, alphas, nums

MASTER_NUMBER = '16262190621'

safezones = ['home',
      'unicef',
      'makerere'
      ]
      
smstestlist = [ '@ mbarara university for 5',
                '@ makere uni comp sci dept for 2',
                '@ home',
                '@mbarara for 7',
                '@garden city for 9',
                '@unicef',
                "@yomamas",
                "@yomama's",
                '@unicef for 3',
                '@ garden city',
                '@ garden city for 26',
                '@ art center For 12',
                '@ art center 4 12',
                '@ art center 4 4',
              ]
              
def check_in_parsing(s):
    update =    (Literal('@') + 
                Group(OneOrMore(Word(alphas))) +  
                StringEnd()) | (Literal('@') + 
                SkipTo(oneOf("4 for For FOR")) + 
                oneOf('4 for For FOR') + 
                Word(nums))
    
    #for s in smstestlist:
    #    print s
    try:
        u = update.parseString(s)
        print u
        if len(u) == 2:
            u[1] = ' '.join(u[1])
            if u[1] in safezones:
                print "user in safezone " + u[1]
                combo = {'location':u[1],'hours':'24'}
                return combo
            else:
                print "Error: " + u[1] + " is not a safezone!"
                return "Error: " + u[1] + " is not a safezone!"
        else:
            print "user at " + u[1] + " for " + u[3] + " hours."
            combo = {'location':u[1],'hours':str(u[3])}
            return combo
    except:
        print "Error: Unable to understand!"

def listserve_broadcast(message):
    return "No listserve functionality yet."
    
def group_maintenance(message):
    return "No group maintenance functionality yet."
    
def help_parsing(message):
    return "No help functions yet"
    
commands = {'@':check_in_parsing,
            '!':listserve_broadcast,
            'g':group_maintenance,
            'h':help_parsing,
            }
            
def check_time():
    users = User.query.all()
    for u in users:
        if u.status.timeExpired <= datetime.datetime.now() and u.status.condition == 'safe':
            u.status.condition = 'uncertain'
            newTime = datetime.datetime.now() + datetime.timedelta(hours=2)
            u.status.timeExpired = newTime
            u.save()
            send_txt(u.number, "Your time has expired. Please reply with a new checkin status.", src=MASTER_NUMBER)
        elif u.status.timeExpired <= datetime.datetime.now() and u.status.condition == 'uncertain':
            u.status.condition = 'alert'
            newTime = datetime.datetime.now() + datetime.timedelta(minutes=10)
            u.status.timeExpired = newTime
            u.save()
            send_txt(u.number, "Your time has expired and we are about to alert EChin. Please reply with a new checkin status.", src=MASTER_NUMBER)
        elif u.status.timeExpired <= datetime.datetime.now() and u.status.condition == 'alert':
            u.status.condition = 'missing'
            u.save()
            alertMessage = u.name + ' is missing!'
            send_txt(u.number, "The Panoptincon will find you!", src=MASTER_NUMBER)
            send_txt('14845575821', alertMessage, src=MASTER_NUMBER)
        else:
            send_txt('14845575821', 'All is well in your kingdom', src=MASTER_NUMBER)
    return "cron done run."

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
    safezones = ['home',
         'unicef',
         'makerere'
         ]
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
    safezones = ['home',
         'unicef',
         'makerere'
         ]
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
        elif "safezone" in time:
            combo = {}
            safezone = time.split('safezone:')[-1][1:]
            combo = {'location':safezone,'hours':'24'}
            return combo
        else:
            combo = {}
            combo = {'location':location,'hours':time}
            return combo
"""
if sms[0] == '@':
        return "location: " + showlocation(msg) + " back in: " + showtime(msg)
else:
    return "need an @ sign"
"""

def calcTime(msg):
    time = int(msg.split('for')[-1][1:])
    timeEntered = datetime.datetime.now()
    timeExpired = timeEntered + datetime.timedelta(hours=time)
    return timeExpired