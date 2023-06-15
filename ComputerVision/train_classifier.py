import pickle
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


data_dict = pickle.load(open('./onehand.pickle', 'rb'))
data_one = np.asarray(data_dict['data'])
labels1 = np.asarray(data_dict['labels'])


x_train, x_test, y_train, y_test, = train_test_split(data_one, labels1, test_size=0.2, shuffle=True, stratify=labels1)

model1 = RandomForestClassifier()

model1.fit(x_train, y_train)

y_predict = model1.predict(x_test)

score1 = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly for model1 !'.format(score1 * 100))

f = open('model1.p', 'wb')
pickle.dump({'model1': model1}, f)
f.close()

