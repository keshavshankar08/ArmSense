import sys
sys.path.append('.')

import csv
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

class Trainer:
    def __init__(self):
        '''
        Initialize the Trainer with the default file name and an empty model.
        '''
        self.model = None

    def clean_data(self, input_data_file_name, output_data_file_name):
        '''
        Remove rows with missing values from the data file.

        :param input_data_file_name: The name of the input data file.
        :param output_data_file_name: The name of the output data file.
        '''
        cleaned_data = []
        with open(input_data_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if not any(cell == 'nan' for cell in row):
                    cleaned_data.append(row)
        
        with open(output_data_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(cleaned_data)

    def normalize_data(self, input_data_file_name, output_data_file_name, output_bounds_file_name):
        '''
        Normalize the features in the data file and store min and max values.

        :param input_data_file_name: The name of the input data file.
        :param output_data_file_name: The name of the output data file.
        :param output_bounds_file_name: The name of the output bounds file.
        '''
        data = []
        with open(input_data_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

        data = np.array(data, dtype=float)
        features = data[:, :48]
        labels = data[:, 48]

        min_vals = features.min(axis=0)
        max_vals = features.max(axis=0)
        normalized_features = (features - min_vals) / (max_vals - min_vals)

        normalized_data = np.hstack((normalized_features, labels.reshape(-1, 1)))

        with open(output_data_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(normalized_data)

        with open(output_bounds_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(min_vals)
            writer.writerow(max_vals)

    def train_model(self, input_data_file_name, output_model_file_name):
        '''
        Train a model using the data in the data file.

        :param input_data_file_name: The name of the input data file.
        :param output_model_file_name: The name of the output model file.
        '''
        data = []
        with open(input_data_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

        data = np.array(data, dtype=float)
        features = data[:, :48]
        labels = data[:, 48]

        X_train, X_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.2, random_state=42)
        X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(48,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(5, activation='softmax')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

        class CustomCallback(tf.keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                print(f"Epoch {epoch + 1}: loss = {logs['loss']:.4f}, accuracy = {logs['accuracy']:.4f}, val_loss = {logs['val_loss']:.4f}, val_accuracy = {logs['val_accuracy']:.4f}")

        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

        model.fit(X_train, y_train, epochs=150, batch_size=64, validation_data=(X_valid, y_valid), callbacks=[CustomCallback(), early_stopping])

        self.model = model

        model.summary()
        
        results_train = model.evaluate(X_train, y_train, verbose=0)
        print(f"Train Loss: {results_train[0]:.4f}")
        print(f"Train Accuracy: {results_train[1]:.4f}")

        results_test = model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {results_test[0]:.4f}")
        print(f"Test Accuracy: {results_test[1]:.4f}")

        self.model.save(output_model_file_name)

    def read_normalization_bounds(self, input_bounds_file_name):
        '''
        Read the min and max values of the features for normalization.

        :param input_bounds_file_name: The name of the input bounds file.
        '''
        with open(input_bounds_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            min_vals = next(reader)
            max_vals = next(reader)

        return np.array(min_vals, dtype=float), np.array(max_vals, dtype=float)