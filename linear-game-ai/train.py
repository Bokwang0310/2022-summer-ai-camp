from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers

import pandas as pd
import numpy as np


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


# 데이터 입력
df_pre = pd.read_csv('dino.csv', header=None)
df = df_pre.sample(frac=1)

dataset = df.values


X = dataset[:, 0:3]
Y = dataset[:, 3:]


X = NormalizeData(X)
Y = NormalizeData(Y)


# 모델 설정
model = Sequential()
model.add(Dense(32, input_dim=X.shape[1], activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(2, activation='sigmoid'))

sgd = optimizers.SGD(learning_rate=0.001)

# 모델 컴파일
model.compile(loss='mse',
              optimizer=sgd, metrics=["acc"])

# 모델 실행
model.fit(X, Y, epochs=30, batch_size=32, shuffle=False, validation_split=0.1)

model.save('dino.h5')

# 결과 출력
print("\n Accuracy: %.4f" % (model.evaluate(X, Y)[1]))
