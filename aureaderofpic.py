import imageio.v3 as iio
import cv2
from matplotlib import pyplot as plt
from IPython.display import Image, Video
from feat import Detector
import opencv_jupyter_ui as jcv2
from feat.utils import FEAT_EMOTION_COLUMNS
import os
import pandas as pd



def main():
    
    detector = Detector(device="cpu")
    directory = 'DiffusionFER/DiffusionEmotion_S/original/surprise'
    emotion='surprise'
    
    all_au_info = []

    for filename in os.listdir(directory):
        #check if we have went through all pics
        #concatenate file name
        f = os.path.join(directory, filename)
        print(f)
        frame=cv2.imread(f)
        if frame is None:
            print(f"Skipping {filename}. Could not read the image.")
            continue

        face_prediction = detector.detect_image(f)
        d_all=[]
        for index,row in  face_prediction.iterrows():
            au_labels = face_prediction.au_columns
            au_values=pd.to_numeric(row[au_labels], errors='coerce')
            #print(au_values)
            
            d={"file":filename[:-4],"emotion":emotion}
            for au_label in au_labels:            
                au_values = row[au_label]
                d_acc={au_label:au_values}
                d.update(d_acc)

            d_all.append(d) 
        au_dataframe = pd.DataFrame(data=d_all)
        # Save the DataFrame to a CSV file
        all_au_info.append(au_dataframe)
    
    final_au_dataframe = pd.concat(all_au_info, ignore_index=True)

# Save the final DataFrame to a CSV file
    final_au_dataframe.to_csv('aus.csv', header=True, index=False)
        
       
if __name__=="__main__":
    main()