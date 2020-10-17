def build(fName):
    indexTemplate = open(fName[:fName.index(".")]+"-template"+fName[fName.index("."):], "r")
    index = open(fName, "w")

    for l in indexTemplate.readlines():
        if "[TITLE]" in l:
            l = l.replace("[TITLE]", "This is the title of ths blog")
        elif "[PARAGRAPH]" in l:
            l = l.replace("[PARAGRAPH]", "Hello world I am lama !")
        index.write(l)
    
    index.close()
    indexTemplate.close()

build("index.html")