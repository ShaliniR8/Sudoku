

def empty(b):
    for i in range(len(b)):
        for j in range(len(b)):
            if b[i][j]==0:
                return (i,j)
                
    return None

def valid (b,num,pos):
    #checking in a row
    for i in range(len(b)):
        if b[pos[0]][i]==num and i!=pos[1]:
            return False
    #checking in a col
    for i in range(len(b)):
        if b[i][pos[1]]==num and i!=pos[0]:
            return False
    #checking the big box
    x=pos[0]//3
    y=pos[1]//3
    
    for i in range(x*3,x*3+3):
        for j in range(y*3,y*3+3):
            if b[i][j]==num and pos!=(i,j):
                return False
    return True

def solve(b):
    find=empty(b)
    #if find not empty then we've reached the end 
    if not find:
        return True
    else:
        r,c=find
    for i in range(1,10):
        if valid(b,i,(r,c)):
            b[r][c]=i
            if solve(b):
                return True
            else:

                b[r][c]=0
    return False

print_board(board)
print(" ")
solve(board)
print_board(board)
