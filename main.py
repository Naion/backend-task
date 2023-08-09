from flask import Flask, request, abort
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from os import listdir
from os.path import isfile, join
import uuid
import base64

app = Flask(__name__)
CORS(app)

#Function that returns a converted version of an image to base64, parameters needed such as an image and its extension.
def image_to_base64(image, extension):
    buff = BytesIO()
    image.save(buff, format=extension)
    img_str = base64.b64encode(buff.getvalue())
    return img_str

@app.route("/")
def hello_wolrd():
  return "<p>Test BackEnd</p>"

@app.post("/upload_image")
def upload_image():
  #Accepted image file types.
  fileTypes = ['jpg', 'jpeg', 'png']
  #Retrieving and parsin file information into JSON format.
  json = request.json
  #Generating a unique ID for the uploaded image.
  unique_id = str(uuid.uuid4())
  json_string = json['base64']
  extension = json['extension']
  #Removing header from the string to avoid decoding errors.
  removed_header = json_string.split(",")[1]
    # Converting string in base64 to image and saving on filesystem
    # Added "+ '==' to handle "binascii.Error: Incorrect padding", base64 will truncate any unnecessary
    # padding characters
  imgdata = base64.b64decode(removed_header + '==')
  filename = f'./images/{unique_id}.{extension}'
  if extension in fileTypes:
    with open(filename, 'wb') as f:
      f.write(imgdata)
  else:
    #Handling error «415 Unsupported Media Type» in case user upload unsupported type, another error filter is
    #at the front-end side to prevent the server from overworking. This will be used in case the user manages
    #to upload unsupported media type via scripting or hardcoding.
    abort(415)
  return {"extension" : extension, "uuid" : unique_id}

@app.post("/analyse_image")
def analyse_image():
  #Searching the stored image given its ID.
  filepath = f"./images/{request.json['uuid']}"
  img = Image.open(filepath)
  #Converting to Base64 before returning the data in order to print it on DOM.
  img2 = image_to_base64(img, 'PNG')
  return {"height" : img.height, "width" : img.width, "base64" : img2.decode()}

@app.get("/list_images")
def list_images():
  base64files = []
  d = []
  #Iterate through each stored file in the image directory.
  files = [f for f in listdir("./images/") if isfile(join("./images/", f))]
  for file in files:
    #Getting the path and converting the image to Base64 plus adding to dictionary the requiered file information.
    filepath = f"./images/{file}"
    img = Image.open(filepath)
    img2 = image_to_base64(img, 'PNG')
    base64files.append(img2.decode())
    d.append({"base64" : img2.decode(), "uuid" : file})
  return d

if __name__ == '__main__':
  app.run(debug=True)