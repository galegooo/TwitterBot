# Python3
import tweepy
import time



def retrieve(fileName):
    textFile = open(fileName, 'r')
    ID = int(textFile.read().strip())
    textFile.close()
    return ID


def store(ID, fileName):
    textFile = open(fileName, 'w')
    textFile.write(str(ID))
    textFile.close()
    return


def search():
    global phrase
    # Retrieve the last seen tweet's ID
    lastNice = retrieve(niceFileName)

    # Retrieve number of nices to this point
    numberNices = retrieve(niceCountFileName)

    nices = api.search(q = '#nice', since_id = lastNice)


    try:
        # Reverse to see first the older tweets
        for nice in reversed(nices):
            print('Found #nice: ' + nice.text + '\n\tID: ' + str(nice.id)
                  + '\n\tUsername: ' + nice.user.screen_name + '\nResponding...')
            lastNice = nice.id
            store(lastNice, niceFileName)

            # This is here because of bot prevention
            numberNices = numberNices + 1
            store(numberNices, niceCountFileName)

            if(phrase == 0):
                api.update_status('@' + nice.user.screen_name +
                ' Your nice hashtag was the ' + str(numberNices) +
                'th since 13/04/2020 13:08! Nice!', nice.id)
            elif(phrase == 1):
                api.update_status('@' + nice.user.screen_name +
                ' Since 13/04/2020 13:08, there has been ' + str(numberNices - 1) +
                ' nice hashtags. Yours was ' + str(numberNices) + '. Nice!', nice.id)
            elif(phrase == 2):
                api.update_status('@' + nice.user.screen_name +
                ' With your nice hashtag, the number of nices said since 13/04/2020 13:08 has increased to ' +
                str(numberNices) + '. Nice!', nice.id)

            phrase = phrase + 1
            if(phrase == 3):
                phrase = 0

            print('\n')
    except:
        print("Error found, waiting 15m")
        time.sleep(60*14)   #14m plus the 1 in the infinte loop


mentionsFileName = 'MentionsID.txt'
niceFileName = 'NiceID.txt'
niceCountFileName = 'NiceCount.txt'

# You can find these keys in twitter developer
consumerKey = 'P3PbJ3qBM8LOBU5L4pnjKotsM'
consumerSecret = 'xLGrQH2j7OjLZXKwHczupL8IdPlVq1vAUOww4RxJXax6P93GQy'
accessKey = '1249442524873146369-GQ5DTDYTMqY99muNrbPycXsBX6lTS0'
accessSecret = 'KtQp1Ez1X5uc6kmM16qXXwnSUxl3lHBRonVVIL9TXTMp7'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)

# This is to prevent bot detection
global phrase
phrase = 0

# Infinite loop, always responding
while True:
    print('Checking for #nice...')
    search()
    print('Waiting 60 seconds')
    time.sleep(60)
