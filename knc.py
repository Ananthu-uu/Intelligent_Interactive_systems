# import useful libraries
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
global predicted_val

def train_and_eval(model, train_in, train_out, val_in, val_out):
    model.fit(train_in, train_out)
    predicted_val = model.predict(val_in)
    print("\nPredicted classes: ", predicted_val, "\n")

    # Evaluate model
    return accuracy_score(val_out, predicted_val)

def main():
    # read and print data
    data = pd.read_csv("new/aufile.csv")
    

    """if 'emotion' in data:
        print("Unique classes", data['emotion'].unique(), "\n")
    else:
        print("'emotion' key not found in data.")
"""
    # See classes
    #print("Unique classes", data["emotion"].unique(), "\n")

    # see class balance
    for class0 in data["emotion"].unique():
        print(f"Found {(data['emotion'] == class0).value_counts().iloc[1]} samples for class {class0}")

    # Let split the dataset for training
    labels = data["emotion"]
    inputs = data.drop(["file","emotion"], axis=1)
    #inputs = data.drop("emotion", axis=1)
    
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

                #read the test file
                #data_test=pd.read_csv("test_to_submit.csv")
                #data_test=[[0.515332,   0.5002553,  0.0583544,  0.22678073, 0.09000432, 0., 0.14082894, 0.02020728, 1. ,        0.02395544, 0.08782247, 0.31127515, 0.47308826, 0. ,        0.37197974, 0.44092998, 0.00786083, 0.05478874, 0.27576774, 0.35553083]]
                #df = pd.DataFrame(data=aus)
                #print(df)
                #aus_array = np.array(aus).reshape(1, -1)
                #predicted_val = model_KNeighbors.predict(aus)
                #print(predicted_val)
            
                print("no face")
                with open("shared_value.txt", "w") as file:
                    file.write("noface")
        else:
                predicted_val = model_KNeighbors.predict(aus)
                predicted_val=str(predicted_val[0])
                print(predicted_val)
                with open("shared_value.txt", "w") as file:
                    file.write(predicted_val)
                #how to pass the emotion to another system


        #cam.release()
        
        
    




if __name__ == "__main__":
    
    main()