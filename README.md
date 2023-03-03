![Python version](https://img.shields.io/github/pipenv/locked/python-version/FischerFranz939/OSM_XML_RemoveElements)
![GitHub license](https://img.shields.io/github/license/FischerFranz939/OSM_XML_RemoveElements)
![CircleCI](https://img.shields.io/circleci/build/github/FischerFranz939/OSM_XML_RemoveElements/main)
[![Coverage Status][cov-img]][cov]

[cov-img]: https://codecov.io/github/FischerFranz939/OSM_XML_RemoveElements/branch/main/graph/badge.svg
[cov]: https://codecov.io/github/FischerFranz939/OSM_XML_RemoveElements


# OSM_XML_RemoveElements
Program to remove unwanted elements from XML. E.g. remove all "power towers", "timestamps"...

The challenge is to process files with several GB size. Reading in the file and 
preparing it for processing requires an extremely large amount of main memory 
(factor ~10) see script (1). Therefore one idea is to process the file in smaller chuncks 
see script (2) and script (3).

---

## Different approaches

1. All in one

    uses ElementTree

    processes the whole input XML-file

2. Line by line

    does not use a XML parser (like ElementTree)

    processes input XML-file in chunks

    only string operations are possible (no XML operations)


3. Element by element

    uses ElementTree

    processes element by element of the input XML-file

    currently: "only" count elements

    only operations per element are possible

4. Use database

    TODO

---

## Links
[markdown cheat-sheet](https://www.markdownguide.org/cheat-sheet/)

[shields](https://shields.io/category/build)

