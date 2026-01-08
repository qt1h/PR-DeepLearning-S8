import csv
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf

import os
normalizer = tf.keras.layers.Normalization()

@tf.keras.utils.register_keras_serializable()
def tversky_loss(alpha=0.2, beta=0.8, smooth=1e-6):
    @tf.keras.utils.register_keras_serializable()    
    def loss(y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, smooth, 1 - smooth)
        y_true_f = tf.reshape(y_true, [-1])
        y_pred_f = tf.reshape(y_pred, [-1])
        TP = tf.reduce_sum(y_true_f * y_pred_f)
        FP = tf.reduce_sum((1 - y_true_f) * y_pred_f)
        FN = tf.reduce_sum(y_true_f * (1 - y_pred_f))
        T  = (TP + smooth) / (TP + alpha*FN + beta*FP + smooth)
        return 1 - T
    return loss

# Variables globales
current_model = None
model_type = None  # 'cnn', 'mlp', ou 'rnn'

# Chemins des modèles
model_paths = {
    "cnn": "/app/saves/models/cnn_seismic.keras",
    "mlp": "/app/saves/models/mlp_seismic.keras",
    "rnn": "/app/saves/models/rnn_seismic.keras"
}


def config(model_name):
    """Configure le modèle à utiliser pour la prédiction"""
    global current_model, model_type

    if model_name not in ["cnn", "mlp", "rnn"]:
        raise ValueError(f"Modèle inconnu: {model_name}. Choisissez parmi 'cnn', 'mlp', 'rnn'")

    model_type = model_name
    model_path = model_paths[model_name]

    try:
        if model_name == "mlp" and os.path.exists(model_path):
            # Utilisation de la Tversky loss pour le MLP
            current_model = load_model(
                model_path,
                custom_objects={'tversky_loss': tversky_loss()}
            )
            print(f"Modèle MLP chargé depuis {model_path} avec Tversky loss")

        if os.path.exists(model_path):
            current_model = load_model(model_path)
            print(f"Modèle {model_name} chargé depuis {model_path}")
        else:
            raise FileNotFoundError(
                f"Le modèle {model_name} n'existe pas à l'emplacement {model_path}. Veuillez fournir ce modèle.")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")
        raise


def classify(file_path):
    """Classifie un fichier contenant une seule valeur en séisme (1) ou non (0)"""
    global current_model, model_type

    if current_model is None:
        raise ValueError("Aucun modèle n'a été configuré. Appelez d'abord config().")

    try:
        with open(file_path, 'r') as f:
            text = f.read().strip()

        parts = text.split(',')

        try:
            values = [float(x) for x in parts]
        except ValueError as ve:
            raise ValueError(f"Impossible de convertir toutes les valeurs en float: {ve}")
        
        # Prétraitement selon le type de modèle
        
        if model_type == "cnn":
            arr = np.array(values).reshape(1, -1)

            x_norm = normalizer(arr)

            input_data = np.expand_dims(x_norm, axis=-1)

        elif model_type == "mlp":
             
            x = np.array([values])
            input_data=normalizer(x)

        elif model_type == "rnn":
            input_data = np.array([values])
        else:
            raise ValueError(f"Type de modèle non pris en charge: {model_type}")

        prediction = current_model.predict(input_data)

        # Classification binaire avec seuil à 0.5
        is_seismic = bool(prediction[0][0] > 0.5)

        result = {
            "is_seismic": is_seismic,
            "probability": float(prediction[0][0]),
            "value": values
        }

        return result

    except Exception as e:
        print(f"Erreur lors de la classification: {e}")
        return {"error": str(e)}