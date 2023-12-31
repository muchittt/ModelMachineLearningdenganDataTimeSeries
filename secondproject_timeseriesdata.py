# -*- coding: utf-8 -*-
"""secondProject : timeSeriesData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1arYUh6AH8l4tFxKcsPQTvjApSJq9CHmF
"""

# install kaggle package
!pip install -q kaggle

# upload kaggle.json
from google.colab import files
files.upload()

# buat direktori dan ubah izin
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!ls ~/.kaggle

!kaggle datasets download -d gauravduttakiit/new-york-taxi

# unzip
!mkdir new-york-taxi
!unzip new-york-taxi.zip -d new-york-taxi
!ls new-york-taxi

# load dataset
import pandas as pd
df = pd.read_csv('new-york-taxi/nyc_taxi.csv')
df.head()

# total data
df.shape

# data info
df.info()

df.isnull().sum()

import matplotlib.pyplot as plt
tgl = df['timestamp'].values
val = df['value'].values
 
 
plt.figure(figsize=(20,5))
plt.plot(tgl, val)
plt.title('Value',
          fontsize=25);

df = df.astype({"value": float})

df.dtypes

val = df['value'].values
val

val2 = val.reshape(-1,1)

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
min_max_scaler = StandardScaler()
val = min_max_scaler.fit_transform(val2)

val = val.flatten()
val

val.max()

val.min()

x = (val.max() - val.min()) * 10/100
print(x)

from sklearn.model_selection import train_test_split
X_latih, X_test = train_test_split(val, test_size=0.2, random_state = 0, shuffle=False)
print(len(X_latih), len(X_test))

def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-1], w[-1:]))
    return ds.batch(batch_size).prefetch(1)

import tensorflow as tf
from keras.layers import Dense, LSTM
latih_set = windowed_dataset(X_latih, window_size=60, batch_size=128, shuffle_buffer=5000)
test_set = windowed_dataset(X_test, window_size=60, batch_size=128, shuffle_buffer=5000)

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(60, return_sequences=True),
    tf.keras.layers.LSTM(60),
    tf.keras.layers.Dense(30, activation="relu"),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1),
    ])

# callback
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('mae')< x):
      self.model.stop_training = True
      print("\nMAE model berhenti karna < 10% dari skala data")
callbacks = myCallback()

optimizer = tf.keras.optimizers.SGD(lr=1.0000e-04, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])
history = model.fit(latih_set, 
                    validation_data=(test_set), 
                    epochs=100, 
                    callbacks=[callbacks])

from matplotlib import pyplot as plt
#loss train & validation
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Plot')
plt.ylabel('Value')
plt.xlabel('Epoch')
plt.legend(loc="upper right")
plt.show()

#accuracy train & validation
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('MAE Plot')
plt.ylabel('Value')
plt.xlabel('Epoch')
plt.legend(loc="upper right")
plt.show()

"""#Nama : Abdul Mukhit Murtadho
#Email : muchitabdul11@gmail.com
#No. Registrasi : 1494037162101-2090
"""