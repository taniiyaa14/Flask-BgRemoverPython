from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

def process_image(input):
    inp = Image.open(input)
    inpp = remove(inp)
    image = inpp.convert("RGBA")

    background_color = (255, 255, 255)
    tolerance = 30

    new_data = [
        (255, 255, 255, 0) if all(abs(c - background_color[i]) <= tolerance for i, c in enumerate(item[:3])) else item
        for item in image.getdata()
    ]

    image.putdata(new_data)

    return image

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        input_file = request.files['imageUpload']
        processed_image = process_image(input_file)

        # Save processed image
        processed_image.save("static/images/img1.png")

        filename = secure_filename(input_file.filename)
        return render_template("index.html", filename=filename)
    
    return render_template("index.html")
