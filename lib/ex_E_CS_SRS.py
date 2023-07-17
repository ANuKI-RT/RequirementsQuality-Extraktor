"""
    Extract requirements statements from the E1356-CS-SRS-01-I1-R3 and resolve acronyms.

    The requirements statements in the document are mostly precise. 
        - In tabular representation
        - With unique identifiers
        - There are deleted requirements with ID but only "DELETED" text.

    Some sub chapters, containing requirements of a specific category, have introduction text.
    Some sub chapters are empty (i.e. "NA") or contain a reference to another chapter.

    OUTPUT FORMAT:
    ReqStatement[SEP]Remark or Justification[END]

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
        The function is optimized for the E1356-CS-SRS-01_I1_R3document.

        Text characteristics:
            - 
    """
    cleaned_text = text.replace("Copyright European Space Agency, 2017", "")
    cleaned_text = cleaned_text.replace("Test Suite for the Basic", "")
    cleaned_text = cleaned_text.replace("mathematical Library - Software", "")
    cleaned_text = cleaned_text.replace("Requirements Specification  date", "")
    cleaned_text = cleaned_text.replace("2018-08-18  ", "")
    cleaned_text = cleaned_text.replace("reference \nE1356-CS-SRS-01  version \n1.3 ", "")
    cleaned_text = cleaned_text.replace("page", "")
    cleaned_text = cleaned_text.replace("Identifier Description Verif.", "")
    cleaned_text = cleaned_text.replace("Method  Rationale", "")
    cleaned_text = cleaned_text.replace("Test run:", "")
    cleaned_text = cleaned_text.replace("Test types:", "")
    cleaned_text = cleaned_text.replace("derived", "")
    cleaned_text = re.sub("[0-9]+ \/ 28", "", cleaned_text)

    chapter_list = re.split("5\.[0-9]+\.?[0-9]?", cleaned_text)
    del chapter_list[:2] #remove general information and chapter 4.4
    
    final_req_list = []

    for c in chapter_list:
        req_list = re.split("REQ-BLTS-[0-9]{4}", c)
        del req_list[:1] #remove chapter header   

        for req in req_list:
            cleaned_req = re.sub("Deleted(\.)?", "", req)
            cleaned_req = re.sub("\s[AIRT]\s", "", cleaned_req)
            cleaned_req = re.sub("SOW", "", cleaned_req)
            cleaned_req = re.sub("[0-9]\.[0-9]\.[0-9]", "", cleaned_req)
            cleaned_req = re.sub("GTD-TR-", "", cleaned_req)
            cleaned_req = re.sub("[0-9]+-BLTS-", "", cleaned_req)
            cleaned_req = re.sub("[0-9]{4}", "", cleaned_req)
            cleaned_req = re.sub("GTD-TR-[0-9]+", "", cleaned_req)
            cleaned_req = re.sub("GTD -TR-[0-9]+", "", cleaned_req)
            cleaned_req = re.sub("GTD -TR-", "", cleaned_req)
            cleaned_req = re.sub("BLTS -", "", cleaned_req)
            cleaned_req = re.sub("BLTS-", "", cleaned_req)
            cleaned_req = re.sub("[0-9][0-9]-", "", cleaned_req)

            if not cleaned_req.isspace():
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

