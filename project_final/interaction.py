from multiprocessing import Process, Pipe
from time import sleep
from furhat_remote_api import FurhatRemoteAPI
from numpy.random import randint
import pandas as pd
import random
import cv2

FURHAT_IP = "localhost"
#from knc import predicted_val

furhat = FurhatRemoteAPI(FURHAT_IP)
furhat.set_led(red=100, green=50, blue=50)
furhat.gesture(name="GazeAway")
#furhat.say(text="hello you")


FACES = {
    'Loo'    : 'Patricia',
    'Amany'  : 'Nazar'
}

VOICES_EN = {
    'Loo'    : 'BellaNeural',
    'Amany'  : 'CoraNeural'
}

VOICES_NATIVE = {
    'Loo'    : 'SofieNeural',
    'Amany'  : 'AmanyNeural'
}

def idle_animation():
    furhat.gesture(name="GazeAway")
    gesture = {"frames" : 
        [{
            "time" : [0.33],
            "persist" : True,
            "params": {
                "NECK_PAN"  : randint(-4,4),
                "NECK_TILT" : randint(-4,4),
                "NECK_ROLL" : randint(-4,4),
            }
        }],

    "class": "furhatos.gestures.Gesture"
    }
    furhat.gesture(body=gesture, blocking=True)

def LOOK_BACK(speed):
    return {
    "frames": [
        {
            "time": [
                0.33 / speed
            ],
            "persist": True,
            "params": {
                'LOOK_DOWN' : 0,
                'LOOK_UP' : 0,
                'NECK_TILT' : 0
            }
        }, {
            "time": [
                1 / speed
            ],
            "params": {
                "NECK_PAN": 0,
                'LOOK_DOWN' : 0,
                'LOOK_UP' : 0,
                'NECK_TILT' : 0
            }
        }
    ],
    "class": "furhatos.gestures.Gesture"
    }

# DO NOT CHANGE
def LOOK_DOWN(speed=1):
    return {
    "frames": [
        {
            "time": [
                0.33 / speed
            ],
            "persist": True,
            "params": {
#                'LOOK_DOWN' : 1.0
            }
        }, {
            "time": [
                1 / speed
            ],
            "persist": True,
            "params": {
                "NECK_TILT": 20
            }
        }
    ],
    "class": "furhatos.gestures.Gesture"
    }

def set_persona(persona):
    furhat.gesture(name="CloseEyes")
    furhat.gesture(body=LOOK_DOWN(speed=1), blocking=True)
    sleep(0.3)
    furhat.set_face(character=FACES[persona], mask="Adult")
    furhat.set_voice(name=VOICES_EN[persona])
    sleep(2)
    furhat.gesture(body=LOOK_BACK(speed=1), blocking=True)

# Say with blocking (blocking say, bsay for short)
def bsay(line):
    furhat.say(text=line, blocking=True)


# function to repond to user emotion
def emo_response(em):
    dt = pd.read_csv('./conversation/Response.csv')
    dt_stat = dt[dt['emotion']==em]
    #print(dt_stat['response'])
    if em == 'angry':
                #if not dt_stat.empty:
                if not dt_stat.empty:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                else:
                    bsay('bad day?')
    elif em == 'sad':
                #if not dt_stat.null:
                if not dt_stat.empty:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                else:
                    bsay('bad day?')
    elif em == 'neutral':
                #if not dt_stat.null:
                if not dt_stat.empty:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                    furhat.gesture(name='Wink')
                else:
                    bsay('What can I get you?')
                    furhat.gesture(name='Wink')
    elif em == 'happy':
                #if not dt_stat.null:
                if not dt_stat.empty:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                    furhat.gesture(name='BigSmile')
                else:
                    bsay('You look happy')
                    furhat.gesture(name='BigSmile')
    else:
        bsay("Strange I can't read you")


# a function to process converation based on user reply
def user_reply(re,dt):
    if re.success:
        match = dt[dt["user_reply"]==re.message]
        print(match)
        if match.empty:
            bsay("Sorry, I didn't hear you")
        else:
            bsay(match["bot_response"].iloc[0])
    else:
        bsay("Sorry, I didn't hear you")


def demo_personas(conn,signal):
    set_persona('Amany')
    bsay("Hi there!, I am your personal bartender")
    furhat.set_led(red=200, green=50, blue=50)

    while (True):

        signal.send('no')
        re=furhat.listen()
        # to start the conversation, say hello.
        while(re.message!='hello'):
            #do nothing, just listen
            print("keep listening")
            re=furhat.listen()
        
        print("start")
            
        signal.send('ready')

        # get emotion value from the perception sub-system
        em=conn.recv()

        dt = pd.read_csv(f"./conversation/{em}.csv")
        emo_response(em)
        re=furhat.listen()
        while(re.message!="thank you"):
            #re=furhat.listen()
            print(re.message)
            sleep(1)
            user_reply(re,dt)
            re=furhat.listen()
        
        bsay("you are welcome")



if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    signal1,signal2 = Pipe()
    p = Process(target=demo_personas, args=(parent_conn,signal2))
    p.start()
    p.join()
    


    parent_conn.close()
    child_conn.close()
    
    