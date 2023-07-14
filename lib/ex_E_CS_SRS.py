"""
    Extract requirements statements from the E1356-CS-SRS-01-I1-R3 and resolve acronyms.

    The requirements statements in the document are mostly precise. 
        - In tabular representation
        - With unique identifiers
        - There are deleted requirements with ID but only "DELETED" text.

    Some sub chapters, containing requirements of a specific category, have introduction text.
    Some sub chapters are empty (i.e. "NA") or contain a reference to another chapter.

    OUTPUT FORMAT:
    ReqStatement[END]

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

    print(output)

    return output



#___________________________________________________________________________________________________
def extract(path_to_doc, path_to_acronyms=""):

    text = getTextFromPDF(path_to_doc)
    #reqs = getReqsFromText(text)
    #full_reqs = resolveAcronyms(reqs, path_to_acronyms)
    #saveRequirements(full_reqs, path_to_doc)

    print("Success")

