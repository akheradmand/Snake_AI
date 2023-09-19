import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data = pd.read_csv('dataset/dataset.csv')
data.fillna(0, inplace=True)

X = np.array(data.iloc[:, :-1].values)
Y = np.array(data.iloc[:, -1].values)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

model=tf.keras.models.Sequential([
    tf.keras.layers.Dense(12, activation='relu'),
    tf.keras.layers.Dense(20,activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(4,activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

output=model.fit(X_train, Y_train, epochs=100)

model.evaluate(X_test, Y_test)

fig,(ax1,ax2)=plt.subplots(1,2)
ax1.plot(output.history["loss"])
ax1.set_title("loss")
ax2.plot(output.history["accuracy"])
ax2.set_title("accuracy")
plt.show()

model.save('weights/my_snake_model.h5')