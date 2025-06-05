# SpaceReqEx - Space Requirements Extraction
This project provides [functionality](lib) to extract [requirements statements](output) from [requirements documents](input) of European space projects. 

## Installation
Clone this repository on your machine:

```cmd
git clone https://gitlab.reutlingen-university.de/anuki/spacereqex.git
```

Create a virtual Python environment for this project, e.g.

```cmd
python3 -m venv env
```

Activate the create environment, e.g. (linux command)
```cmd
source env/bin/activate
```

Install the needed libaries using pip, e.g.
```cmd
pip install -r requirements.txt
```

## Run the application
Configure the function calls, select the input and run
```cmd
python3 main.py
```

## Important notes
Select a function of the lib for a respective requirement document in the main.py program for executing the extraction. Due to overlaps between requirements statements and comments or complex formatting, manual cleaning of the resulting data file in the output folder could be necessary.

### References
The code of this repository as well as the extracted data served as an input in the following two papers:

Korfmann, R., Beyersdorffer, P., Gerlich, R., Münch, J., & Kuhrmann, M. (2025). Overcoming Data Shortage in Critical Domains With Data Augmentation for Natural Language Software Requirements. Journal of Software: Evolution and Process, 37(5), e70027.![10.1002/smr.70027](https://onlinelibrary.wiley.com/doi/10.1002/smr.70027)

Korfmann, R., Beyersdorffer, P., Münch, J., & Kuhrmann, M. (2024, September). Using data augmentation to support AI-based requirements evaluation in large-scale projects. In European Conference on Software Process Improvement (pp. 97-111). Cham: Springer Nature Switzerland. ![10.1007/978-3-031-71139-8_7](https://link.springer.com/chapter/10.1007/978-3-031-71139-8_7)


