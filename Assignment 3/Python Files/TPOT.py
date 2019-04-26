import pandas as pd
from tpot import TPOTRegressor
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
from sklearn.preprocessing import Imputer

feature_matrix = pd.read_csv('Clean_Dataset.csv', index_col=0)

feature_matrix.head()

feature_matrix.drop(feature_matrix.select_dtypes(['object']), inplace=True, axis=1)

feature_matrix.head()

X = feature_matrix.drop('int_rate', axis=1)
y = feature_matrix['int_rate']

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=1)


X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=1)

tpot = TPOTRegressor(generations=3, population_size=50, verbosity=2, random_state=20)
tpot.fit(X_train, y_train)

y_hat = tpot.predict(X_test)
print("R2 score:", sklearn.metrics.r2_score(y_test, y_hat))