#Import necessary libraries
from flask import Flask, render_template, request
 
import numpy as np
import os
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
 
#load model
model =load_model(r"\model\v3_pred_cott_dis.h5")
 
print('@@ Model loaded')
 
 
def pred_cot_dieas(cott_plant):
  test_image = load_img(cott_plant, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
   
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result = model.predict(test_image).round(3) # predict diseased palnt or not
  print('@@ Raw result = ', result)
   
  pred = np.argmax(result) # get the index of max value
 
  if pred == 0:
    return "Disease Cotton Plant"# if index 0 burned leaf
  elif pred == 1:
      return 'Diseased Cotton Plant' # # if index 1
  elif pred == 2:
      return 'Healthy Cotton Plant' # if index 2  fresh leaf
  else:
    return "Healthy Cotton Plant" 
 
#------------>>pred_cot_dieas<<--end
     
 
# Create flask instance
app = Flask(__name__)
 

     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        
 
        print("@@ Predicting class......")
        pred, output_page = pred_cot_dieas(cott_plant=filename)
               
        return render_template(output_page, pred_output = pred, user_image = file_path)
     
# For local system &amp; cloud
if __name__ == "__main__":
    app.run()
