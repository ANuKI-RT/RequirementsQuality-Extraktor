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

    final_req_list = []

    for c in chapter_list:
        req_list = re.split("MPVM\s-[A-Z]+-[0-9]+", c)
        del req_list[:1] #remove chapter header   
        
        for req in req_list:
            cleaned_req = re.sub("OBCP-[0-9a-z]+,", "", req)
            cleaned_req = re.sub("MPVM-FC[0-9a-z]+,", "", req)
            cleaned_req = re.sub("MPVM-FC-", "", req)
            cleaned_req = re.sub("REQ-VM-[0-9a-z]+,", "", cleaned_req)
            cleaned_req = re.sub("REQ-VM[0-9a-z]+,", "", cleaned_req)
            cleaned_req = re.sub("REQ-VM[0-9]+", "", cleaned_req)
            cleaned_req = re.sub("REQ-OBCPE-[0-9a-z]+,", "", cleaned_req)
            cleaned_req = re.sub("OBCP-", "", cleaned_req)
            cleaned_req = re.sub("OBCP", "", cleaned_req)
            cleaned_req = re.sub("[0-9][0-9][0-9][a-z],", "", cleaned_req)
            cleaned_req = re.sub("[0-9][0-9][0-9],", "", cleaned_req)
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
            cleaned_req = re.sub("REQ-", "", cleaned_req)
            cleaned_req = re.sub("VM[0-9]+", "", cleaned_req)
            cleaned_req = re.sub("E[0-9]+", "", cleaned_req)

            final_req_list.append(cleaned_req)

    print(str(len(final_req_list)) + " requirements extracted.")

    return final_req_list
    
#___________________________________________________________________________________________________
def resolveAcronyms(req_list, path_to_acronyms):
    """
        Load acronyms for specific requirement document from given path.
        Replace every abbrevation with the full text in the requirements list.
    
        Note: if an acronym is not listed in the abbrevation list of the requirements document,
        than the acronym is not resolved (e.g. RAM).
    """

    if path_to_acronyms == "":
        return req_list

    acronyms = open(path_to_acronyms, "r").read()
    acronym_list = acronyms.split("\n")

    for a in acronym_list:
        a_list = a.split(",")

        for i, req in enumerate(req_list):
            if a_list[0] in req:
                req_list[i] = re.sub(a_list[0], a_list[1], req)

    return req_list

#___________________________________________________________________________________________________
def saveRequirements(req_list, path_to_doc):
    """
        Save the extracted and cleaned requirements in one text document.
        Therefore, the given path from the input folder is changed to the output folder.

        Note: because of complex formatting issues, requirement statement are not splitted
        from their comments. This needs to be done manually.
    """

    output_path = re.sub("input", "output", path_to_doc)
    output_path = re.sub("pdf", "txt", output_path)
    
    with open(output_path, "w") as f:
        for r in req_list:
            f.write(re.sub("\n","",r))
            f.write("\n")
    
        f.close()
    

#___________________________________________________________________________________________________
def extract(path_to_doc, path_to_acronyms=""):

    text = getTextFromPDF(path_to_doc)
    reqs = getReqsFromText(text)
    full_reqs = resolveAcronyms(reqs, path_to_acronyms)
    saveRequirements(full_reqs, path_to_doc)   

    print("Success")
