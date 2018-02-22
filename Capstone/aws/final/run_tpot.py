import pandas as pd
import numpy as np
pd.set_option('max_colwidth',100)
import scipy as sp
from sklearn import preprocessing as pp
import pickle
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression, SGDClassifier
from sklearn.model_selection import cross_val_predict, GridSearchCV, train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

pred = pd.read_pickle('./couple_data_lasso_feature_selection_predictors')
target = pd.read_pickle('./couple_data_without_resample_target')

X_train, X_test, y_train, y_test = train_test_split(pred.values, target.values.ravel(), test_size=0.3, random_state=42)

# Try TPOT
from tpot import TPOTClassifier

pipeline_optimizer = TPOTClassifier(scoring='f1', cv=5, random_state=42, verbosity=2, n_jobs=-1)
pipeline_optimizer.fit(X_train, y_train)
pipeline_optimizer.export('./tpot_exported_pipeline.py')
