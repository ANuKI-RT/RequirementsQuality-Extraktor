"""
    Extract requirements statements from the E1356-CS-SRS-01-I1-R3 and resolve acronyms.

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

    print(output)

    return output



#___________________________________________________________________________________________________
def extract(path_to_doc, path_to_acronyms=""):

    text = getTextFromPDF(path_to_doc)
    #reqs = getReqsFromText(text)
    #full_reqs = resolveAcronyms(reqs, path_to_acronyms)
    #saveRequirements(full_reqs, path_to_doc)

    print("Success")

