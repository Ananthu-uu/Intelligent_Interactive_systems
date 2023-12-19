from multiprocessing import Process, Pipe
from time import sleep
from furhat_remote_api import FurhatRemoteAPI
from numpy.random import randint
import cv2
import exercise_3_face_tracking_solved
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

def neutralfunc():
    
    # Start listening for speech
    re=furhat.listen()

    if(re.success):
        if(re.message=='do you have any suggestion'):
            bsay('maybe a glass of beer')
            re=furhat.listen()
            if(re.message=='sure'):
                bsay('here you go')
        elif(re.message=='I would like a glass of white wine'):
            bsay('good choice, here you go')
            furhat.gesture(name='Smile')
        else:
            bsay('sorry, can you say it again?')
            neutralfunc()
    else:
        bsay('sorry, can you say it again?')
        neutralfunc()
        

def angerfunc():
    
    # Start listening for speech
    re=furhat.listen()

    if(re.success):
        if(re.message=='yes, I want to have a whiskey'):
            bsay('Sure, here you go')

        elif(re.message=='I do not want to talk about it'):
            bsay('sure, maybe you want to have a shot of tequila')
            furhat.gesture(name='Smile')
            re=furhat.listen()
            if(re.message=='sure'):
                bsay('here you go')
        else:
            bsay('sorry, can you say it again?')
            angerfunc()
    else:
        bsay('sorry, can you say it again?')
        angerfunc()

def sadfunc():
    
    # Start listening for speech
    re=furhat.listen()

    if(re.success):
        if(re.message=='Just give me rum'):
            bsay('Sure, here you go')

        elif(re.message=='can you make some drinks to cheer me up'):
            bsay('sure, maybe you want to have our special cocktail')
            furhat.gesture(name='Smile')
            re=furhat.listen()
            if(re.message=='sure'):
                bsay('here you go')
        else:
            bsay('sorry, can you say it again?')
            sadfunc()
    else:
        bsay('sorry, can you say it again?')
        sadfunc()


def happyfunc():
    
    # Start listening for speech
    re=furhat.listen()

    if(re.success):
        if(re.message=='yes, can I have a glass of red wine'):
            bsay('Sure, here you go')

        elif(re.message=='do you have any suggestion'):
            bsay('yes, maybe you want to have fireball')
            furhat.gesture(name='Smile')
            re=furhat.listen()
            if(re.message=='sure'):
                bsay('here you go')
        else:
            bsay('sorry, can you say it again?')
            happyfunc()
    else:
        bsay('sorry, can you say it again?')
        happyfunc()


def demo_personas(conn,signal):
    set_persona('Amany')
    bsay("Hi there!, I am your personal bartender")
    furhat.set_led(red=200, green=50, blue=50)

    while (True):

        signal.send('no')
        re=furhat.listen()
        while(re.message!='hello'):
            #do nothing, just listen
            print("keep listening")
            re=furhat.listen()
        
        print("start")
            
        signal.send('ready')

        #COMBINE emotion and speech
        em=conn.recv()
        if(em=='angry'):
            bsay('bad day?')
            angerfunc()
        if(em=='sad'):
            bsay('what can I do to cheer you up?')
            sadfunc()
        if(em=='happy'):
            furhat.gesture(name='BigSmile')
            bsay('you look happy, that is great, what would you like to have')
            happyfunc()
        if(em=='neutral'):
            bsay('Shall I make something special to make you happy?')
            furhat.gesture(name='Wink')
            neutralfunc()

        #read emotion again
        




if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    signal1,signal2 = Pipe()
    p = Process(target=demo_personas, args=(parent_conn,signal2))
    p.start()
    p.join()
    


    parent_conn.close()
    child_conn.close()
    
    