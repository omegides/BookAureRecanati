from PIL import Image
import pytesseract
import cv2
import os

def ocr2txt(image,preprocess="thresh",path='.\\bookpages\\',file_ext='_left'):
    """
    ocr2txt function:
    Input: img (path (str)) - an image path to a .jpg/.png file to be interpert into a text file
           thresh (str) - whether to create a threshold image or not 
    Output: (str) a file name that hold the current text to be analyzed
    """
    ## path to the pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    if preprocess=='thresh':
        gray = cv2.threshold(gray,0,255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    ## write the grayscale image to disk as a temporary file so we can apply OCR on it
    filename = "{}".format(os.getpid()) + file_ext + '.png'
    cv2.imwrite(path+filename,gray)
    
    text = pytesseract.image_to_string(Image.open(path+filename))

    filename_txt = open('./bookpages/' + filename[:-4] +'.txt','w')
    filename_txt.write(text)
    filename_txt.close()
    ## load the image as a PIL/Pillow image, apply OCR, and the delete the temporary file
    
    os.remove(path+filename)
    return filename[:-4] 
