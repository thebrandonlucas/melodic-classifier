
# coding: utf-8

# In[164]:


import numpy as np
import pandas as pd
import os, sys


# In[165]:


orig_dir = "/Volumes/NexStar3/Preclinical_fMRI_Converted"

def getFiles(path, substring, *args):
    array = []
    for root, dirs, files in os.walk(path):
            for file in files:
                stop = False
                if substring in file:
                    for arg in args: 
                        if arg in file: 
                            stop = True
                    if stop is True: 
                        continue
                    filepath = root + '/' + file
                    array.append(filepath)
                    # print(filepath)
    return array;


# In[166]:


os.chdir(orig_dir)

f_artifact = []
t_artifact = []
f_non_artifact = []
t_non_artifact = []
count = 0
for root, dirs, files in os.walk(orig_dir):
    for directory in dirs:
        # make this an option later
        if "Preclin" in directory:
            mriDirs = []
            for d in os.listdir(directory): 
                if "Encoding1_AP_MB4_2_5mmISO_2" in d: 
                    mriDirs.append(d)
            os.chdir(directory)
            for d in mriDirs: 
                # the files that indicate which id's are artifacts
                if "fix_s8.txt" in os.listdir(d):
                    artifact_numbers_file = open(d + "/fix_s8.txt")
                else: 
                    continue
                for d2 in os.listdir(d): 
                    if "melodic_s8" in d2: 
                        melodic_folder = d2
                os.chdir(d)
                # switch into melodic dir 
                line = artifact_numbers_file.readline()
                artifact_numbers_file.close()
                artifact_numbers = line.strip().split(",")
                # every var after "t" is substrings to exclude
                directory = root + '/' + directory + '/' + d + '/' + melodic_folder + '/report'
                f_files = getFiles(directory, "f", "EV", "index", "IC", "._", ".html", "DS", "png", "fix")
                t_files = getFiles(directory, "t", "EV", "index", "IC", "._", "f", ".html", "DS", "png", "fix")
                for file_path in f_files:
                    filename = file_path.split("/")[-1]
                    file_id = filename.split("f")[1]
                    file_id = file_id.split(".")[0]
                    if file_id in artifact_numbers:
                        f_artifact.append(file_path)
                    else:
                        f_non_artifact.append(file_path)
                for file_path in t_files:
                    filename = file_path.split("/")[-1]
                    file_id = filename.split("t")[1]
                    file_id = file_id.split(".")[0]
                    if file_id in artifact_numbers:
                        t_artifact.append(file_path)
                    else:
                        t_non_artifact.append(file_path)
                os.chdir('..')
        os.chdir(root)
        


# In[167]:


from sklearn.model_selection import train_test_split
from numpy import median

# load all the text file data
# we're loading both the f and t file data, 
# the first half of the matrix will be the 
# f data and the second half the t data
data = []
labels = []
for f in f_artifact:
    with open(f) as file: 
        temp = []
        for line in file: 
            temp.append(float(line.strip()))
        median = np.median(temp)
        while len(temp) < 282: 
            temp.append(median)
        data.append(temp)
        labels.append(1)

for f in f_non_artifact: 
    with open(f) as file: 
        temp = []
        for line in file: 
            temp.append(float(line.strip()))
        median = np.median(temp)
        while len(temp) < 282: 
            temp.append(median)
        data.append(temp)
        labels.append(0)

    
for t in t_artifact: 
    with open(t) as file: 
        temp = []
        for line in file: 
            temp.append(float(line.strip()))
        median = np.median(temp)
        while len(temp) < 282: 
            temp.append(median)
        data.append(temp)
        labels.append(1)


for t in t_non_artifact: 
    with open(t) as file: 
        temp = []
        for line in file: 
            temp.append(float(line.strip()))
        median = np.median(temp)
        while len(temp) < 282: 
            temp.append(median)
        data.append(temp)
        labels.append(1)

print(len(data))
print(data[0])
print(data[-1])


# In[168]:


# data = np.array(data)
# labels = np.array(labels)
print(data[-1])
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)


# In[169]:


from sklearn.preprocessing import Imputer

imputer = Imputer(strategy="median")

imputer.fit_transform(X_train)


# In[170]:


# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# print(X_train.shape)
# print(y_train.shape)

# svm_clf = SVC(kernel="poly", degree=3, coef0=1, C=5)
# svm_clf.fit(X_train, y_train)
# y_pred = svm_clf.predict(X_test)

random_forest_clf = RandomForestClassifier(n_estimators=10, random_state=42)
random_forest_clf.fit(X_train, y_train)
y_pred = random_forest_clf.predict(X_test)

accuracy_score(y_test, y_pred)

# score = cross_val_score(log_clf, X_train, y_train, cv=5, verbose=3)
# score.mean()


# In[176]:


from sklearn.externals import joblib

joblib.dump(random_forest_clf, "tmp/random_forest_clf.pkl")

# random_forest_clf_loaded = joblib.load("random_forest_clf.pkl")


# In[172]:


from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from scipy.stats import reciprocal, uniform

# param_distributions = {"gamma": reciprocal(0.001, 0.1), "C": uniform(1, 10)}
param_distributions = {"n_estimators": [5, 10, 15]}
rnd_search_cv = GridSearchCV(random_forest_clf, param_distributions, verbose=2, cv=5)
rnd_search_cv.fit(X_train, y_train)


# In[173]:


rnd_search_cv.best_estimator_


# In[174]:


rnd_search_cv.best_score_


# In[175]:


rnd_search_cv.best_estimator_.fit(X_train, y_train)

y_pred = rnd_search_cv.best_estimator_.predict(X_test)
accuracy_score(y_test, y_pred)

