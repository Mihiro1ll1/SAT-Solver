import sys
import copy

def flatter(lst): #二重リストをフラットする
    x = []
    for i in lst:
        abs_lst = [abs(j) for j in i]
        x.extend(abs_lst)
    
    return x

def merge(ft):
    ft_ = [[] for i in range(len(ft)-1)]
    flag = [[1 for j in range(len(ft[i]))] for i in range(len(ft))]
    remains = []
    
    for i in range(len(ft)-1):
        for j in range(len(ft[i])):
            for k in range(len(ft[i+1])):

                subA = list(set(ft[i][j])-set(ft[i+1][k]))
                subB = list(set(ft[i+1][k])-set(ft[i][j]))

                if(len(subA)==1 & len(subB)==1):
                    sub = subA[0]+subB[0]
                else:
                    sub = 1
                
                if(sub == 0):
                    tmp = list(set(ft[i][j])-set(subA))
                    tmp = sorted(tmp, key=lambda x: abs(x))
                    p_num = len(list(filter(lambda x: x > 0,tmp)))
                    if(ft_[p_num].count(tmp)==0):
                        ft_[p_num].append(tmp)

                    flag[i][j]=0
                    flag[i+1][k]=0

    for i in range(len(ft)):
        for j in range(len(ft[i])):
            if(flag[i][j]==1):
                remains.append(ft[i][j])

    return [ft_,remains]

def get_prime(tt):
    ft = [[] for i in range(len(tt[0])+1)]

    for i in range(len(tt)): #各ファクターについて正のリテラル数をカウント
        p_num = len(list(filter(lambda x: x > 0,tt[i])))
        ft[p_num].append(tt[i])


    remains = []

    while True:
       #print(ft,remains)
       [ft_,r] = merge(ft) 
       remains += r
       #if (len(ft0)==len(r)):
       if (len(ft_)==0):
           break

       ft = ft_
    
    return remains

def subset_problem(table):
    
    #table内の全ての要素が2→完了，return
    fin_flag=1
    for i in table:
        for j in i:
            if(j!=2):
                fin_flag=0

    if(fin_flag):
        return []

    req_flag = 0
    for i in range(len(table[0])):
        req_num = 0

        for j in range(len(table)):
            if(table[j][i]==1):
                req_num += 1
                buf = j

        if(req_num==1):
            req_flag = 1
            break

    if(req_flag):
        tmp = table[buf]
        for j in range(len(tmp)):
            if(tmp[j]==1):
                for i in range(len(table)):
                    table[i][j] = 2

        table[buf] = [2 for i in range(len(tmp))]
        return [buf]+subset_problem(table)
    else:
        cand = -1
        for i in range(len(table)):
            for j in range(len(table[i])):
                if(table[i][j]==1):
                    cand = i
                    break
            if(cand!=-1):
                break

        tmp = table[cand]
        table[cand] = [2 for i in range(len(tmp))]

        M_m = subset_problem(table)
        
        for j in range(len(tmp)):
            if(tmp[j]==1):
                for i in range(len(table)):
                    table[i][j] = 2

        M_p = [cand]+subset_problem(table)

        if(len(M_m)<len(M_p)):
            return M_m
        else:
            return M_p

def MCP(tt,cand):
    table = [[0 for i in range(len(tt))] for j in range(len(cand))]
    
    for i in range(len(cand)):
        for j in range(len(tt)):
            if(set(cand[i]) <= set(tt[j])):
                table[i][j] = 1
    #print(table)
    winner = subset_problem(table)

    ans = [cand[i] for i in winner]

    return ans

def QM(fnc):
    
    # fncの各ファクターに全てのリテラルが含まれるように修正
    # ex) リテラル数3の場合　[1,-2] -> [1,-2,3],[1,-2,-3]
    flat = flatter(fnc)
    maxi = max(flat)
    fnc_ = []
    for i in fnc:
        lst = []
        for j in range(1,maxi+1):
            if(not(j in i) and not(-1*j in i)):
                if(lst==[]):
                    lst.append(sorted(i+[j],key=abs))
                    lst.append(sorted(i+[-1*j],key=abs))
                else:
                    tmp_lst = copy.deepcopy(lst)
                    for k in range(len(lst)):
                        lst[k].append(j)
                        lst[k] = sorted(lst[k],key=abs)
                        tmp_lst[k].append(-1*j)
                        tmp_lst[k] = sorted(tmp_lst[k],key=abs)

                    lst = lst + tmp_lst
        if(lst==[]):
            fnc_ = fnc_ + [i]
        else:
            fnc_ = fnc_ + lst
    #print(fnc_)


    prime = get_prime(fnc_) #主項のみを抽出
    return MCP(fnc_,prime) #元の論理関数に対する最小被覆問題を解き，必要な主項のみをさらに抽出
    
if __name__ == '__main__':
    fnc = [[1],[-1,-2,3],[-1,3]]
    print(QM(fnc))
