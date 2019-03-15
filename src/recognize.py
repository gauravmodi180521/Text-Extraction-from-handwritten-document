#IMPORTS
import cv2
import numpy as np
#FILE IMPORTS
from cc_segmentation import get_connected_components
from lwc_segmentation import get_line, get_chars, get_outline
from label_image import predict

#CONVERTING IMAGE INTO GRAYSCALE IMAGE
def to_grayscale(original_image):
	img = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
	return img

#CONVERTING IMAGE TO BINARY IMAGE
def to_binary(grayscale_image):
	thresh, img = cv2.threshold(grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)
	return img

#DRIVER CODE
#=============================================================

#INITIALIZING VALUES:
threshold_value = 110
original_image = input("Enter file name: ")

#PREPROCESSING
grayscale_image = to_grayscale(original_image)#original to grayscale
binarized_image = to_binary(grayscale_image)#grayscale to binary
binarized_image_int16 = np.int16(binarized_image)#uint8 to int16

#SEGMENTING
#objects = get_connected_components(binarized_image_int16)

line_coordinates =  get_line(binarized_image)
character_coordinates = get_chars(binarized_image, line_coordinates)

"""
#making box on CC
i = 0
for obj in objects:
    cv2.rectangle(binarized_image, (obj[2],obj[0]), (obj[3],obj[1]), color=(0,255,0), thickness=2)
    #cv2.putText(img, pred_list[i], (obj[2]+5, obj[0]), 2, 0.7, (0, 0, 255))
    i+=1
"""

#segmenting words in the output
for coo in character_coordinates:
	min_outline, max_outline = get_outline(coo)
	char_seg_thresh = (max_outline+min_outline)/2
	co_end = coo[0][0]
	for co in coo:
		img = cv2.resize(binarized_image[co[3]:co[1], co[0]:co[2]], (60,60))
		cv2.imwrite("../intermediate_file/ch.png", img)
		predicted_char = chr(int(predict("../intermediate_file/ch.png")))
		if(co[0] - co_end > char_seg_thresh):
			print("", predicted_char, end="")
		else:
			print(predicted_char, end="")
		co_end = co[2]
	print("\n")

#making box on line and characters
for co in line_coordinates:
    cv2.rectangle(binarized_image, (co[0], co[1]), (co[2], co[3]), color=(0,255,0), thickness=1)
for coo in character_coordinates:
    for co in coo:
    	cv2.rectangle(binarized_image, (co[0], co[1]), (co[2], co[3]), color=(0,255,0), thickness=1)


# pred_list = []
# for obj in objects:
#     pred_list.append(predict_class(binarized_image[obj[0]:obj[1], obj[2]:obj[3]]))
# img = cv2.cvtColor(binarized_image, cv2.COLOR_GRAY2RGB)

# for x in pred_list:
# 	print(x, end="")

cv2.imshow("win", binarized_image)
cv2.waitKey()