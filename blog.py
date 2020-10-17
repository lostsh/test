import os

def aTag(link, text):
    return "<a href="+link+">"+text+"</a>"
#def navTag()

def build(fName):
    indexTemplate = open(fName[:fName.index(".")]+"-template"+fName[fName.index("."):], "r")
    index = open(fName, "w")

    for l in indexTemplate.readlines():
        if "[TITLE]" in l:
            l = l.replace("[TITLE]", "This is the title of ths blog")
        elif "[PARAGRAPH]" in l:
            l = l.replace("[PARAGRAPH]", "Hello world I am lama !")
        elif "[NAV]" in l:
            strNav = ""
            for i in os.listdir("./"):
                if ".html" in i and not "-template" in i: strNav += aTag(i, i[:i.index(".")])
            l = l.replace("[NAV]", strNav)
        index.write(l)
    
    index.close()
    indexTemplate.close()


build("index.html")