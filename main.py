import os
import uuid
import base64
from flask import Flask, request, jsonify, send_from_directory, abort

app = Flask(__name__)


UPLOAD_FOLDER = '/screenshots'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Retrieve the base64 image from the request
        img_data = request.form['image']
        img_byte = base64.b64decode(img_data)

        # Generate a unique filename
        filename = f"screenshot_{str(uuid.uuid4())}.png"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the image to the server
        with open(file_path, 'wb') as f:
            f.write(img_byte)

        # Return the URL or path where the image is stored
        image_url = f"http://47.250.81.38:5010/uploads/{filename}"
        return jsonify({"image_url": image_url, "message": "Image uploaded successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/images', methods=['GET'])
def get_images():
    try:
        images = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.endswith('.png'):  # Adjust for your image formats
                image_url = f"http://47.250.81.38:5010/uploads/{filename}"
                images.append({"filename": filename, "image_url": image_url})
        return jsonify(images), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/image/<filename>', methods=['DELETE'])
def delete_image(filename):
    try:
        # Full path to the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": f"Image '{filename}' deleted successfully."}), 200
        else:
            return jsonify({"error": "Image not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    try:
        # Serve the image from the upload directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        abort(404)  # Return 404 if the file is not found


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010)
