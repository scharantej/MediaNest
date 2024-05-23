
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename

import io
from PIL import Image
import numpy as np
import faiss
import torch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model = torch.hub.load('facebookresearch/deit:main', 'deit_base_patch16_224', pretrained=True)

# Load media items' vectors
vectors = np.load('media_vectors.npy')
index = faiss.IndexFlatL2(vectors.shape[1])  
index.add(vectors.astype(np.float32))

def encode_query(image_path):
    image = Image.open(image_path).resize((224, 224))
    image = np.array(image) / 255.0
    image = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)
    with torch.no_grad():
        embedding = model.forward_features(image).numpy()
    return embedding

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        query = request.files['query']
        if query:
            filename = secure_filename(query.filename)
            file_path = f'static/uploads/{filename}'
            query.save(file_path)
            query_vector = encode_query(file_path)
            distances, indices = index.search(query_vector.reshape(1, -1), 10)
            media_items = []
            for index in indices[0]:
                media_items.append({'id': index, 'distance': distances[0][index]})
            return render_template('home.html', media_items=media_items)
    return render_template('home.html')

@app.route('/media_item/<int:media_item_id>', methods=['GET'])
def media_item(media_item_id):
    return render_template('media_item.html', media_item_id=media_item_id)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
