import pandas as pd
import re

def combine_dict_values(dict1, dict2):
    combined = {**dict1,**dict2}
    for key,value in combined.items():
        if key in dict1 and key in dict2:
            try:
                combined[key] = dict1[key] + value
            except TypeError:
                combined[key] = dict1[key] + [value]
    return combined


def txt2csv(file_name_txt,bookname,page_n,columns):
    dict2df = dict.fromkeys(columns,[])
    one_block = []
    all_blocks = [] 
    
    with open('./bookpages/'+file_name_txt+'.txt') as f:
        for line in f:
            if 'Identity Numbers'.lower() in line.lower():
                one_block = []
                all_blocks.append(one_block)
            one_block.append(line)
    for one_block_ in all_blocks:
        error_idx = 1
        dict2dict = dict.fromkeys(columns,[None])
        idx_line = 0
        for line in one_block_:
            if line!='\n':
                for i,col in enumerate(columns):
                    if col.lower() in line.lower():
                        val = line.strip().replace(col,'').\
                                        replace(':','').\
                                        strip()
                        if 'Born'.lower() == col.lower():
                            find_str = re.search('(?<={}).*[0-9]'.format(col), line)
                            try:
                                dict2dict[col] = [find_str.group(0).replace(':','')]
                            except:
                                dict2dict['Error '+str(error_idx)] = 'Error '+col+' '+file_name_txt
                                error_idx += 1
                                # print('Error '+col+' '+file_name_txt)
                        elif 'Domiciled at'.lower() == col.lower():
                            if '?' in line:
                                find_str = re.search('\(.\)', line)
                                try:
                                    first = find_str.group(0).replace(':','')
                                    dict2dict[col] = ['?']
                                    dict2dict['Quarter'] = [re.search('(?<={}).*'.format('\)'),first).group(0).replace(':','').strip()]
                                except:
                                    dict2dict['Error '+str(error_idx)] = 'Error '+col+' '+file_name_txt
                                    error_idx += 1
                            else:
                                find_str = re.search('(?<={}).*'.format(col), line)
                                first = find_str.group(0).replace(':','')
                                try:
                                    dict2dict[col] = [re.search('(.*)\(',first).group(1).replace(':','').strip()]
                                    find_q = re.search('\((.*)\)',first)
                                except:
                                    dict2dict['Error '+str(error_idx)] = 'Error '+col+' '+file_name_txt
                                    error_idx += 1
                                try:
                                    dict2dict['Quarter'] = [find_q.group(0).replace(':','').strip()]
                                except:
                                    dict2dict['Error '+str(error_idx)] = 'Error '+col+' '+file_name_txt
                                    error_idx += 1
                        elif 'Page'.lower() == col.lower():
                            dict2dict[col] = page_n
                        else:
                            find_str = re.search('(?<={}).*'.format(col.lower()), line.lower())
                            dict2dict[col] = [find_str.group(0).replace(':','').title().strip()]
                            break
                    elif col.lower() == 'Serial Number'.lower() and idx_line==i:
                        val = line.strip().replace(col,'').\
                            replace('.','').\
                            strip()
                        dict2dict['Serial Number'] = [val.strip()]
                        break
                    elif col.lower() == 'Last Name'.lower() and idx_line==i:
                        val = line.strip().replace(col,'').\
                            replace('.','').\
                            strip()
                        try:
                            dict2dict['Last Name'] = [val.split(' ')[0].strip()]
                            dict2dict['Name'] = [val.split(' ')[1].strip()]
                            break
                        except:
                            dict2dict['Error '+str(error_idx)] = 'Error '+col+' '+file_name_txt
                            error_idx += 1                            
                    elif col.lower()=='Born'.lower() and ('Bom'.lower() in line.lower()):
                        val = line.strip().replace(col,'').\
                                            replace(':','').\
                                            strip()
                        find_str = re.search('(?<={}).*[0-9]'.format('Bom'), line)
                        try:
                            dict2dict[col] = [find_str.group(0).replace(':','').strip()] 
                        except :
                            dict2dict['Error '+str(error_idx)] = 'Error '+col+' '+file_name_txt
                            error_idx += 1
                    elif 'Page'.lower() == col.lower():
                        dict2dict[col] = page_n
                    
                idx_line += 1
        dict2df = combine_dict_values(dict2df, dict2dict)
    return dict2df

