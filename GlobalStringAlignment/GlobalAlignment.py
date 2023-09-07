import sys
sys.setrecursionlimit(10000000) 
def GlobalAlignment():
    filename = input("Enter file name: ")
    inputfile = open(filename, "r")
    nums = inputfile.readline()[:-1].split()
    match_reward = int(nums[0])
    mismatch_penalty = int(nums[1])
    indel_penalty = int(nums[2])
    s = inputfile.readline()[:-1]
    t = inputfile.readline()[:-1]
    inputfile.close()
    
    backtrack, score = LCSBackTrack(s,t,match_reward,mismatch_penalty,indel_penalty)
    out = OutputLCS(backtrack, s, t, len(s), len(t))
    
    return (score,out[0],out[1])

def LCSBackTrack(v,w, matchRew, matchPen, indelPen):
    rows = len(v)+1
    cols = len(w)+1
    paths = [[0 for c in range(cols)] for r in range(rows)] 
    backtrack = [["" for c in range(cols)] for r in range(rows)]
    for i in range(1,len(v)+1):
        paths[i][0] = (-i*(indelPen))
        backtrack[i][0] = "↓"
    for j in range(1,len(w)+1):
        paths[0][j] = (-j*(indelPen))
        backtrack[0][j] = "→"
    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            match = (-1 * matchPen)
            if v[i-1] == w[j-1]:
                match = matchRew
            paths[i][j] = max(paths[i-1][j]-indelPen, paths[i][j-1]-indelPen, paths[i-1][j-1]+match)
            if paths[i][j] == paths[i-1][j]-indelPen:
                backtrack[i][j] = "↓"
            elif paths[i][j] == paths[i][j-1]-indelPen:
                backtrack[i][j] = "→"
            elif paths[i][j] == paths[i-1][j-1]+match:
                backtrack[i][j] = "↘"
    return backtrack, paths[len(v)][len(w)]

def OutputLCS(backtrack, v, w, i, j):
    if i == 0 or j == 0:
        if i != 0:
            return[v[:i], (i)*"-"]
        if j != 0:
            return[(j)*"-",w[:j]]
        else:
            return ["",""]
    if backtrack[i][j] == "↓":
        out = OutputLCS(backtrack, v, w, i-1, j)
        out[0] += v[i-1]
        out[1] += "-"
        return out
    elif backtrack[i][j] == "→":
        out = OutputLCS(backtrack, v, w, i, j-1)
        out[0] += "-"
        out[1] += w[j-1]
        return out
    else:
        out = OutputLCS(backtrack, v, w, i - 1, j - 1)
        out[0] += v[i-1]
        out[1] += w[j-1]
        return out

print(GlobalAlignment())
