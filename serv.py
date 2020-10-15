import socket
import socketserver
import datetime

def getPagePathFromGetReq(bruteGetReq):
    path = "/404"
    if(bruteGetReq.split(' ')[0]=="GET"):
        path = bruteGetReq.split(' ')[1]
    return path

def buildPage(path, content):
    pHeader = "HTTP/1.1 404\r\n"
    pBody = "Not Found"
    if path=='' or path == "/404":
        return pHeader+pBody
    pHeader = "HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n"
    
    pBody = "<head><meta charset=\"utf-8\"/><title>Httpy - simple serv</title></head>"
    pBody += "<body>"
    pBody += "<!-- Last refresing time : "+datetime.datetime.now().strftime('%H:%M:%S')+"-->"
    pBody += content.replace("\n", "<br>")
    pBody += "</body>"
    return pHeader+pBody

# dans cette fonction on definit le contenu des pages
def webSiteMaker(pathOfPageToBuild):
    pageBuilded = ""
    if pathOfPageToBuild=="/":
        pageBuilded = buildPage(pathOfPageToBuild, "Welcome to index")
    elif pathOfPageToBuild=="/calc":
        content = "<form action=\"/result\" method=\"get\">Nombre 1: <input type=\"text\" name=\"n1\" /><br />Nombre 2: <input type=\"text\" name=\"n2\" /><br /><input type=\"submit\" value=\"Additioner!\" /></form>"
        pageBuilded = buildPage(pathOfPageToBuild, content)
    elif "/result" in pathOfPageToBuild and "?" in pathOfPageToBuild:
        content = ""
        params = pathOfPageToBuild[pathOfPageToBuild.index("?")+1:]
        tabParams = params.split('&')
        #dans le tab intParams on recupere tous les chiffres dont on veut avoir la somme
        intParams = [0]*len(tabParams)
        i = 0
        for i in range(len(tabParams)):
            intParams[i] = int(tabParams[i][tabParams[i].index("=")+1:])
        #on fais la somme du tableau
        somme = 0
        strNbSommes = ""
        j = 0
        for j in range(len(intParams)):
            strNbSommes += str(intParams[j])+" + "
            somme+=intParams[j]
        content += "Result : "+strNbSommes[:strNbSommes.rindex('+')]+" = "+str(somme)
        pageBuilded = buildPage(pathOfPageToBuild, content)
    else:
        pageBuilded = buildPage(pathOfPageToBuild, "<h3>Sorry something went wrong</h3>")
    return pageBuilded


class WebServer(socketserver.BaseRequestHandler):

    #first line of the request GET /page HTTP/1.1\n\r
    getReq = ""

    def handle(self):
        client = self.request
        io = client.makefile()

        # Receiving client commands line per line
        print('> Request: ')
        receivingHeaders = True
        while receivingHeaders:
            line = io.readline().strip()
            print(line)
            if line == '':
                receivingHeaders = False
            elif line.split(' ')[0]=="GET":
                getReq = line


        # Creating a response for the client
        print('> Response: ')
        pagePath = getPagePathFromGetReq(getReq)
        response = webSiteMaker(pagePath)

        print(response)
        client.sendall(response.encode('utf-8'))


HOST, PORT = "127.0.0.1", 8080
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer((HOST, PORT), WebServer) as server:
    server.serve_forever()
