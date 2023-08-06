This is a convertor that takes normal mathematical text expressions as String inputs (eg. "2+ln2√π) and return the expression as it would be written in python (2+(math.log(2))*(math.sqrt(math.pi))

                            To do so


pip install utnamtte



-----------------------#Method 1---------------------------------

import utnamtte
print(utnamtte.tte("2+ln2"))



------------------------#Method 2----------------------------------

from utnamtte import tte
print(tte("2+ln2"))



------------------------#Method 3---------------------------------

from utnamtte import tte as xy
print(xy("2+ln2"))


watch tutorial on youtube https://bit.ly/ytutnamtte