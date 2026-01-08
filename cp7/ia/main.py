import classify
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'dat','tsv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(UPLOAD_FOLDER)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/config', methods=['POST'])
def doConfiguration():
    print("Configuration du modèle...")
    model_name = "mlp"
    if 'model' in request.form:
        model_name = request.form['model']
    elif 'model' in request.args:
        model_name = request.args['model']

    try:
        classify.config(model_name)
        return {"status": "ok", "message": f"Configuration du modèle {model_name} terminée"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.route('/predict', methods=['POST'])
def doClassification():
    print("Classification en cours...")

    if 'file' not in request.files:
        return {"status": "error", "message": "Aucun fichier n'a été envoyé"}, 400

    file = request.files['file']
    if not file or file.filename == '':
        return {"status": "error", "message": "Nom de fichier invalide"}, 400

    if not allowed_file(file.filename):
        return {"status": "error",
                "message": f"Type de fichier non autorisé. Extensions autorisées: {', '.join(ALLOWED_EXTENSIONS)}"}, 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    try:
        result = classify.classify(filename)
        return render_prediction_result(result)
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


def render_prediction_result(result):
    """Génère le HTML de résultat selon la prédiction"""
    if "error" in result:
        return {"status": "error", "message": result["error"]}, 500

    is_seismic = result["is_seismic"]
    probability = result["probability"] * 100  # Convertir en pourcentage
    value = result["value"]

    html = f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>{"SÉISME DÉTECTÉ" if is_seismic else "Pas de séisme"}</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                .result-box {{ 
                    padding: 30px; 
                    border-radius: 10px; 
                    display: inline-block;
                    margin: 20px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                .seismic {{ 
                    background-color: #ffcccc; 
                    color: #cc0000;
                    font-size: 48px;
                    font-weight: bold;
                }}
                .non-seismic {{ 
                    background-color: #ccffcc;
                    color: #006600;
                    font-size: 24px;
                }}
                .details {{ 
                    margin-top: 20px; 
                    font-size: 18px; 
                    color: #333; 
                }}
                .back-button {{
                    margin-top: 30px;
                    padding: 10px 20px;
                    background-color: #4285f4;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="result-box {'seismic' if is_seismic else 'non-seismic'}">
                {("SÉISME" if is_seismic else "PAS DE SÉISME")}
            </div>

            <div class="details">
                <p>Valeur analysée: <strong>{value}</strong></p>
                <p>Probabilité: <strong>{probability:.2f}%</strong></p>
            </div>

            <a href="/" class="back-button">Retour</a>
        </body>
    </html>
    '''

    return html


@app.route('/', methods=['GET'])
def doHome():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Détection de Séismes</title>
            <meta charset="UTF-8" />
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #333;
                    text-align: center;
                    border-bottom: 2px solid #ddd;
                    padding-bottom: 10px;
                }
                .section {
                    background-color: #f9f9f9;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                label {
                    display: block;
                    margin-bottom: 10px;
                    font-weight: bold;
                }
                select, input[type="file"] {
                    padding: 8px;
                    width: 100%;
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                input[type="submit"] {
                    background-color: #4285f4;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #3367d6;
                }
                .file-instructions {
                    font-size: 14px;
                    color: #666;
                    margin-top: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Détection de Séismes</h1>

            <div class="section">
                <h2>1. Configurer le modèle</h2>
                <form method="post" action="/config" enctype="application/x-www-form-urlencoded">
                    <label for="model">Choisir le type de modèle :</label>
                    <select name="model" id="model">
                        <option value="cnn">CNN (Réseau de Neurones Convolutifs)</option>
                        <option value="mlp" selected>MLP (Perceptron Multicouche)</option>
                        <option value="rnn">RNN (Réseau de Neurones Récurrents)</option>
                    </select>
                    <p class="file-instructions">Assurez-vous que les modèles existent dans le dossier ./models/ (cnn_seismic.keras, mlp_seismic.keras rnn_seismic.keras)</p>
                    <input type="submit" value="Configurer">
                </form>
            </div>

            <div class="section">
                <h2>2. Analyser un fichier</h2>
                <form method="post" action="/predict" enctype="multipart/form-data">
                    <label for="file">Importer un fichier (txt, csv, dat) contenant une seule valeur :</label>
                    <input type="file" name="file" id="file">
                    <p class="file-instructions">Le fichier doit contenir uniquement une valeur numérique (par exemple: 0.82)</p>
                    <input type="submit" value="Analyser">
                </form>
            </div>
        </body>
    </html>
    '''


if __name__ == '__main__':
    print("Démarrage du serveur...")
    if not os.path.exists("/app/saves/models"):
        print(
            "ATTENTION: Le dossier ./models n'existe pas. Veuillez le créer et y placer vos modèles (cnn_seismic.keras, mlp_seismic.keras, rnn_seismic.keras)")
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
    print("Serveur arrêté")