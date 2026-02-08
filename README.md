Python Version Python 3.7+

Files needed to run my code:

    - dfsb.py
    - minconflicts.py

For data confirmation, you can use the following folder/files to cross-check with my PDF report:

    - N20M100K4QuestionsAndOutput
        - The folder contains all 20 problem of N=20 M=100 K=4 and the output of DFS-B++ and MCLS-R
    - N50M625K4QuestionsAndOutput
        - The folder contains all 20 problem of N=50 M=625 K=4 and the output of DFS-B++ and MCLS-R
    - N100M2500K4QuestionsAndOutput
        - The folder contains all 20 problem of N=100 M=2500 K=4 and the output of DFS-B++ and MCLS-R
    - N200M10000K4QuestionsAndOutput
        - The folder contains all 20 problem of N=200 M=10000 K=4 and the output of DFS-B++ and MCLS-R
    - N400M40000K4QuestionsAndOutput
        - The folder contains all 20 problem of N=400 M=40000 K=4 and the output of DFS-B++ and MCLS-R

How to run my code:

    - python dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>
        - <INPUT FILE>: the input filename
        - <OUTPUT FILE>: the output filename
        - <MODE FLAG>: can be either 0 (plain DFS-B) or any other number (improved DFS-B++).
        - EX: python dfsb.py backtrack_easy solution.txt 0
    - python minconflicts.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>
        - <INPUT FILE>: the input filename
        - <OUTPUT FILE>: the output filename
        - <MODE FLAG>: can be either 0 (plain MCLS) or any other number (improved MCLS-R)
        - EX: python minconflicts.py minconflict_easy solution.txt 1

References:

    - https://en.wikipedia.org/wiki/Min-conflicts_algorithm from HW PDF
    - https://pages.cs.wisc.edu/~bgibson/cs540/handouts/csp.pdf from HW PDF
    - “constraint-satisfaction-part-I” Lecture Slides
    - “constraint-satisfaction-part-IIa-b” Lecture Slides
    - https://www.w3schools.com/python/ Python documentations
    
