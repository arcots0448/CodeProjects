def LocalAlignment():
    filename = input("Enter file name: ")
    inputfile = open(filename, "r")
    indel_penalty = 5
    s = inputfile.readline()[:-1]
    t = inputfile.readline()[:-1]
    inputfile.close()
    
    backtrack, paths = LCSBackTrack(s,t,indel_penalty)
    row = 0
    col = 0
    big = paths[row][col]
    for i in range(len(paths)):
        for j in range(len(paths[i])):
            if paths[i][j] > big:
                big = paths[i][j]
                row = i
                col = j
    out = OutputLCS(backtrack, s, t, row, col, row, col)    
    return (big,out[0],out[1])

def findScore(a,b):
    scoreMatrix = [[2 ,-2 ,0 ,0 ,-3 ,1 ,-1 ,-1 ,-1 ,-2 ,-1 ,0 ,1 ,0 ,-2 ,1 ,1 ,0 ,-6 ,-3],
            [-2 ,12 ,-5 ,-5 ,-4 ,-3 ,-3 ,-2 ,-5 ,-6 ,-5 ,-4 ,-3 ,-5 ,-4 ,0 ,-2 ,-2 ,-8 ,0],
            [0 ,-5 ,4 ,3 ,-6 ,1 ,1 ,-2 ,0 ,-4 ,-3 ,2 ,-1 ,2 ,-1 ,0 ,0 ,-2 ,-7 ,-4],
            [0 ,-5 ,3 ,4 ,-5 ,0 ,1 ,-2 ,0 ,-3 ,-2 ,1 ,-1 ,2 ,-1 ,0 ,0 ,-2 ,-7 ,-4],
            [-3 ,-4 ,-6 ,-5 ,9 ,-5 ,-2 ,1 ,-5 ,2 ,0 ,-3 ,-5 ,-5 ,-4 ,-3 ,-3 ,-1 ,0 ,7],
            [1 ,-3 ,1 ,0 ,-5 ,5 ,-2 ,-3 ,-2 ,-4 ,-3 ,0 ,0 ,-1 ,-3 ,1 ,0 ,-1 ,-7 ,-5],
            [-1 ,-3 ,1 ,1 ,-2 ,-2 ,6 ,-2 ,0 ,-2 ,-2 ,2 ,0 ,3 ,2 ,-1 ,-1 ,-2 ,-3 ,0],
            [-1 ,-2 ,-2 ,-2 ,1 ,-3 ,-2 ,5 ,-2 ,2 ,2 ,-2 ,-2 ,-2 ,-2 ,-1 ,0 ,4 ,-5 ,-1],
            [-1 ,-5 ,0 ,0 ,-5 ,-2 ,0 ,-2 ,5 ,-3 ,0 ,1 ,-1 ,1 ,3 ,0 ,0 ,-2 ,-3 ,-4],
            [-2 ,-6 ,-4 ,-3 ,2 ,-4 ,-2 ,2 ,-3 ,6 ,4 ,-3 ,-3 ,-2 ,-3 ,-3 ,-2 ,2 ,-2 ,-1],
            [-1 ,-5 ,-3 ,-2 ,0 ,-3 ,-2 ,2 ,0 ,4 ,6 ,-2 ,-2 ,-1 ,0 ,-2 ,-1 ,2 ,-4 ,-2],
            [0 ,-4 ,2 ,1 ,-3 ,0 ,2 ,-2 ,1 ,-3 ,-2 ,2 ,0 ,1 ,0 ,1 ,0 ,-2 ,-4 ,-2],
            [1 ,-3 ,-1 ,-1 ,-5 ,0 ,0 ,-2 ,-1 ,-3 ,-2 ,0 ,6 ,0 ,0 ,1 ,0 ,-1 ,-6 ,-5],
            [0 ,-5 ,2 ,2 ,-5 ,-1 ,3 ,-2 ,1 ,-2 ,-1 ,1 ,0 ,4 ,1 ,-1 ,-1 ,-2 ,-5 ,-4],
            [-2 ,-4 ,-1 ,-1 ,-4 ,-3 ,2 ,-2 ,3 ,-3 ,0 ,0 ,0 ,1 ,6 ,0 ,-1 ,-2 ,2 ,-4],
            [1 ,0 ,0 ,0 ,-3 ,1 ,-1 ,-1 ,0 ,-3 ,-2 ,1 ,1 ,-1 ,0 ,2 ,1 ,-1 ,-2 ,-3],
            [1 ,-2 ,0 ,0 ,-3 ,0 ,-1 ,0 ,0 ,-2 ,-1 ,0 ,0 ,-1 ,-1 ,1 ,3 ,0 ,-5 ,-3],
            [0 ,-2 ,-2 ,-2 ,-1 ,-1 ,-2 ,4 ,-2 ,2 ,2 ,-2 ,-1 ,-2 ,-2 ,-1 ,0 ,4 ,-6 ,-2],
            [-6 ,-8 ,-7 ,-7 ,0 ,-7 ,-3 ,-5 ,-3 ,-2 ,-4 ,-4 ,-6 ,-5 ,2 ,-2 ,-5 ,-6 ,17 ,0],
            [-3 ,0 ,-4 ,-4 ,7 ,-5 ,0 ,-1 ,-4 ,-1 ,-2 ,-2 ,-5 ,-4 ,-4 ,-3 ,-3 ,-2 ,0 ,10]]

    vals = {'A':0,'C':1,'D':2,'E':3,'F':4,'G':5,'H':6,'I':7,'K':8,'L':9,'M':10,'N':11,'P':12,'Q':13,'R':14,'S':15,'T':16,'V':17,'W':18,'Y':19}
    
    return scoreMatrix[vals[a]][vals[b]]

def LCSBackTrack(v,w, indelPen):
    rows = len(v)+1
    cols = len(w)+1
    paths = [[0 for c in range(cols)] for r in range(rows)] 
    backtrack = [["" for c in range(cols)] for r in range(rows)]
    for i in range(len(v)+1):
        paths[i][0] = max((-i*(indelPen)),0)
    for j in range(len(w)+1):
        paths[0][j] = max((-j*(indelPen)),0)
    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            match = findScore(v[i-1],w[j-1])
            paths[i][j] = max(paths[i-1][j]-indelPen, paths[i][j-1]-indelPen, paths[i-1][j-1]+match, 0)
            if paths[i][j] == paths[i-1][j]-indelPen:
                backtrack[i][j] = "↓"
            elif paths[i][j] == paths[i][j-1]-indelPen:
                backtrack[i][j] = "→"
            elif paths[i][j] == paths[i-1][j-1]+match:
                backtrack[i][j] = "↘"
    return backtrack, paths
    
def OutputLCS(backtrack, v, w, i, j, endR, endC):
    if backtrack[i][j] == "" and (i != endR and j != endC):
        return ["",""]
    if backtrack[i][j] == "↓":
        out = OutputLCS(backtrack, v, w, i-1, j, endR, endC)
        out[0] += v[i-1]
        out[1] += "-"
        return out
    elif backtrack[i][j] == "→":
        out = OutputLCS(backtrack, v, w, i, j-1, endR, endC)
        out[0] += "-"
        out[1] += w[j-1]
        return out
    else:
        out = OutputLCS(backtrack, v, w, i - 1, j - 1, endR, endC)
        out[0] += v[i-1]
        out[1] += w[j-1]
        return out
print(LocalAlignment())
