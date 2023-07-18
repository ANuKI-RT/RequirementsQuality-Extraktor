"""
    Extract requirements statements from the RTEMS_SRS and resolve acronyms.

    The requirements statements in the document are mostly precise. 
        - With one unique identifier as path
        - In tabular representation
        - Every requirement follows the same structure with the same meta data tags
        - Many source code symbols

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
        The function is optimized for the RTEMS_SRS document.

        Text characteristics:
            - Split by chapters
            - Split by "rational to devide statement from additional information
            - Remove 2x path ID
    """

    final_req_list = []

    cleaned_text = re.sub("[0-9]+CISTER", "", text)
    cleaned_text = re.sub("Research Centre inReal-Time & EmbeddedCom put i n", "", cleaned_text)
    cleaned_text = re.sub("g Systems", "", cleaned_text)
    cleaned_text = re.sub("RTEMSQualiﬁcationSoftwareRequirementSpeciﬁcation", "", cleaned_text)
    cleaned_text = re.sub("\[sparc/gr712rc/smp/4\]", "", cleaned_text)
    cleaned_text = re.sub("Release3 ESAContractNo. 4000125572/18/NL/GLC/as", "", cleaned_text)
    cleaned_text = re.sub("Release3", "", cleaned_text)
    cleaned_text = re.sub("ESAContractNo.", "", cleaned_text)
    cleaned_text = re.sub("4000125572/18/NL/GLC/as", "", cleaned_text)
    cleaned_text = re.sub("©2021embeddedbrainsGmbH", "", cleaned_text)
    cleaned_text = re.sub("see:", "", cleaned_text)

    toplevel_chapter_list = re.split("5\.[0-9]+\s", cleaned_text)
    del toplevel_chapter_list[:1]

    for tlc in toplevel_chapter_list:
        chapter_list = re.split("5\.[0-9]+\.[0-9]+\s", tlc)
        del chapter_list[:1]

        for c in chapter_list:
            req_body = re.split("5\.[0-9]+\.[0-9]+\.[0-9]",c)
            req = re.split("rationale:", req_body[0])
            cleaned_req = re.sub("spec:(\/[a-z\-0-9]+)+", "", req[0])
            
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

