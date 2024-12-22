from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
from PIL import Image
from function import download_zip

app = Flask(__name__)
app.static_folder = 'static'

model = YOLO(r'best.pt')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'images[]' not in request.files:
            message = {
                'error': "No image uploaded!",
                'success': False
            }
            return jsonify(message)
        if request.files['images[]'].filename == '':
            message = {
                'error': "No image selected!",
                'success': False
            }
            return jsonify(message)
        
        # Apple Counting
        n_images = 0
        bacterial_spot = 0
        early_blight = 0
        healthy = 0
        late_blight = 0
        leaf_miner = 0
        leaf_mold = 0
        mosaic_virus = 0
        septoria = 0
        spider_mites = 0
        yellow_leaf_curl_virus = 0
        no_identity = 0

        img_path = "static/predict/img/"
        img_results = []

        files = request.files.getlist('images[]')

        for i, file in files:
            if file:
                n_images += 1

                filename = "Leaf_" + str(i) + ".jpg"
                image_path = img_path + filename
                file.save(image_path)

                results = model(image_path)

                for i, r in enumerate(results):
                    boxes = r.boxes
                    for cls in boxes.cls:
                        if(cls == 0):
                            bacterial_spot += 1
                        elif(cls == 1):
                            early_blight += 1
                        elif(cls == 2):
                            healthy += 1
                        elif(cls == 3):
                            late_blight += 1
                        elif(cls == 4):
                            leaf_miner += 1
                        elif(cls == 5):
                            leaf_mold += 1
                        elif(cls == 6):
                            mosaic_virus += 1
                        elif(cls == 7):
                            septoria += 1
                        elif(cls == 8):
                            spider_mites += 1
                        elif(cls == 9):
                            yellow_leaf_curl_virus += 1
                        else:
                            no_identity += 1
                    
                    im_bgr = r.plot()  
                    im_rgb = Image.fromarray(im_bgr[..., ::-1]) 

                    img_results.append(image_path)
                    im_rgb.save(image_path)

                os.remove(image_path)

        message = {
                'success': True,
                'img_results': img_results,
                'n_images': n_images,
                'bacterial_spot': bacterial_spot,
                'early_blight': early_blight,
                'healthy': healthy,
                'late_blight': late_blight,
                'leaf_miner': leaf_miner,
                'leaf_mold': leaf_mold,
                'mosaic_virus': mosaic_virus,
                'septoria': septoria,
                'spider_mites': spider_mites,
                'yellow_leaf_curl_virus': yellow_leaf_curl_virus,
                'no_identity': no_identity
            }
        return jsonify(message)
    else:
        message = {
                'success': False,
                'error': "You don't have access with this page!"
            }
        return jsonify(message)
    
@app.route('/predict_download', methods=['POST'])
def predict_download():
    file_list = request.form.getlist('img_results[]')

    zs = []
    for file in file_list:
        zs.append(file)

    return download_zip(zs)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=False, port=5000, host='0.0.0.0', threaded = True)