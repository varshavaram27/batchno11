from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename



app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

static_path = 'static'
app.config['IMAGE_UPLOADS'] = static_path



model_path2 = 'xce.h5' # load .h5 Model

CTS = load_model(model_path2)
from keras.preprocessing.image import load_img, img_to_array

def model_predict2(image_path,model):
	print("Predicted")
	image = load_img(image_path,target_size=(224,224))
	image = img_to_array(image)
	image = image/255
	image = np.expand_dims(image,axis=0)
	
	main=model.predict(image)
	main=str(main)
	def string_to_list_of_ints(string):
		string=string[2:]
		string=string[:-2]
		return list( string.split(' '))
	a=string_to_list_of_ints(main)
	print(type(a))
	a1=round(float(a[0]),2)
	b=round(float(a[1]),2)        
	if a1>= 0.89:
		return "Basal cell Carcinoma","after.html"
	elif b>= 0.21:
		return "Melanoma Disease","after.html"
	else:
		return "Squamous Cell Carcinoma","after.html"


# routes
@app.route("/", methods=['GET', 'POST'])
def kuch_bhi():
	return render_template("home.html")

@app.route("/about")
def about_page():
	return "About You..!!!"

@app.route("/submit", methods = ['GET', 'POST'])
def get_hours():
	if request.method == 'POST':
		print("Entered")
    
		print("Entered here")
		file = request.files['my_image'] # fet input
		filename = file.filename        
		print("@@ Input posted = ", filename)
			
		file_path = os.path.join(UPLOAD_FOLDER, filename)
		file.save(file_path)

		print("@@ Predicting class......")
		pred, output_page = model_predict2(file_path,CTS)
		


	return render_template(output_page, pred_output = pred, img_src=UPLOAD_FOLDER + file.filename)





if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)