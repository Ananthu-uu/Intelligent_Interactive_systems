# import useful libraries
from multiprocessing import Process, Pipe
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

import cv2
import numpy as np
import opencv_jupyter_ui as jcv2
from feat import Detector
from IPython.display import Image

from feat.utils import FEAT_EMOTION_COLUMNS

import warnings
warnings.filterwarnings('ignore')

def train_and_eval(model, train_in, train_out, val_in, val_out):
    model.fit(train_in, train_out)
    predicted_val = model.predict(val_in)
    print("\nPredicted classes: ", predicted_val, "\n")

    # Evaluate model
    return accuracy_score(val_out, predicted_val)

def main(conn,signal1):
    # read and print data
    data = pd.read_csv("new/aufile.csv")
    
    # See classes
    #print("Unique classes", data["emotion"].unique(), "\n")

    # see class balance
    for class0 in data["emotion"].unique():
        print(f"Found {(data['emotion'] == class0).value_counts().iloc[1]} samples for class {class0}")

    # Let split the dataset for training
    labels = data["emotion"]
    inputs = data.drop(["emotion"], axis=1)
    
    
    data_in, test_in, data_out, test_out = train_test_split(
        inputs,
        labels,
        test_size=0.1,
        random_state=42,
        stratify=labels  # balances labels across the sets
    )
    train_in, val_in, train_out, val_out = train_test_split(
        data_in,
        data_out,
        test_size=(0.2/0.9),  # 20% of the original data
        random_state=42,
        stratify=data_out
    )

    print("\nLenght of each split of the data: ", len(train_in), len(val_in), len(test_in), "\n")
    
    # Train model 
    model_KNeighbors = KNeighborsClassifier()
    print(
        "\nAccuracy of model_KNeighbors: ",
        train_and_eval(model_KNeighbors, train_in, train_out, val_in, val_out)
    )

    print(
        "Best model accuracy on test set: ",
        accuracy_score(
            test_out,
            model_KNeighbors.predict(test_in)
        )
    )

    # Hyperparameter search/tuning


    # do the grid search on KNeighborsClassifier
    param_grid = [{
    "n_neighbors": [3, 5, 7, 9],      # Number of neighbors
    "weights": ["uniform", "distance"]  # Weighting of neighbors
    #"p": [1, 2] ,                        # Power parameter for Minkowski distance (1 for Manhattan, 2 for Euclidean)
    
    }]

    KNeighborsClassifier_search = GridSearchCV(KNeighborsClassifier(), param_grid,cv=5)
    KNeighborsClassifier_search.fit(train_in, train_out)
    print(
        "\n\nKNeighborsClassifier with best parameters on test set: ",
        accuracy_score(
            test_out,
            KNeighborsClassifier_search.predict(test_in)
        )
    )
    print(
        "Best parameters of KNeighborsClassifier: ",
        KNeighborsClassifier_search.best_params_
    )
    
    detector = Detector(device="cpu")
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cv2.namedWindow('Emotion display')
   

    while True:
        ret, frame = cam.read()
        if not ret:
            print("OpenCV found an error reading the next frame.")
        

        faces = detector.detect_faces(frame)  
        landmarks = detector.detect_landmarks(frame, faces)
        emotions = detector.detect_emotions(frame, faces, landmarks)
        #Au
        aus=detector.detect_aus(frame,landmarks)

        # The functions seem to assume a collection of images or frames. We acces "frame 0".
        faces = faces[0]
        landmarks = landmarks[0]
        emotions = emotions[0]
        aus=aus[0]
        

        if not faces:            
            print("no face")
            if signal1.poll():
                if(signal1.recv()=='ready'):
                    conn.send('no face')
            
            print('con')

        else:
            strongest_emotion = emotions.argmax(axis=1)  
            

            predicted_val = model_KNeighbors.predict(aus)
            predicted_val=str(predicted_val[0])
            
            if signal1.poll():
                if (signal1.recv()=='ready'):
                    conn.send(predicted_val)
                    print('put emotion in the pipe')

            
            
            for (face, top_emo) in zip(faces, strongest_emotion):
                (x0, y0, x1, y1, p) = face
                cv2.rectangle(frame, (int(x0), int(y0)), (int(x1), int(y1)), (255, 0,0), 3)
                cv2.putText(frame, predicted_val, (int(x0), int(y0 - 10)), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
            
            cv2.circle(frame,(32,32),16,(0,0,255),-1)
            cv2.imshow("Emotion Detection", frame)

            #how to pass the emotion to another system
        key = cv2.waitKey(1) & 0xFF
        if key == 27: # ESC pressed
            break


        #cam.release()
        
        
    




if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    signal1,signal2 = Pipe()
    p = Process(target=main, args=(child_conn,signal1))
    p.start()

    p.join()
    parent_conn.close()
    child_conn.close()
    