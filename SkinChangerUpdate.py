
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request as urllib2

import requests
import zipfile
import io

import os
import glob
import shutil


def getFileURL(web_url):
    """

    This function grab the tartget download file's url from the website(web_url)

    Args:
        web_url (String): website url 
    Returns:
        string: the file url (file_url)
    """

    http = httplib2.Http()
    content = str(http.request(web_url))

    file_url = ""
    try:
        for link in BeautifulSoup(content, features="html.parser").find_all('a', href=True):
            if "zip" in link["href"]:
                file_url = link["href"]
                print("File found!")
                LOLVersion = file_url.split("_")[1]
                LOLVersion = LOLVersion[:-4]
                return file_url, LOLVersion
    except:
        print("ZIP file not found!")

    return "fail"


def downloadAndExtract(file_url, dst_path):
    """
        load zip file from the file_url into the buffer and extract it into dst_path

    Args:
        file_url (String): the url of the zip file on the website
        dst_path (String): the destination of the zip file extracted 
    """

    # fail case if the zip file url not found return
    if file_url == "fail":
        return

    # empty the folder for further update
    listOfFileName = os.listdir(dst_path)
    for file in listOfFileName:
        os.remove(os.path.join(dst_path, file))

    print("Successfully empty the folder!")

    # attempt to get the file using file_url
    try:
        file = requests.get(file_url)

    except:
        print("Unable to download")
        return

    # attempt to extract the zip file using the gotten file
    try:
        zipFile = zipfile.ZipFile(io.BytesIO(file.content))
        zipFile.extractall(dst_path)
    except:
        print("Unable to extract")
        return

    print("Successfully have the extracted files!")


def updataSkinChanger(dst_path, LOLVersion):

    # assemble the file path for the exe file (skinchanger file_uunextracted)
    exeFileName = "LOLPRO " + LOLVersion + ".exe"
    filePath = os.path.join(dst_path, exeFileName)
    print(filePath)

    # excute the file at filePath
    os.startfile(filePath)
    print("Successfully opened!")

    # wait until the file is closed -- press enter to continue
    input("Enter enter to continue.")

    fileList = os.listdir(dst_path)  # get all the file name in the folder

    findFlag = -1
    fileName = ""

    # find the new file (the actual skin changer)
    for file in fileList:
        if file != "data.lol" and file != "README.txt" and file != exeFileName:
            findFlag = 1
            fileName = file

    # check if find the skin changer
    if findFlag == -1:
        print("file not found")
        return
    

    fileName = os.path.join(dst_path, fileName) 
    
    # new file name
    newFileName = "skin.exe"
    newFileName = os.path.join(dst_path, newFileName)

    os.rename(fileName, newFileName) # rename the file
    
        # excute the file at filePath
    os.startfile(newFileName)
    print("Successfully replaced and opened!")
    
    
# def


def main():

    # define paths
    web_url = "https://lolskin.pro/"
    dst_path = "D:\Desktop\SkinChanger"

    # run function
    file_url = getFileURL(web_url)

    downloadAndExtract(file_url[0], dst_path)  # file_uel[0] is the file url
    # file_url[1] is the current LOL version
    updataSkinChanger(dst_path, file_url[1])


if __name__ == "__main__":
    main()
