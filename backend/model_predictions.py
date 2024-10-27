import tensorflow as tf
import numpy as np
import pandas as pd

from sklearn import preprocessing

model = tf.keras.models.load_model(r'backend\best_model.keras')
sex_dummies_cols = pd.read_csv(r"backend\data\sex_dummies_columns.csv", header=0).squeeze().values
local_dummies_cols = pd.read_csv(r"backend\data\local_dummies_columns.csv", header=0).squeeze().values
y_labels = ("Actinic keratoses and intraepithelial carcinoma / Bowen's disease", #('akiec','bcc','bkl', 'df','nv','vasc', 'mel')
"Basal cell carcinoma",
"Benign keratosis-like lesions",
"Dermatofibroma",
"Melanocytic nevi",
"Vascular lesions",
"Melanoma")

# classify age
def processAge(age:int):
    if age < 30:
        age = 0
    elif age < 50:
        age = 1
    else:
        age = 2
    return np.array([float(age)])

def processLocal(local:str):
    dum_cols = pd.get_dummies(local)
    result = dum_cols.reindex(columns=local_dummies_cols, fill_value=0) # new categories automatically 0
    return np.array([result],dtype=np.float64)[0][0]

def processSex(sex:str):
    dum_cols = pd.get_dummies(sex)
    result = dum_cols.reindex(columns=sex_dummies_cols, fill_value=0) # new categories automatically 0
    return np.array([result], dtype=np.float64)[0][0]

def predict(raw_picture_data, age:int, sex:str, local:str): # raw_pic_data should be list of floats
    age = processAge(age)
    sex = processSex(sex)
    local = processLocal(local)

    
    inputs = np.concatenate((raw_picture_data, age))
    inputs = np.concatenate((inputs, sex))
    inputs = np.concatenate((inputs, local))
    inputs = np.array([inputs])

    # normalize inputs
    scaler = preprocessing.StandardScaler().fit(inputs)
    inputs = scaler.transform(inputs)

    results = model.predict(inputs)

    idx = np.argmax(results)
    title = y_labels[idx]
    return results[0][idx], title

if __name__ == "__main__":
    age = 80
    sex = "male"
    localization = "scalp"
    test_path = r"backend\tests\processed_test_picture.txt"
    with open(test_path, "r") as file:
        test_pic = file.readline()
    test_pic = np.array(test_pic.split(","),dtype=np.float64)

    prediction = predict(test_pic,age, sex, localization)
    print(prediction)
    # print(np.argmax(prediction))