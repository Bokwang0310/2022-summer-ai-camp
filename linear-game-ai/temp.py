from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers

import pandas as pd
import numpy as np
import math


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


# 데이터 입력
df_pre = pd.read_csv('dino.csv', header=None)
df = df_pre.sample(frac=1)

dataset = df.values


print(df_pre.isnull().any())

X = dataset[:, 0:3]
Y = dataset[:, 3:]


X = NormalizeData(X)
Y = NormalizeData(Y)

finalX = []

for a in X:
    newX = [0 for i in range(30)]
    newX[math.trunc(a[0] * 10)] = 1
    newX[math.trunc(a[1] * 10) + 10] = 1
    newX[math.trunc(a[2] * 10) + 20] = 1
    finalX.append(newX)

print(finalX[0])
X = np.array(finalX)
print(X)
# print("X:", X)
# print("Y:", Y)

print(X[100])
print(Y[100])

print(X[550])
print(Y[550])

# 모델 설정
model = Sequential()
model.add(Dense(64, input_dim=X.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(2, activation='sigmoid'))

# model = Sequential()
# model.add(Dense(1, input_dim=3, activation="LeakyReLU"))


sgd = optimizers.SGD(learning_rate=0.001)

# 모델 컴파일
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop', metrics=["accuracy"])

# 모델 실행
model.fit(X, Y, epochs=30, batch_size=128, shuffle=True, validation_split=0.1)

model.save('dino.h5')

# 결과 출력
print("\n Accuracy: %.4f" % (model.evaluate(X, Y)[1]))
