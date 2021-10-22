from fer import FER
import cv2
from tkinter import messagebox
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

def img_capture():
    try:
        camera = cv2.VideoCapture(0)
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite('test.jpg',image)
        camera.release()
        cv2.destroyAllWindows()
    except:
        messagebox.showwarning("Warning", "No camera device detected!")

def img_enhance():
    img = Image.open("test.jpg")
    enhancer = ImageEnhance.Brightness(img)

    factor = 1.5
    im_output = enhancer.enhance(factor)
    im_output.save("test.jpg")

def detect_emotion():
    for x in range(10):
        img = plt.imread('test.jpg')
        detector = FER(mtcnn=True)
        plt.imshow(img)

        try:
            emotion, score = detector.top_emotion(img)
            return emotion
        except:
            img_enhance()

    if(x == 10):
        messagebox.showwarning("Warning", "No face detected")
    return 0


