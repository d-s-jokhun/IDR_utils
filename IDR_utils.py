#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# e.g. of url : url='http://ccdb-portal.crbs.ucsd.edu:8080/broad_data/plate_26794/26794-ERSyto.zip'

# for plate in 24277 24278 24279 24280 24293 24294 24295 24296 24297 24300 24301 24302 24303 24304 24305 24306 24307 24308 24309 24310 24311 24312 24313 24319 24320 24321 24352 24357 24507 24508 24509 24512 24514 24515 24516 24517 24518 24523 24525 24560 24562 24563 24564 24565 24566 24583 24584 24585 24586 24588 24590 24591 24592 24593 24594 24595 24596 24602 24604 24605 24609 24611 24617 24618 24619 24623 24624 24625 24631 24633 24634 24635 24636 24637 24638 24639 24640 24641 24642 24643 24644 24645 24646 24647 24648 24651 24652 24653 24654 24655 24656 24657 24661 24663 24664 24666 24667 24683 24684 24685 24687 24688 24726 24731 24732 24733 24734 24735 24736 24739 24740 24750 24751 24752 24753 24754 24755 24756 24758 24759 24772 24773 24774 24775 24783 24785 24789 24792 24793 24795 24796 24797 25372 25374 25376 25378 25380 25382 25387 25391 25392 25403 25406 25408 25410 25414 25416 25418 25420 25422 25424 25426 25428 25430 25432 25434 25435 25436 25438 25485 25488 25490 25492 25503 25553 25564 25565 25566 25567 25568 25569 25570 25571 25572 25573 25575 25576 25578 25579 25580 25581 25583 25584 25585 25587 25588 25590 25591 25592 25593 25594 25598 25599 25605 25638 25639 25641 25642 25643 25663 25664 25665 25667 25674 25675 25676 25677 25678 25679 25680 25681 25683 25686 25688 25689 25690 25692 25694 25695 25700 25704 25707 25708 25724 25725 25726 25732 25738 25739 25740 25741 25742 25847 25848 25849 25852 25853 25854 25855 25856 25857 25858 25859 25862 25885 25890 25891 25892 25903 25904 25908 25909 25911 25912 25913 25914 25915 25918 25923 25925 25929 25931 25935 25937 25938 25939 25943 25944 25945 25949 25955 25962 25965 25966 25967 25968 25983 25984 25985 25986 25987 25988 25989 25990 25991 25992 25993 25994 25997 26002 26006 26007 26008 26009 26058 26060 26061 26071 26081 26092 26107 26110 26115 26118 26124 26126 26128 26133 26135 26138 26140 26159 26166 26174 26181 26202 26203 26204 26205 26207 26216 26224 26232 26239 26247 26271 26521 26531 26542 26544 26545 26562 26563 26564 26569 26572 26574 26575 26576 26577 26578 26579 26580 26588 26592 26595 26596 26598 26600 26601 26607 26608 26611 26612 26622 26623 26625 26626 26640 26641 26642 26643 26644 26662 26663 26664 26666 26668 26669 26670 26671 26672 26673 26674 26675 26677 26678 26679 26680 26681 26682 26683 26684 26685 26688 26695 26702 26703 26705 26724 26730 26739 26744 26745 26748 26752 26753 26765 26767 26768 26771 26772 26785 26786 26794 26795;
# do
# 	for channel in Hoechst ERSyto ERSytoBleed Ph_golgi Mito;
# 	do
# 		URL_LIST="http://ccdb-portal.crbs.ucsd.edu:8080/broad_data/plate_${plate}/${plate}-${channel}.zip $URL_LIST"
# 	done
# done


# In[1]:


import csv
import os
import multiprocessing as mp
import time
import requests
import numpy as np
import wget


# In[2]:


def IDR_TargetGetter(CompoundsOfInterest, idx_file=None):
    
    if idx_file is None:
        url = 'https://raw.githubusercontent.com/d-s-jokhun/idr-metadata/master/idr0016-wawer-bioactivecompoundprofiling/screenA/idr0016-screenA-annotation.csv'
        idx_file = str(os.path.basename(url))
        r = requests.get(url)
        with open(idx_file, 'w') as idxfile:
            idxfile.write(r.text)
    
    Targets=[]
    with open(idx_file, newline='') as idxfile:
        idx_reader = csv.DictReader(idxfile,fieldnames=None, restkey=None, restval=None, dialect='excel')
        for row in idx_reader:
            if CompoundsOfInterest.count(row['Compound Name']) > 0 :
                Targets.append({'Plate':row['Plate'],
                               'Well':row['Well'],
                               'Compound Name':row['Compound Name']})
    print('No. of targets identified = ',len(Targets))
    
    return Targets
#  Targets = [{plate, Well, Compound}]


# In[3]:


def IDR_ImgAvailChk(CompoundsOfInterest, ChannelsOfInterest, Local_ImgPath, idx_file=None):

    Targets = IDR_TargetGetter(CompoundsOfInterest, idx_file)
    PlatesOfInterest=np.unique([Target['Plate'] for Target in Targets])

    Existing_Folders = [dI for dI in os.listdir(Local_ImgPath)]
    dwnld_args=[]
    for plate in PlatesOfInterest:
        for channel in ChannelsOfInterest:
            Prospective_FolderName = f"{plate}-{channel}"
            if (Prospective_FolderName not in Existing_Folders and str(Prospective_FolderName+'.zip') not in Existing_Folders):
                dwnld_args.append((f"https://cildata.crbs.ucsd.edu/broad_data/plate_{plate}/{plate}-{channel}.zip",Local_ImgPath))
    
    print('No. of files to be downloaded = ',len(dwnld_args))
    
    return Targets, dwnld_args


# In[4]:


# Downloading the images
def IDR_ImageFetcher (dwnld_args):
    
    start=time.perf_counter()
    with mp.Pool() as pool:
        pool.starmap(wget.download, dwnld_args)
    print('Time elapsed during import = '+ str(time.perf_counter() - start) + ' s')
    print('Download and unzip Complete!')
    


# In[10]:


Use_as_Downloader = False


# In[11]:


if Use_as_Downloader:
    # Provide the compound/s and channel/s of interest as lists
    CompoundsOfInterest=selected_classes+['Cdk2/5 inhibitor','mammea A/BA']#['chlorphenamine','paracetamol']
    ChannelsOfInterest=['ERSytoBleed', 'Ph_golgi'] 
    # ChannelsOfInterest=['Hoechst', 'ERSyto', 'ERSytoBleed', 'Ph_golgi', 'Mito'] 


# In[12]:


if Use_as_Downloader:
    # Provide the idx_file which maps CompoundsOfInterest to specific plates
    # Set idx_file to None in order to download idx_file from IDR's github
    idx_file = './idr0016-screenA-annotation.csv'
    # idx_file = None

    # Provide the location where the files are to be downloaded
    Local_ImgPath = os.path.abspath(r'/MBELab/jokhun/Pro 1/U2OS small mol screening/RawImages')


# In[13]:


if Use_as_Downloader:
    # Checking which all files have to be downloaded
    Targets, dwnld_args = IDR_ImgAvailChk(CompoundsOfInterest, ChannelsOfInterest, Local_ImgPath, idx_file)


# In[14]:


if Use_as_Downloader:
    # Downloading the files
    IDR_ImageFetcher (dwnld_args)


# In[ ]:




