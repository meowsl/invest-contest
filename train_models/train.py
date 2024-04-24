import os, concurrent.futures
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    LSTM
)
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau
)
from parse import find_rows_by_first_cell_value
from constants import DATA_CUR

def generate_model(values: list, number: int or str):
    data = np.array(values)
    data = data.reshape((-1, 1))

    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]

    model = Sequential()

    # Слои
    model.add(LSTM(units=2048, input_shape=(1, 1), activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=1024, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=512, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=256, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=128, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=64, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=32, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=16, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=8, activation='relu', kernel_initializer='he_normal', kernel_regularizer=tf.keras.regularizers.l2(0.010)))
    model.add(Dense(units=1))

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)
    early_stopping = EarlyStopping(monitor='val_loss', patience=20)
    model.compile(optimizer='adam', loss='mean_squared_error')

    train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_data)).batch(1)
    validation_dataset = tf.data.Dataset.from_tensor_slices((test_data, test_data)).batch(1)

    model.fit(train_dataset, epochs=10, validation_data=validation_dataset, callbacks=[reduce_lr, early_stopping])

    forecast_2023 = model.predict(test_data)
    print(f"Прогноз на следующий год по показателю {number}: {forecast_2023[-1][0]:.2f}")

    if not os.path.exists('../server/source'):
        os.makedirs('../server/source')

    # Проверка на наличие папки и цура
    cur_folder = None
    for folder, array in DATA_CUR.items():
        if str(number) in array:
            cur_folder = folder
            break

    save_folder = os.path.join('../server/source', f'{cur_folder}')
    if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    save_path = os.path.join(os.getcwd(), f'{save_folder}/indicator{number}_model.h5')
    model.save(save_path)

def main():
    file_name = 'data/data.xlsx'
    value = 'Ростовская область'
    data_cur = find_rows_by_first_cell_value(file_name, value)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for item in data_cur:
            executor.submit(generate_model, item['Values'], item['Indicator'])

if __name__ == "__main__":
    main()
