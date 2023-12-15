from time import sleep
from furhat_remote_api import FurhatRemoteAPI
from numpy.random import randint
import cv2
#import exercise_3_face_tracking_solved
import pandas as pd
import random
FURHAT_IP = "localhost"

furhat = FurhatRemoteAPI(FURHAT_IP)
furhat.set_led(red=100, green=50, blue=50)
furhat.gesture(name="GazeAway")
furhat.say(text="hello you")



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

def demo_personas():
    set_persona('Amany')
    bsay("Hi there!")
    
    while (True):
        inp=input('emtion')
        #print("I'm reading\n")
        dt = pd.read_csv('Response.csv')
        dt_stat = dt[dt['emotion']==inp]
        print(dt_stat['response'])
        
        if inp == 'anger':
                if not dt_stat.empty:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                else:
                    bsay('bad day?')
        elif inp == 'sad':
                if not dt_stat.null:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                else:
                    bsay('bad day?')
        elif inp == 'neutral':
                if not dt_stat.null:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                    furhat.gesture(name='Wink')
                else:
                    bsay('What can I get you?')
                    furhat.gesture(name='Wink')
        elif inp == 'happy':
                if not dt_stat.null:
                    bsay(random.choice(dt_stat['response'].dropna().tolist()))
                    furhat.gesture(name='BigSmile')
                else:
                    bsay('You look happy')
                    furhat.gesture(name='BigSmile')
        else:
             bsay("Strange I can't read you")


        # if(inp=='anger' or inp=='disgust' or inp=='sad'):

        #     bsay('bad day?')
        # if(inp=='fear'):
        #     bsay('Why you look like you see a ghost.')
        # if(inp=='happy'):
        #     furhat.gesture(name='BigSmile')
        #     bsay('you look happy.')
        # if(inp=='neutral'):
        #     bsay('Shall I make something special to make you happy?')
        #     furhat.gesture(name='Wink')
        # if(inp=='surprise'):
        #     bsay('What happened?')

        
        #recomment drinks


    furhat.set_voice(name=VOICES_NATIVE['Amany'])
    #bsay("يسعدني أن ألتقي بكم جميعا!") # Nice to meet you all
    #furhat.set_voice(name=VOICES_EN['Amany'])
    
    sleep(1)
    idle_animation()
    sleep(1)
    
    #set_persona('Loo')
    #furhat.set_voice(name=VOICES_NATIVE['Loo'])
    #furhat.gesture(name='Smile')
    #bsay("Hej allihopa!")
    #furhat.set_voice(name=VOICES_EN['Loo'])
    #furhat.gesture(name='Smile')
    #bsay("My name is Loo, my pronouns are they them! I speak English and Swedish")
    



if __name__ == '__main__':
    demo_personas()
    idle_animation()
    