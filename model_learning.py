import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


#function to train and test the evaluation model

def train_and_eval(model, train_in, train_out, val_in, val_out):
    model.fit(train_in, train_out)
    predicted_val = model.predict(val_in)
    print("\nPredicted classes: ", predicted_val, "\n")

    # Evaluate model
    return accuracy_score(val_out, predicted_val)



def main():
    data = pd.read_csv("aufile.csv")   #integrate the values from aufile.csv
    #print(data)


    # splitting of data
    labels = data["emotion"]
    inputs = data.drop("emotion", axis=1)
    #print("Input : \n",inputs)
    #print("Labels: ",labels,"\n")
    # split = 70/20/10
    #Testing
    data_in, test_in, data_out, test_out = train_test_split(
        inputs,
        labels,
        test_size=0.1,
        random_state=42,
        stratify=labels  # balances labels across the sets
    )
    #validation
    train_in, val_in, train_out, val_out = train_test_split(
        data_in,
        data_out,
        test_size=(0.2/0.9),  # 20% of the original data
        random_state=42,
        stratify=data_out
    )

    model_1 = DecisionTreeClassifier()
    print(
        "\nAccuracy of model_1: ",
        train_and_eval(model_1, train_in, train_out, val_in, val_out)
    )
    param_grid_dt = {'criterion':['gini','entropy'],
              'max_depth':np.arange(1,21).tolist()[0::2],
              'min_samples_split':np.arange(2,11).tolist()[0::2],
              'max_leaf_nodes':np.arange(3,26).tolist()[0::2]}
    best_model_dt = GridSearchCV(DecisionTreeClassifier(), param_grid_dt, cv=5, n_jobs=-1)
    best_model_dt.fit(train_in, train_out)
    best_model_dt.predict(test_in)
    acc_score_dt = accuracy_score(test_out,best_model_dt.predict(test_in))
    print("Performance of DecisionTreeClassifier model on the test set:", acc_score_dt*100,"% \n")

    print("Best parameter value for DecisionTreeClassifier model: ",best_model_dt.best_params_,"\n") 
    #SVC model

    model_2 = SVC()
    print(
        "\nAccuracy of model_2: ",
        train_and_eval(model_2, train_in, train_out, val_in, val_out)
    )
    param_grid_svc = [
        {"kernel": ["poly"], "degree": [3, 15, 25, 50]},
        {"kernel": ["rbf", "linear", "sigmoid"]}
    ]

    best_model_svc = GridSearchCV(SVC(), param_grid_svc)
    best_model_svc.fit(train_in, train_out)
    best_model_svc.predict(test_in)
    acc_score_svc = accuracy_score(test_out,best_model_svc.predict(test_in))
    print("Performance of SVC model on the test set:", acc_score_svc*100,"% \n")

    print("Best parameter value for SVC model: ",best_model_svc.best_params_,"\n") 


    # K Neighbors classifier model
    model_3 = KNeighborsClassifier()
    acc = train_and_eval(model_3,train_in,train_out, val_in, val_out)
    print("Accuracy of the KNN model: ",acc*100,"% \n")

    #Hyperparameter tuning by giving a range of K value between 1 and 30
    k_values = np.arange(1, 30, 1)
    print("k values: ",k_values,"\n")
    param_grid_KNN = dict(n_neighbors=k_values)

    best_model_KNN = GridSearchCV(model_3,param_grid_KNN)
    best_model_KNN.fit(train_in,train_out)
    best_model_KNN.predict(test_in)
    acc_score_KNN = accuracy_score(test_out,best_model_KNN.predict(test_in))
    print("Performance of KNN model on the test set:", acc_score_KNN*100,"% \n")

    print("Best K value for knn model: ",best_model_KNN.best_params_,"\n") 


    #Integrate the values coming from the live feed

    # ld_test_to_submit = pd.read_csv("test_to_submit.csv")
    # classification = best_model.predict(ld_test_to_submit)
    # np.savetxt('outputs',classification,fmt='%s')
   
    
    

if __name__ == "__main__":
    main()