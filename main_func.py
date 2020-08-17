import pdf_split2img 
import text2csv as tc
from pdf2image import convert_from_path
import os
import pandas as pd

pdf_file = 'D:\Tsarfaty_Lab\sheshet\Aure_Recanati_Book1.pdf'
path,bookname = os.path.split(pdf_file)
dpi = 100  # quality
first_page = 8 # this book starts at page 8 (before there are list of possible names)
batch_size = 10
grayscale = True
fmt = 'jpeg'

# creating table with columns from a csv file (need to create one per book)
column_file = 'columns_book.csv'
table_csv = pd.read_csv(column_file)
table_csv.dropna(axis=0,how='all',inplace=True)
table_csv.to_csv(bookname.split('.')[0]+'.csv')


# pages = convert_from_path(pdf_path=os.path.join(path,bookname),
#                         dpi=dpi, first_page=first_page,
#                         last_page=batch_size+first_page-1, grayscale=grayscale,
#                         fmt=fmt)

pages = convert_from_path(pdf_path=os.path.join(path,bookname),
                        dpi=dpi, first_page=first_page,
                        grayscale=grayscale,
                        fmt=fmt)

original_first_page = 31


# page_file_name_left = r'./book_pages/'+bookname+'_'+str(page_n+start_page)+'_left.jpg'
# page_file_name_right = r'./book_pages/'+bookname+'_'+str(page_n+start_page)+'_right.jpg'


for n_page, page in enumerate(pages):
    table2db = pd.DataFrame(columns = table_csv.columns)
    text_left, text_right = pdf_split2img.jpg2img(page,
     bookname = bookname.split('.')[0], page_n=n_page, start_page=first_page)
    dict2df = tc.txt2csv(text_left,bookname,n_page+first_page+original_first_page-1,table2db.columns)
    table2db = pd.DataFrame.from_dict(dict2df)
    table2db.to_csv(bookname.split('.')[0]+'.csv', mode='a', header=False)
    dict2df = tc.txt2csv(text_right,bookname,n_page+first_page+original_first_page-1,table2db.columns)
    table2db = pd.DataFrame.from_dict(dict2df)
    table2db.to_csv(bookname.split('.')[0]+'.csv', mode='a', header=False)

