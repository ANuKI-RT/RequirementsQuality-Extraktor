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
    ReqStatement[SEP]ID[SEP]Comment[END]

"""

from PyPDF2 import PdfReader

#___________________________________________________________________________________________________
def getTextFromPDF(path_to_doc):
    """ 
        Extracts the text from a PDF and converts it in string representation.
    """

    reader = PdfReader(path_to_doc)
    output = ""
    
    for i in range(0,len(reader.pages) - 1):
        page = reader.pages[i]
        output += page.extract_text()

    return output


#___________________________________________________________________________________________________
def getReqsFromText(text):
    """
        Splits a given text in single requirements statements.
        The function is optimized for the MPY-SPB-SRS-0001 document.
    """

    print(text)


#___________________________________________________________________________________________________
def extract(path_to_doc):

    text = getTextFromPDF(path_to_doc)
    reqs = getReqsFromText(text)

    print("Success")
