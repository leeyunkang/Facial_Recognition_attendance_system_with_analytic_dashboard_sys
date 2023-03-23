# 从人脸图像文件中提取人脸特征存入 "features_all.csv" / Extract features from images and save into "features_all.csv"

import os
import dlib
import csv
import numpy as np
import logging
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model


# 要读取人脸图像文件的路径 / Path of cropped faces
path_images_from_camera = "faces_recognition/data/data_faces_from_camera/"


# Dlib 正向人脸检测器 / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()
#detector = load_model('training_model/facetracker.h5')


# Dlib 人脸 landmark 特征点检测器 / Get face landmarks
predictor = dlib.shape_predictor('faces_recognition/data/data_dlib/shape_predictor_68_face_landmarks.dat')


# Dlib Resnet 人脸识别模型，提取 128D 的特征矢量 / Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("faces_recognition/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")



# 返回单张图像的 128D 特征 / Return 128D features for single image
# Input:    path_img           <class 'str'>
# Output:   face_descriptor    <class 'dlib.vector'>
def return_128d_features(path_img):
    img_rd = cv2.imread(path_img)
    faces = detector(img_rd, 1)
    

    #img_rd1 = img_rd[50:500, 50:500,:]
    '''
    img_rd12 = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    img_rd1 = tf.image.resize(img_rd12, (120,120))

    img_rd1 = np.expand_dims(img_rd1/255, axis=0)

    img_rd1 = np.reshape(img_rd1, (-1, 120, 120, 3))
    yhat = detector.predict(img_rd1)
    sample_coords = yhat[1][0]

    if yhat[0] > 0.7:
        image_height, image_width, _ = img_rd.shape

        rectangle_coords = dlib.rectangles()
        rectangle_coords.append(dlib.rectangle(
            int(sample_coords[0] * image_width),
            int(sample_coords[1] * image_height),
            int(sample_coords[2] * image_width),
            int(sample_coords[3] * image_height)
        ))
        faces = rectangle_coords
        print(type(faces[0]))
        print(faces[0])
'''
        # Assuming img_rd is the image
        #rectangle_width = int((sample_coords[2] - sample_coords[0]) * img_rd.shape[1])
        #rectangle_height = int((sample_coords[3] - sample_coords[1]) * img_rd.shape[0])
        #faces = rectangle_width * rectangle_height

        #height, width, _ = img_rd.shape
        #scaled_coords = np.multiply(sample_coords, [width, height, width, height]).astype(int)
        #values = [(scaled_coords[0], scaled_coords[1]), (scaled_coords[2], scaled_coords[3])]
        #faces = tuple(values)
        #faces = type(dlib.rectangles)
        #faces = scaled_coords[0]
        #print("faces",faces)
        #x1, y1, x2, y2 = np.multiply(sample_coords, [img_rd1.shape[1], img_rd1.shape[0], img_rd1.shape[1], img_rd1.shape[0]]).astype(int)
        #faces = img_rd[y1:y2, x1:x2]
        
    
    #print(faces)
    '''
    print (roi )
    print("Type:", type(roi))
    print (img_rd )
    print("Type:", type(img_rd))

    
    print(faces)
    # Get the type of the array
    print("Type:", type(faces))

    # Get the shape of the array
    #print("Shape:", faces.shape)
 
    
    rgb = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    img_rd2= tf.image.resize(rgb, (120,120))
    #img_rd1 = np.expand_dims(img_rd2/255,0)
    yhat = detector.predict(np.expand_dims(img_rd2/255,0))
    sample_coords = yhat[1][0]
    # Get the type of the array
    print("Type:", type(img_rd))

    # Get the shape of the array
    print("Shape:", img_rd.shape)

    '''
    '''
    if yhat[0]> 0.90: 



        top_left = (int(sample_coords[0] * 120), int(sample_coords[1] * 120))
        bottom_right = (int(sample_coords[2] * 120), int(sample_coords[3] * 120))

        cv2.rectangle(np.expand_dims(img_rd/255,0), top_left, bottom_right, (255, 0, 0), 2)
        
        rect = dlib.rectangle(*top_left, *bottom_right)
        rectangles.append(rect)
       
        x1, y1, x2, y2 = np.multiply(sample_coords, [img_rd.shape[1], img_rd.shape[0], img_rd.shape[1], img_rd.shape[0]]).astype(int)
        #x1, y1, x2, y2 = np.multiply(sample_coords, [500, 500, 500, 500]).astype(int)

        #roi = img_rd[y1:y2, x1:x2]
        # Create a _dlib_pybind11.rectangles object from the rectangle coordinates
        rects = dlib.rectangles([dlib.rectangle(x1, y1, x2, y2)])
        faces =rects
    else:
        faces=[]
    '''
    logging.info("%-40s %-20s", "检测到人脸的图像 / Image with faces detected:", path_img)

    # 因为有可能截下来的人脸再去检测，检测不出来人脸了, 所以要确保是 检测到人脸的人脸图像拿去算特征
    # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
    if len(faces) != 0:
        '''
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)

        # Assuming `img_rd` is a TensorFlow EagerTensor object representing an RGB image
        img_rd = img_rd.numpy()

        # Convert the array to an 8-bit RGB image
        img_rd = (img_rd * 255).astype(np.uint8)
        '''

        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        logging.warning("no face")
    return face_descriptor


# 返回 personX 的 128D 特征均值 / Return the mean value of 128D face descriptor for person X
# Input:    path_face_personX        <class 'str'>
# Output:   features_mean_personX    <class 'numpy.ndarray'>
def return_features_mean_personX(path_face_personX):
    features_list_personX = []
    photos_list = os.listdir(path_face_personX)
    if photos_list:
        for i in range(len(photos_list)):
            # 调用 return_128d_features() 得到 128D 特征 / Get 128D features for single image of personX
            logging.info("%-40s %-20s", "正在读的人脸图像 / Reading image:", path_face_personX + "/" + photos_list[i])
            features_128d = return_128d_features(path_face_personX + "/" + photos_list[i])
            # 遇到没有检测出人脸的图片跳过 / Jump if no face detected from image
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        logging.warning("文件夹内图像文件为空 / Warning: No images in%s/", path_face_personX)

    # 计算 128D 特征的均值 / Compute the mean
    # personX 的 N 张图像 x 128D -> 1 x 128D
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX, dtype=object).mean(axis=0)
    else:
        features_mean_personX = np.zeros(128, dtype=object, order='C')
    return features_mean_personX


def main():
    logging.basicConfig(level=logging.INFO)
    # 获取已录入的最后一个人脸序号 / Get the order of latest person
    person_list = os.listdir("faces_recognition/data/data_faces_from_camera/")
    person_list.sort()

    with open("faces_recognition/data/features_all.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for person in person_list:
            # Get the mean/average features of face/personX, it will be a list with a length of 128D
            logging.info("%sperson_%s", path_images_from_camera, person)
            features_mean_personX = return_features_mean_personX(path_images_from_camera + person)

            if len(person.split('_', 2)) == 2:
                # "person_x"
                person_name = person
            else:
                # "person_x_tom"
                person_name = person.split('_', 2)[-1]
            features_mean_personX = np.insert(features_mean_personX, 0, person_name, axis=0)
            # features_mean_personX will be 129D, person name + 128 features
            writer.writerow(features_mean_personX)
            logging.info('\n')
        logging.info("所有录入人脸数据存入 / Save all the features of faces registered into: data/features_all.csv")


if __name__ == '__main__':
    main()

    