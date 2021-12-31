# CKYParse
A simple implementation of the CKY algorithm in python. The result of the analysis is returned as a list of lxml.etree._Element. If there is more than one parsing pattern due to ambiguity in natural language, a list with all elements is returned.

## requrement
- python: 3.9.9
- lxml==4.7.1

## How to use
### grammer
Gives a line separated phrase structure grammar. These rules must be given in Chomsky normal form.
```python
grammer = """
S -> NP VP
NP -> DET N
NP -> NP PP
VP -> V NP
VP -> VP PP
PP -> PREP NP
N -> I|girl|telescope
NP -> I|girl|telescope
V -> saw
VP -> saw
DET -> a
PREP -> with
"""
```
