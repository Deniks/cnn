import numpy as np
import cv2
import os

cam = cv2.VideoCapture(0)
s, img = cam.read()
if s:
 #   cv2.namedWindow("cam-test")
#    cv2.imshow("cam-test", img)
#    cv2.waitKey(0)
 #   cv2.destroyWindow("cam-test")
    cv2.imwrite(os.path.join('/c/Users/rezan/Desktop/windows_protocter_spyware', 'face.jpg'), img)

def dataset():
    images = []
    labels = []
    labels_dic = {}
    people = [person for person in os.listdir("people/")]
    for i, person in enumerate(people):
            labels_dic[i] = person
            for image in os.listdir("people/" + person):
                    images.append(cv2.imread("people/" + person + '/' + image, 0))
                    labels.append(person)
       
    return (images, np.array(labels), labels_dic)

images, labels, labels_dic = dataset()

class FaceDetector(object):
    def __init__(self, xml_path):
        self.classifier = cv2.CascadeClassifier(xml_path)
    
    def detect(self, image, biggest_only=True):
        scale_factor = 1.2
        min_neighbors = 5
        min_size = (30, 30)
        biggest_only = True
        faces_coord = self.classifier.detectMultiScale(image,
                                                       scaleFactor=scale_factor,
                                                       minNeighbors=min_neighbors,
                                                       minSize=min_size,
                                                       flags=cv2.CASCADE_SCALE_IMAGE)
        return faces_coord

def cut_faces(image, faces_coord):
    faces = []
    
    for (x, y, w, h) in faces_coord:
        w_rm = int(0.3 * w / 2)
        faces.append(image[y: y + h, x + w_rm: x + w - w_rm])
         
    return faces

def resize(images, size=(224, 224)):
    images_norm = []
    for image in images:
        if image.shape < size:
            image_norm = cv2.resize(image, size, 
                                    interpolation=cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(image, size, 
                                    interpolation=cv2.INTER_CUBIC)
        images_norm.append(image_norm)

    return images_norm



def normalize_faces(image, faces_coord):

    faces = cut_faces(image, faces_coord)
    faces = resize(faces)
    
    return faces
  
for image in images:
    detector = FaceDetector("haarcascade_frontalface_default.xml")
    faces_coord = detector.detect(image, True)
    faces = normalize_faces(image ,faces_coord)
    for i, face in enumerate(faces):
            cv2.imwrite('%s.jpeg' % (count), faces[i])
            count += 1  


"""
if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    while 1:
        _,frame =cam.read()
        #image_faces = []
        image_faces = detect(frame)
        console.log(image_faces)
        cv2.imwrite("face-" + str(1) + ".jpg", 'denis')
        #for i, face in enumerate(image_faces):
        #   cv2.imwrite("face-" + str(i) + ".jpg", face)

        #cv2.imshow("features", frame)
        if cv2.waitKey(1) == 0x1b: # ESC
            print('ESC pressed. Exiting ...')
            break

"""