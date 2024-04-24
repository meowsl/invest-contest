import time, os
import tensorflow as tf
from tensorflow.keras.initializers import Orthogonal
import numpy as np
from constants import DATA_CUR
from parse import find_rows_by_first_cell_value

def test_model(values: list, number: int or str):

    for folder, array in DATA_CUR.items():
        if str(number) in array:
            cur_folder = folder

    start_time = time.time()

    model_path = os.path.join(os.path.dirname(__file__), f'models/{cur_folder}/indicator{number}_model')
    model = tf.saved_model.load(model_path)

    loaded_model = tf.saved_model.load(model_path)
    data = np.array(values).reshape((-1, 1))

    data_tensor = tf.convert_to_tensor(data, dtype=tf.float32)
    data_tensor = tf.expand_dims(data_tensor, axis=-1)

    # Вызов метода predict модели
    output = loaded_model.signatures["serving_default"](inputs=data_tensor)

    # Получение результатов
    pred = output["output_0"].numpy()

    end_time = time.time()

    # Вывод результата предсказания и времени, затраченного на предсказание
    print("-" * 10)
    print(f'Model #{number}')
    print(f"Model prediction: {pred[-1][0]:.2f}")
    print(f"Time taken to make the prediction: {end_time - start_time:.4f} seconds")
    print("-" * 10)

def main():
    file_name = 'data/data.xlsx'
    value = 'Ростовская область'
    data_cur = find_rows_by_first_cell_value(file_name, value)
    for item in data_cur:
        test_model(item['Values'], item['Indicator'])

if __name__ == "__main__":
    main()