
# เก็บข้อมูลOCR tha & Eng return string2
def OCR_filev3(entrypath,custom_config): 
    import pytesseract
    import cv2
    if entrypath=='' :return '',''

    img = cv2.imread(entrypath)
    mainthaocr=pytesseract.image_to_string(img, lang='tha', config=custom_config) # 
    mainengocr=pytesseract.image_to_string(img, lang='eng', config=custom_config) # 

    return mainthaocr ,mainengocr