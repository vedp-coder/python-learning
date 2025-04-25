import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import matplotlib.pyplot as plt

class ImageClassifier:
    def __init__(self):
        # Load pre-trained MobileNetV2 model
        self.model = MobileNetV2(weights='imagenet')
        print("Model loaded successfully!")
        
    def classify_image(self, img_path):
        # Load and preprocess the image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Make predictions
        predictions = self.model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=5)[0]
        
        return decoded_predictions, img
    
    def display_results(self, img_path):
        # Get predictions and image
        predictions, img = self.classify_image(img_path)
        
        # Display image and predictions
        plt.figure(figsize=(10, 5))
        
        # Display image
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.axis('off')
        plt.title('Input Image')
        
        # Display predictions
        plt.subplot(1, 2, 2)
        y_pos = np.arange(len(predictions))
        labels = [pred[1] for pred in predictions]
        scores = [pred[2] for pred in predictions]
        
        plt.barh(y_pos, scores, align='center')
        plt.yticks(y_pos, labels)
        plt.xlabel('Probability')
        plt.title('Top 5 Predictions')
        
        plt.tight_layout()
        plt.show()
        
        # Print predictions
        print("\nTop predictions:")
        for i, (imagenet_id, label, score) in enumerate(predictions):
            print(f"{i+1}: {label} ({score:.2f})")

def main():
    classifier = ImageClassifier()
    
    while True:
        print("\nImage Classification Menu:")
        print("1. Classify an image")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == '1':
            img_path = input("\nEnter path to image: ")
            try:
                classifier.display_results(img_path)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            print("Thank you for using the Image Classifier!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
