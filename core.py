
from tensorflow.keras.preprocessing.image import load_img , img_to_array


class Detection():

    def __init__(self, dir=None):
        self.dir = dir
        self.classes = [ 'Actinic Keratoses', 'Basal Cell Carcinoma', 
                        'Benign Keratosis', 'Dermatofibroma', 
                        'Melanoma', 'Melanocytic Nevi', 
                        'Vascular naevus']

    # Image Resizing
    def resize_img(self, filename, size=(224, 224)):
        img = load_img(filename , target_size = size)
        img = img_to_array(img)
        img = img.reshape(1,224,224,3)
        img = img.astype('float32')
        img = img/255.0
        return img
    
    # Model Prediction
    def predict(self, img, model):
        result = model.predict(img)
        dict_result = {}
        for i in range(len(self.classes)):
            dict_result[result[0][i]] = self.classes[i]
        
        res = result[0]
        res.sort()
        res = res[::-1]
        prob = res[:3]
        prob_result = []
        class_result = []
        for i in range(3):
            prob_result.append((prob[i]*100).round(2))
            class_result.append(dict_result[prob[i]])
        return class_result , prob_result


