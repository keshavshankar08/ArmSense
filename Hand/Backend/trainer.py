import sys
sys.path.append('.')

import csv
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import datetime

class Trainer:
    def __init__(self):
        '''
        Initialize the Trainer with the default file name and an empty model.
        '''
        self.model = None
        self.model_file_path = "Hand/Backend/Resources/model.h5"
        self.feature_data_file_name = "Hand/Backend/Resources/feature_data.csv"
        self.processed_data_file_name = "Hand/Backend/Resources/processed_data.csv"
        self.normalization_bounds_file_name = "Hand/Backend/Resources/normalization_bounds.csv"

    def process_data(self):
        '''
        Clean and normalize the features in the data file and store min and max values.
        '''
        cleaned_data = []
        with open(self.feature_data_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if not any(cell == 'nan' for cell in row):
                    cleaned_data.append(row)

        data = np.array(cleaned_data, dtype=float)
        features = data[:, :-1]
        labels = data[:, -1]

        min_vals = features.min(axis=0)
        max_vals = features.max(axis=0)
        normalized_features = (features - min_vals) / (max_vals - min_vals + 1e-8)

        normalized_data = np.hstack((normalized_features, labels.reshape(-1, 1)))
        normalized_data = np.array([[float(f"{cell:.2f}") for cell in row] for row in normalized_data])

        with open(self.processed_data_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(normalized_data)

        with open(self.normalization_bounds_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(min_vals)
            writer.writerow(max_vals)

    def train_model(self):
        '''
        Train a model using the data in the data file.

        :param input_data_file_name: The name of the input data file.
        :param output_model_file_name: The name of the output model file.
        '''
        data = []
        with open(self.processed_data_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

        data = np.array(data, dtype=float)
        features = data[:, :48]
        labels = data[:, 48]

        X_train, X_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.2, random_state=42)
        X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(shape=(48,)),
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

        self.model.save(self.model_file_path)