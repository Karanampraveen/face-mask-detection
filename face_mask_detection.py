# -*- coding: utf-8 -*-
"""face-mask-detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TLuShWJpSw-THJHLLeZuCOCX1ab4ekWh
"""

from google.colab import drive
drive.mount('/content/drive')

pip install tensor

import tensorflow as tf
import numpy as np

width = 224
height = 224
batch_size = 32
data_dir = r"/content/drive"

training = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,             # Directory containing the images
    validation_split=0.3,  # Fraction of the dataset to use for validation
    subset='training',     # Use this subset for training
    seed=123,              # Seed for reproducibility
    image_size=(height, width),  # Size to resize the images to
    batch_size=batch_size  # Number of samples per batch
)

classes = training.class_names
classes

training

import matplotlib.pyplot as plt

# Assuming you have 'training' and 'classes' defined somewhere in your code

for images, labels in training.take(1):
    plt.imshow(images[1].numpy().astype('uint8'))
    plt.title(classes[labels[1]])

plt.show()

from tensorflow.keras.applications import MobileNetV2

model = MobileNetV2(weights='imagenet')

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.summary()

face_mask_detection = model.fit(training,epochs=3)

import tensorflow as tf

# Define the target size (height, width)
height, width = 224, 224  # Adjust these values based on your model's input size

# Load the image
img = tf.keras.preprocessing.image.load_img('/content/new.jpg', target_size=(height, width))

# Convert the image to an array
image_array = tf.keras.preprocessing.image.img_to_array(img)

# Expand dimensions to fit in the model
image_array = tf.expand_dims(image_array, 0)

# Check the shape of the image
print(image_array.shape)

predictions = model.predict(image_array)
score = tf.nn.softmax(predictions[0])

print(score)

model.save("dummy.model")

import tensorflow as tf

# Load the saved Keras model
model = tf.keras.models.load_model("dummy.model")

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open("dummy.tflite", "wb") as f:
    f.write(tflite_model)

from tensorflow.keras.models import load_model
detector = load_model("dummy.model")

# Clone the OpenCV repository
!git clone https://github.com/opencv/opencv.git

# Create a directory named "Video"
!mkdir Video

!pip install ffmpeg-python

from IPython.display import HTML, Javascript, display
from google.colab.output import eval_js
from base64 import b64decode
import numpy as np
import io
import ffmpeg

video_file_test = '/content/Video/osy_test.mp4'

# HTML and JavaScript code for video recording button
VIDEO_HTML = """
<script>
var my_div = document.createElement("DIV");
var my_p = document.createElement("P");
var my_btn = document.createElement("BUTTON");
var my_btn_txt = document.createTextNode("Press to start recording");
my_btn.appendChild(my_btn_txt);
my_div.appendChild(my_btn);
document.body.appendChild(my_div);

var base64data = 0;
var reader;
var recorder, videoStream;

var handleSuccess = function(stream) {
    videoStream = stream;

    var options = {
        mimeType: 'video/webm; codecs=vp9'
    };

    recorder = new MediaRecorder(stream, options);

    recorder.ondataavailable = function(e) {
        var url = URL.createObjectURL(e.data);
        var preview = document.createElement('video');
        preview.controls = true;
        preview.src = url;
        document.body.appendChild(preview);

        reader = new FileReader();
        reader.readAsDataURL(e.data);

        reader.onloadend = function() {
            base64data = reader.result;
        };
    };

    recorder.start();
};

var recordButton = my_btn;
recordButton.innerText = "Press to start recording";

navigator.mediaDevices.getUserMedia({ video: true }).then(handleSuccess);

function toggleRecording() {
    if (recorder && recorder.state == "recording") {
        recorder.stop();
        videoStream.getVideoTracks()[0].stop();
        recordButton.innerText = "Saving the recording. Please wait!";
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

var data = new Promise(resolve => {
    recordButton.onclick = () => {
        toggleRecording();
        sleep(2000).then(() => {
            // wait 2000ms for the data to be available
            resolve(base64data.toString());
        });
    };
});
</script>
"""

display(HTML(VIDEO_HTML))

