# OSM_XML_RemoveElements
Program to remove unwanted elements from XML. E.g. remove all "power towers", "timestamps"...

---
**>>>>>> WORK IN PROGRESS <<<<<<**

---

The challenge is to process files with several GB size. Reading in the file and 
preparing it for processing requires an extremely large amount of main memory 
(factor ~10) see script (1). Therefore one idea is to process the file in smaller chuncks 
see script (2) and script (3).

---

## Different approaches

1. Script 1

    uses ElementTree

    processes the whole input XML-file

2. Script 2

    does not use a XML parser (like ElementTree)

    processes input XML-file in chunks

    only string operations are possible (no XML operations)


3. Script 3

    uses ElementTree

    processes element by element of the input XML-file

    currently: "only" count elements

    only operations per element are possible

---

## Links
[markdown cheat-sheet](https://www.markdownguide.org/cheat-sheet/)

