from flask import Flask,render_template,request,redirect,url_for
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        input=request.files['imageUpload']
        inp=Image.open(input)
        inpp=remove(inp)
        image=inpp.convert("RGBA")
        data = image.getdata()
        new_data = []
        background_color = (255, 255, 255)
        tolerance = 30
        for item in data:
            if all(abs(c - background_color[i]) <= tolerance for i, c in enumerate(item[:3])):
                new_data.append((255, 255, 255, 0)) 
            else:
                new_data.append(item)

        image.putdata(new_data)

        image.save("static/images/img1.png")

        filename=secure_filename(input.filename)
        return render_template("index.html",filename=filename)
    return render_template("index.html")


