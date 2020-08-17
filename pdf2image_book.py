from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image

# filename = 'page2'
# img = cv2.imread(filename+'.png')
# gray = cv2.cvtColor(img[40:-40,:],cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray,0,150,apertureSize = 3)
# minLineLength = 200
# maxLineGap = 30
# lines = cv2.HoughLinesP(edges,1,np.pi/180,200,minLineLength,maxLineGap)


pages = convert_from_path('D:\Tsarfaty_Lab\sheshet\Aure_Recanati_Book1.pdf', 200,first_page=8,last_page=20,grayscale=True,fmt='jpeg')
# for page,i in enumarate(pages):
#    filename = 'page'+str(i)

page1 = pages[0]        ## specific page 
gray = np.asarray(page1)
edges = cv2.Canny(gray,0,150,apertureSize = 3)

minLineLength = 200
maxLineGap = 30
lines = cv2.HoughLinesP(edges,1,np.pi/180,200,minLineLength,maxLineGap)

idx_middle = []
idy_middle = []
for slice_ in range(4): 
    sum_lines = gray[int(np.round(gray.shape[0]/4))*slice_:int(np.round(gray.shape[0]/4))*(slice_+1),:].sum(axis=0)/255
    print(sum_lines.max(), sum_lines>sum_lines.max()-10)
    # plt.plot(gaussian_filter(sum_lines>sum_lines.max()-2,sigma=1))
    # plt.show()
    idx_max = [float(i) for i,x in enumerate(gaussian_filter(sum_lines>sum_lines.max()-2,sigma=1)) 
                                if (x and i>len(sum_lines)/4 and i<3*len(sum_lines)/4)]
    idx_middle = idx_middle + [int(idx_max[int(np.round(len(idx_max)/2)+1)])]
    idy_middle = idy_middle + [int(np.round(gray.shape[0]/4))*slice_]
print(idx_middle, idy_middle)
print(lines)

cv2.imwrite(filename+'houghlines3.jpg',gray)
crop_img = gray[:,:idx_middle[0]] # img[y:y+h, x:x+w]
# print(idy_middle[0])
cv2.imwrite(filename+'houghlines3_1_2.jpg',crop_img)
cv2.imwrite(filename+'houghlines3_2_2.jpg',gray[:,idx_middle[0]:])

