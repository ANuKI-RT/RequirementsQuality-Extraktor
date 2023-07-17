"""
    Extract requirements statements from the E1356-GTD-SRS-01-I1-R4 and resolve acronyms.

    The requirements statements in the document are mostly precise. 
        - With two unique identifiers
        - With end character []
        - Remarks are everytime indicated via "Remark:" 
        - Many math symbolds
        - Some requirements contain tables and images (will be not in the output file)

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
        The function is optimized for the E1356-GTD-SRS-01_I1_R4 document.

        Text characteristics:
            - Delimiter between requirements is /square 
    """

    cleaned_text = re.sub("E1356-GTD-SRS-01", "", text)
    cleaned_text = re.sub("Copyright European Space Agency,", "", cleaned_text)
    cleaned_text = re.sub("SoftwareRequirementsSpecification", "", cleaned_text)
    cleaned_text = re.sub("2017-2018", "", cleaned_text)
    cleaned_text = re.sub("E1356-MLFS", "", cleaned_text)
    cleaned_text = re.sub("Identifier", "", cleaned_text)
    cleaned_text = re.sub("Issue 1.4 Date 2018-04-30", "", cleaned_text)
    cleaned_text = re.sub("Page[0-9]+of[0-9]+", "", cleaned_text)
    chapter_list = re.split("5\.[0-9]+\.?[0-9]+?", cleaned_text)
    
    final_req_list = []

    for c in chapter_list:
        req_list = re.split("/square", c)

        for req in req_list:            
            cleaned_req = re.sub("REQ-BL-[0-9]{4}", "", req)
            cleaned_req = re.sub("//GTD-TR-01-BL-[0-9]{4}", "", cleaned_req)
            cleaned_req = re.sub(",GTD-TR-01-BL-[0-9]{4}", "", cleaned_req)
            cleaned_req = re.sub("/T", "", cleaned_req)
            cleaned_req = re.sub("/A", "", cleaned_req)
            cleaned_req = re.sub("/I", "", cleaned_req)
            cleaned_req = re.sub("/D", "", cleaned_req)
            cleaned_req = re.sub("/R", "", cleaned_req)
            cleaned_req = re.sub("Table", "", cleaned_req)
            cleaned_req = re.sub("Figure", "", cleaned_req)
            cleaned_req = re.sub("function description", "", cleaned_req)
            cleaned_req = re.sub("Name description", "", cleaned_req)
            cleaned_req = re.sub("X Result Requirement", "", cleaned_req)
            cleaned_req = re.sub("X Y Result Requirement", "", cleaned_req)
            cleaned_req = re.sub("X∗iptrResult Requirement", "", cleaned_req)
            cleaned_req = re.sub("Metric name Target", "", cleaned_req)

            cleaned_req = re.sub("Remark:", "[SEP]", cleaned_req)
            
            if not cleaned_req.isspace():
                final_req_list.append(cleaned_req + "[END]")

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

