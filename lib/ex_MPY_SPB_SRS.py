"""
    Extract requirements statements from the MPY-SPB-SRS-001 and resolve acronyms.

    The requirements statements in the document are not precise. 
        - In tabular representation
        - With many enumerations
        - With comments in iraltic
        - With unique identifiers
        - With source code snipets

    There are empty categories with no requirements (i.e. chapters with no information).

    OUTPUT FORMAT:
    ReqStatement[SEP]Comment[END]

"""

from PyPDF2 import PdfReader
import re

#___________________________________________________________________________________________________
def getTextFromPDF(path_to_doc):
    """ 
        Extracts the text from a PDF and converts it in string representation.
    """

    reader = PdfReader(path_to_doc)
    output = ""
    
    for i in range(0,len(reader.pages)):
        page = reader.pages[i]
        output += page.extract_text()

    return output


#___________________________________________________________________________________________________
def getReqsFromText(text):
    """
        Splits a given text in single requirements statements.
        The function is optimized for the MPY-SPB-SRS-0001 document.

        Text characteristics:
            - First string on each page: "MPY-VM SRS $pageNumber MPY-SPB-SRS- 001 $version $date
            - Req ID syntax = $subsystemID $reqCategoryID $sequentialNumber
            - A req is indicated with the ID, sometimes with OBCP codes, than verification char
            - After that two or three data points, the requirements text is following.
            - The req statement is one sentence, often ending with an enumeration.
            - Sometimes, a comment is following. Often starting with "Note", but not each time.
            - Empty chapters have only NA as content.
    """
    
    cleaned_text = text.replace("Python 3.4.", "Python 3.4")
    cleaned_text = cleaned_text.replace("MPY-SPB-SRS- 001", "")
    cleaned_text = cleaned_text.replace("1.1 - 30/11/2017", "")
    chapter_list = re.split("(3[.][0-9]+[.])", cleaned_text)
    del chapter_list[:3] #remove general information in chapter 3.1   
    del chapter_list[::2] #remove every chapter number in the list

    for c in chapter_list:
        req_list = re.split("MPVM\s-[A-Z]+-[0-9]+", c)
        del req_list[:1] #remove chapter header   
        
        for req in req_list:
            cleaned_req = re.sub("OBCP-[0-9a-z]+,", "", req)
            cleaned_req = re.sub("REQ-VM-[0-9a-z]+,", "", cleaned_req)
            cleaned_req = re.sub("REQ-VM[0-9a-z]+,", "", cleaned_req)
            cleaned_req = re.sub("REQ-VM[0-9]+", "", cleaned_req)
            cleaned_req = re.sub("REQ-OBCPE-[0-9a-z]+,", "", cleaned_req)
            cleaned_req = re.sub("OBCP-", "", cleaned_req)
            cleaned_req = re.sub("OBCP", "", cleaned_req)
            cleaned_req = re.sub("[0-9][0-9][0-9][a-z],", "", cleaned_req)
            cleaned_req = re.sub("[0-9]+[a-z]", "", cleaned_req)
            cleaned_req = re.sub("\s[0-9]\s", "", cleaned_req)
            cleaned_req = re.sub("\s[TRAI]\s", "", cleaned_req)
            cleaned_req = re.sub("\s[-]\s", "", cleaned_req)
            cleaned_req = re.sub("\s[,]\s", "", cleaned_req)
            cleaned_req = re.sub("\s[0-9][0-9]\s", "", cleaned_req)
            cleaned_req = re.sub("MPY-VM\sSRS", "", cleaned_req)
            cleaned_req = re.sub("-[0-9]", "", cleaned_req)
            cleaned_req = re.sub("\s[0-9],", "", cleaned_req)
            cleaned_req = re.sub("MPY-VSR", "", cleaned_req)
            cleaned_req = re.sub("REQ-E00", "", cleaned_req)
            cleaned_req = re.sub("REQ-E-", "", cleaned_req)
            cleaned_req = re.sub("REQ-VM30", "", cleaned_req)
            print("***********************************************")
            print(cleaned_req)
            input()
        print(len(req_list))
        break
    
#___________________________________________________________________________________________________
def extract(path_to_doc):

    text = getTextFromPDF(path_to_doc)
    reqs = getReqsFromText(text)

    print("Success")
