import os
import cv2
import joblib
import numpy as np
import tensorflow as tf
import efficientnet.keras

from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request,'index.html')

def upload(request):
    return render(request,'upload.html')



svm_model_path = os.path.join('model/svm_model.joblib')


#svm_model_path = os.path.join('model/svm_model_updated.joblib')
list_of_classes  = ['Corn Common Rust', 'Corn Healthy', 'Potato Healthy',  'Potato Late Blight', 'Rice Brown Spot','Rice Healthy']
#list_of_classes  = ['Rice Brown Spot', 'Corn Common Rust', 'Rice Healthy', 'Corn Healthy', 'Potato Late Blight', 'Potato Healthy']

def load_model():
    with open('model/efficientnet_b0_model.json', 'r') as json_file:


    #with open('model/enet_updated.json', 'r') as json_file:

        loaded_model_json = json_file.read()
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)


    # Load the weights
    loaded_model.load_weights(os.path.join('model/efficientnet_b0_model.h5'))


    #loaded_model.load_weights(os.path.join('model/efficientnet_b0_model_updated.h5'))

    loaded_svm_model = joblib.load(svm_model_path)
    return loaded_model, loaded_svm_model



def predict(image_path, model, svm_model):
    img = cv2.imread(image_path)
    #img_resized = cv2.resize(img, (224, 224))
    img_resized = cv2.resize(img, (224, 224))
    img_resized = img_resized.astype('float32') / 255.0
    img_resized = np.expand_dims(img_resized, axis=0)

    pred = model.predict(img_resized)
    new_data_flat = pred.reshape(1, -1)
    prediction = svm_model.predict(new_data_flat)[0]

    probability = np.max(pred)
    return list_of_classes[prediction], probability


def predict_crop_disease(request):
    loaded_model, loaded_svm_model = load_model()

    if request.method == 'POST' and request.FILES['image']:
        # Save the uploaded image
        uploaded_file = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, 'image.jpg')

        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
   

        # Perform prediction using Streamlit code

        prediction, probability = predict(image_path, loaded_model, loaded_svm_model)



        # Render the result using a Django template
        if prediction in [ 'Corn Common Rust','Rice Brown Spot', 'Potato Late Blight']:
            result = f"Prediction : {prediction}"
            new_Accuracy = probability - 0.0278
            Accuracy = f"Accuracy : {new_Accuracy* 100:.2f}"
        else:
            result = f"Prediction : {prediction}"
            new_Accuracy = probability - 0.0278
            Accuracy = f"Accuracy : {new_Accuracy* 100:.2f}"

        
       
        accuracy_value = float(new_Accuracy * 100)
        accuracy_status = "Invalid_Image" if accuracy_value < 63.45 else "valid"


        return render(request, 'result.html', {'result': result, 'Accuracy': Accuracy, 'invalide': accuracy_status})
    else:
        return render(request, 'upload.html')
   
    
   
    

