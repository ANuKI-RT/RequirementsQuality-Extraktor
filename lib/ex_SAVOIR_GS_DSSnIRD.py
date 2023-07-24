"""
    Extract requirements statements from the SAVOIR-GS-DSSnIRD-006 and resolve acronyms.

    The requirements statements in the document are mostly precise. 
        - For requirements structure, see chapter 3.3

    OUTPUT FORMAT:
    ReqStatement[SEP]Remark[END]

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
        The function is optimized for the  SAVOIR-GS-DSSnIRD-006document.
    """

    final_req_list = []

    cleaned_text = re.sub("Page\s[0-9]+\/270", "", text)
    cleaned_text = re.sub("SAVOIR Data Storage Service and ", "", cleaned_text)
    cleaned_text = re.sub("Interface Requirement Document", "", cleaned_text)
    cleaned_text = re.sub("Date 20\/08\/2020", "", cleaned_text)
    cleaned_text = re.sub("Issue 1 Rev 0", "", cleaned_text)
    cleaned_text = re.sub("ESA UNCLASSIFIED – For Official Use", "", cleaned_text)
    
    toplevel_chapter_list = re.split("8\sDATA\sSTORAGE\sSERVICES", cleaned_text)
    reqs_chapter_list = re.split("7\.[0-9]+\s", toplevel_chapter_list[0])
    del reqs_chapter_list[:1]
    serv_chapter_list = re.split("8\.[0-9]+\.[0-9]+\s", toplevel_chapter_list[1])
    del serv_chapter_list[:1]

    for tlc in reqs_chapter_list:
        
        chapter_list = re.split("7\.[0-9]+\.[0-9]+\s", tlc)
        
        for c in chapter_list:

            reqs = re.split("SAVOIR\.MMS\.[A-Z]+\.[0-9]+\s", c)
            del reqs[:1]

            for r in reqs: 
                cleaned_req = re.split("Rationale\:\s", r)
                cleaned_req = re.split("Comment\:\s", cleaned_req[0])
                cleaned_req = re.split("Verification\sMethod\:\s", cleaned_req[0])
                cleaned_req = re.split("Parent\:\s", cleaned_req[0])

                if not cleaned_req[0].isspace():
                    final_req_list.append(cleaned_req[0] + "[END]")
    
    for tlc in serv_chapter_list:
        
        full_chapter_list = re.split("8\.[0-9]+\.[0-9]+\.[0-9]\s", tlc)
        
        for c in full_chapter_list:
            
            reqs = re.split("SAVOIR\.MMS\.[A-Z]+\.[0-9]+\s", c)
            del reqs[:1]

            for r in reqs: 
                cleaned_req = re.split("Rationale\:\s", r)
                cleaned_req = re.split("Comment\:\s", cleaned_req[0])
                cleaned_req = re.split("Verification\sMethod\:\s", cleaned_req[0])
                cleaned_req = re.split("Parent\:\s", cleaned_req[0])
                
                if not cleaned_req[0].isspace():
                    final_req_list.append(cleaned_req[0] + "[END]")
    
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
    del acronym_list[-1]


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
            
            cleaned_req = re.sub("\n","",r)
            try:
                f.write(cleaned_req[re.search("[a-z][A-Z]", cleaned_req).end() - 1:])
            except:
                f.write(cleaned_req)
            f.write("\n")

        f.close()

#___________________________________________________________________________________________________
def extract(path_to_doc, path_to_acronyms=""):

    text = getTextFromPDF(path_to_doc)
    reqs = getReqsFromText(text)
    full_reqs = resolveAcronyms(reqs, path_to_acronyms)
    saveRequirements(full_reqs, path_to_doc)
    print("Success")
