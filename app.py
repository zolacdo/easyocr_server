# app.py
from flask import Flask, request, jsonify
import easyocr
import tempfile
import os

app = Flask(__name__)

# Charger le lecteur EasyOCR une seule fois (optimisation)
# 'fr' pour le français, 'en' si tu veux du bilingue
reader = easyocr.Reader(['fr'], gpu=False)  # gpu=False pour hébergement gratuit

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image fournie'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Fichier vide'}), 400

    try:
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        # Reconnaissance OCR
        results = reader.readtext(tmp_path, detail=0)  # detail=0 → juste le texte
        full_text = '\n'.join(results)

        # Nettoyer le fichier temp
        os.unlink(tmp_path)

        return jsonify({
            'text': full_text,
            'success': True
        })

    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# Route de santé (pour les services d'hébergement)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))