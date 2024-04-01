import sys

def flatter(lst):
    x = []
    for i in lst:
        abs_lst = [abs(j) for j in i]
        x.extend(abs_lst)
    
    return x

def Tseitin(dnf):
    maxi = max(flatter(dnf))
    next = maxi + 1

    ans=[]

    for i in dnf:
        ans.append([-1*i[j] for j in range(len(i))]+[next])
        for j in i:
            ans.append([j,-1*next])
        next += 1

    return ans



