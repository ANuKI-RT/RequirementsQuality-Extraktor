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

        Text characteristics:
            - First string on each page: "MPY-VM SRS $pageNumber MPY-SPB-SRS- 001 $version $date
            - Req ID syntax = $subsystemID $reqCategoryID $sequentialNumber
            - A req is indicated with the ID, somethimes with OBCP codes, than verification char
            - After that two or three data points, the requirements text is following.
            - The req statement is one sentence, often ending with an enumeration.
            - Sometimes, a comment is following. Often starting with "Note", but not each time.
            - Empty chapters have only NA as content.
    """

    print(text)


#___________________________________________________________________________________________________
def extract(path_to_doc):

    text = getTextFromPDF(path_to_doc)
    reqs = getReqsFromText(text)

    print("Success")