def start_webcam():
    js_code = '''
    async function startWebcam() {
        const div = document.createElement('div');
        const video = document.createElement('video');
        video.style.display = 'block';

        const stream = await navigator.mediaDevices.getUserMedia({ video: true });

        document.body.appendChild(div);
        div.appendChild(video);
        video.srcObject = stream;
        await video.play();

        // Resize the output to fit the video element.
        google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
        return;
    }
    '''

    js = Javascript(js_code)
    display(js)

    eval_js('startWebcam()')

def get_video():
    # Assuming VIDEO_HTML is defined elsewhere in your code
    display(HTML(VIDEO_HTML))

    # Execute JavaScript code to get the recorded video data
    data = eval_js('data')

    # Decode base64 data to binary
    binary_data = b64decode(data.split(',')[1])

    return binary_data

# Call start_webcam to display the webcam feed
start_webcam()

# Call get_video to retrieve the recorded video data
recorded_video_data = get_video()

import io

videofile = get_video()
with open(video_file_test, 'wb') as file:
  file.write(videofile)

import tensorflow as tf
import cv2

# Define the path to the Haar Cascade XML file
haarcascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

# Starting the video stream
video_file_test = '/content/Video/osy_test.mp4'
cap = cv2.VideoCapture(video_file_test)

# Using the Haar Cascade Classifier
classifier = cv2.CascadeClassifier('https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml')

from google.colab.patches import cv2_imshow

from google.colab.patches import cv2_imshow
import tensorflow as tf
import cv2
import numpy as np

# Load the face mask detection model
detector = tf.keras.models.load_model('dummy.model')  # Replace with the actual path to your model

# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the video stream
video_file_test = '/content/Video/osy_test.mp4'
cap = cv2.VideoCapture(video_file_test)

score = None
label = None

while True:
    # Read the frame from the stream
    success, frame = cap.read()

    if not success:
        break

    # Resize the frame to speed up processing
    new_image = cv2.resize(frame, (frame.shape[1] // 1, frame.shape[0] // 1))

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        try:
            # Get the coordinates for the detected face
            face_img = new_image[y:y+h, x:x+w]

            # Resize the face to fit into the model
            resized = cv2.resize(face_img, (224, 224))

            # Convert the detected image into an array
            image_array = tf.keras.preprocessing.image.img_to_array(resized)

            # Expand the dimensions to fit in the model
            image_array = tf.expand_dims(image_array, 0)

            # Make predictions on the ROI
            predictions = detector.predict(image_array)

            # Get the results
            score = tf.nn.softmax(predictions[0])
            label = np.argmax(score)

        except Exception as e:
            print('Bad frame')


        # Draw rectangle and label based on the prediction
        if label == 0:
            cv2.rectangle(new_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(new_image, "Mask", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        elif label == 1:
            cv2.rectangle(new_image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(new_image, 'No Mask', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            None
    # Display the frame
    cv2_imshow(new_image)

    # Print the prediction and confidence

    print(np.argmax(score))

    # Waitkey to terminate the loop
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

# Release the video stream
cap.release()
cv2.destroyAllWindows()

from google.colab.patches import cv2_imshow
import tensorflow as tf
import cv2
import numpy as np

# Load the face mask detection model
detector = tf.keras.models.load_model('dummy.model')  # Replace with the actual path to your model

# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

score = None
label = None

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame to speed up processing
    new_image = cv2.resize(frame, (frame.shape[1] // 1, frame.shape[0] // 1))

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        try:
            # Get the coordinates for the detected face
            face_img = new_image[y:y+h, x:x+w]

            # Resize the face to fit into the model
            resized = cv2.resize(face_img, (224, 224))

            # Convert the detected image into an array
            image_array = tf.keras.preprocessing.image.img_to_array(resized)

            # Expand the dimensions to fit in the model
            image_array = tf.expand_dims(image_array, 0)

            # Make predictions on the ROI
            predictions = detector.predict(image_array)

            # Get the results
            score = tf.nn.softmax(predictions[0])
            label = np.argmax(score)

        except Exception as e:
            print('Bad frame')

        # Draw rectangle and label based on the prediction
        if label == 0:
            cv2.rectangle(new_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(new_image, "Mask", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        elif label == 1:
            cv2.rectangle(new_image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(new_image, 'No Mask', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            None

    # Display the frame
    cv2_imshow(new_image)

    # Print the prediction and confidence
    print(np.argmax(score))

    # Terminate the loop if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the video stream
cap.release()
cv2.destroyAllWindows()

