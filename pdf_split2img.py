import numpy as np
import ocr2txt as ot
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

def jpg2img(page, bookname = 'Aure_Recanati_Book1', page_n=0, start_page=0):
    '''
    jpg2text: function that takes jpg and return two string 
    with the path to the text files in both left and right side of the page
    Input: page (PIL Image) - specific page from a pdf file as gray-scale image
           bookname (str) - the name of the book this page was extracted from
           page_n (int) - the number of the page, to track the pages in order to correct false ocr reading
           start_page (int) - the page where the content begins to be relevant 
                        (for example: if we want to skip the table of content and the text starts on page 8, so 'start_page=8')
    Output: text_left (str), text_right (str) - both are path to each side of the page .txt file 
    '''
    gray = np.asarray(page)
    
    idx_middle = []
    for slice_ in range(4): 
        sum_lines = gray[int(np.round(gray.shape[0]/4))*slice_:int(np.round(gray.shape[0]/4))*(slice_+1),:].sum(axis=0)/255
        # print(sum_lines.max(), sum_lines>sum_lines.max()-10)
        idx_middle.append(gaussian_filter(sum_lines[100:-200],sigma=3).argmin(axis=0)[0]+90)

    # There is a 15 pixels offset
    text_left = ot.ocr2txt(image=gray[:,:idx_middle[0]-15],file_ext = '_'+str(page_n+start_page)+'_left')
    text_right = ot.ocr2txt(image=gray[:,idx_middle[2]-15:],file_ext = '_'+str(page_n+start_page)+'_right')
    return text_left, text_right

