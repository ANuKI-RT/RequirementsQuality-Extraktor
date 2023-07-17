from lib import ex_MPY_SPB_SRS
from lib import ex_E_CS_SRS
from lib import ex_E_GTD_SRS

def main ():

    #ex_MPY_SPB_SRS.extract("input/MPY-SPB-SRS-001.pdf", "input/MPY-SPB-SRS-001 Acronyms.txt")
    #ex_E_CS_SRS.extract("input/E1356-CS-SRS-01_I1_R3.pdf", "input/E1356-CS-SRS-01_I1_R3 Acronyms.txt")
    ex_E_GTD_SRS.extract("input/E1356-GTD-SRS-01_I1_R4.pdf", "input/E1356-GTD-SRS-01_I1_R4 Acronyms.txt")

main()
