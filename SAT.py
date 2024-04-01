#!/usr/bin/env python

import sys
import copy
import networkx as nx

def flatter(lst): #二重リストをフラットする
# {{{
    x = []
    for i in lst:
        abs_lst = [abs(j) for j in i]
        x.extend(abs_lst)
    
    return x
# }}}

def merge(ft):
# {{{
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
                    p_num = len(list(filter(lambda x: x > 0, tmp)))
                    if(ft_[p_num].count(tmp)==0):
                        ft_[p_num].append(tmp)

                    flag[i][j]=0
                    flag[i+1][k]=0

    for i in range(len(ft)):
        for j in range(len(ft[i])):
            if(flag[i][j]==1):
                remains.append(ft[i][j])

    return [ft_, remains]
# }}}

def get_prime(tt):
# {{{
    ft = [[] for i in range(len(tt[0])+1)]

    for i in range(len(tt)): #各ファクターについて正のリテラル数をカウント
        p_num = len(list(filter(lambda x: x > 0, tt[i])))
        ft[p_num].append(tt[i])

    remains = []

    while True:
       [ft_, r] = merge(ft) 
       remains += r
       if (len(ft_)==0):
           break

       ft = ft_
    
    return remains
# }}}

def subset_problem(table):
# {{{    
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
# }}}

def mcp(tt,cand): # simplest DNF generation
# {{{
    table = [[0 for i in range(len(tt))] for j in range(len(cand))]
    
    for i in range(len(cand)):
        for j in range(len(tt)):
            if(set(cand[i]) <= set(tt[j])):
                table[i][j] = 1
    winner = subset_problem(table)

    ans = [cand[i] for i in winner]
    return ans
# }}}

def qm(fnc):
# {{{
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
                    lst.append(sorted(i+[j], key=abs))
                    lst.append(sorted(i+[-1*j], key=abs))
                else:
                    tmp_lst = copy.deepcopy(lst)
                    for k in range(len(lst)):
                        lst[k].append(j)
                        lst[k] = sorted(lst[k], key=abs)
                        tmp_lst[k].append(-1*j)
                        tmp_lst[k] = sorted(tmp_lst[k], key=abs)

                    lst = lst + tmp_lst
        if(lst==[]):
            fnc_ = fnc_ + [i]
        else:
            fnc_ = fnc_ + lst

    prime = get_prime(fnc_) #主項のみを抽出
    return mcp(fnc_, prime) #元の論理関数に対する最小被覆問題を解き，必要な主項のみをさらに抽出
# }}}

def tseitin(dnf): # simplest DNF to CNV converstion
# {{{
    maxi = max(flatter(dnf))
    next = maxi + 1

    ans=[]

    for i in dnf:
        ans.append([-1*i[j] for j in range(len(i))]+[next])
        for j in i:
            ans.append([j,-1*next])
        next += 1

    return ans
# }}}

def find_node(G, attr, value): #G内のnodeのうちattr=valueのものをリストで抽出
# {{{

    result = []

    d = nx.get_node_attributes(G, attr)

    for key, v in d.items():
        if(v == value):
            result.append(key)

    return result
# }}}

def find_max(G, attr): #G内のnodeがもつattrのうち最大値を出力（Gが空グラフの場合は0）
# {{{
    maxi = -1

    d = nx.get_node_attributes(G, attr)
    
    v_list = [v for key, v in d.items()]

    if(v_list==[]):
        return 0
    else:
        return max(v_list)
# }}}

def bcp(cnf, G, dl):
# {{{
    fin = 0
    while fin==0: #追加すべきノードがなくなるまで繰り返す
        fin = 1
        G_old = nx.DiGraph(G) #グラフをコピー
        for i in range(len(cnf)):
            dec = 0 #すでに真偽が決定したファクターかどうか
            cnt = 0 #ファクター内の未割当のリテラル数

            for j in range(len(cnf[i])):
                if(cnf[i][j]<0): #負数の場合
                    cand = abs(cnf[i][j])
                    if(cand in list(G_old.node)): #リテラルがG_oldに含まれる→割当済み
                        if(G_old.node[cand]['value']==0): #そのリテラルが1→そのファクターが真で決定
                            dec=1
                            break
                    else: #リテラルがG_oldに含まれない→未割当
                        cnt += 1
                        fct = i
                        target = cnf[i][j]
                elif(cnf[i][j]>0): #正数の場合
                    cand = cnf[i][j]
                    if(cand in list(G_old.node)):
                        if(G_old.node[cand]['value']==1):
                            dec=1
                            break
                    else:
                        cnt += 1
                        fct = i
                        target = cnf[i][j]

            if(dec==0 and cnt==0): #ファクターが偽で決定
                return [G, True]
            
            if(dec==0 and cnt==1): #unit-clauseがあった場合
                fin = 0

                #追加するノードへの辺の始点になるノードを探索
                wl_max = 0
                for j in list(set(cnf[fct])-{target}):
                    tmp = G.node[abs(j)]['w_level']
                    if(tmp>wl_max):
                        wl_max = tmp

                p_list = []
                for j in list(set(cnf[fct])-{target}): #旧グラフでファクタ内最大のw_levelを持つリテラル→辺の始点
                    if(G.node[abs(j)]['w_level']==wl_max):
                        p_list.append(abs(j))

                wl = wl_max + 1

                if(target<0):
                    name = abs(target)
                    v = 0
                else:
                    name = target
                    v = 1

                if(not(name in list(G.node))): #そのリテラルがグラフになかった場合→追加可能
                    G.add_node(name, value = v, d_level = dl, w_level = wl) #ノードの追加
                    for k in p_list: #辺の追加
                            G.add_edge(k, name, factor=fct)
                else: #そのリテラルが既にグラフに追加されていた場合→値次第ではコンフリクト
                    if(G.node[name]['value']==v): #値が等しい→コンフリクト無→辺の追加のみ
                        for k in p_list: #辺の追加
                                G.add_edge(k, name, factor=fct)
                    else: #値が異なる→コンフリクト→（暫定）追加せずに返す
                        return [G, True]

    return [G, False]
# }}}

def decide(cnf, G, dl):
### {{{
    for i in range(len(cnf)):
        dec=0 #すでに真偽が決定したファクターかどうか
        for j in range(len(cnf[i])):
            if(cnf[i][j]<0): #負数の場合
                cand = abs(cnf[i][j])
                if(cand in list(G.node)):
                    if(G.node[cand]['value']==0):
                        dec=1
                        break
                else:
                    target = cnf[i][j]
            else: #整数の場合
                cand = cnf[i][j]
                if(cand in list(G.node)):
                    if(G.node[cand]['value']==1):
                        dec=1
                        break
                else:
                    target = cnf[i][j]
        if(dec==0): #真偽が決定していないファクター→targetが存在→割当
            break

    if(dec==1): #全てのファクターの真偽が決定している→充足→割当の必要無→return True
        return [G, True]
    else: #割当
        wl = find_max(G, 'w_level')
        if(wl==0):
            wl =1

        if(target<0):
            name = abs(target)
            v = 0
        else:
            name = target
            v = 1

        G.add_node(name, value = v, d_level = dl, w_level = wl) #ノードの追加
        return [G, False]
# }}}

def analyze_conflict(G):
# {{{
    maxi = find_max(G, 'd_level')
    return maxi
# }}}
    
def back_track(G, b_level, cnf):
# {{{
    dl_lst = find_node(G, 'd_level', b_level)
    
    min_wl = find_max(G, 'w_level')
    for i in dl_lst:#w_levelの最小値を探す
        tmp = G.node[i]['w_level']
        if(tmp<min_wl):
            min_wl = tmp
    
    wl_lst = find_node(G, 'w_level', min_wl) #指定されたd_levelを持つノードのうち，最小のw_levelを持つノードのリスト
    
    new_fct = [] #新しいファクターの作成
    for i in wl_lst:
        if(G.node[i]['value']==0):
            new_fct.append(i)
        if(G.node[i]['value']==1):
            new_fct.append(-1*i)

    new_fct = sorted(new_fct,key=abs)
    cnf.append(new_fact) #新しいファクターの追加

    #指定されたd_levelを持つノードの全削除
    G.remove_nodes_from(dl_list)

    return G
# }}}

def dpll(cnf): # SAT solver
# {{{
    d_level = 0
    G = nx.DiGraph()
    
    [G, conflict] = bcp(cnf, G, d_level)
    if(conflict):
        return [False]
    
    while True:
        d_level += 1
        [G, sat] = decide(cnf, G, d_level)
        if(sat): #充足可能
            node1 = find_node(G, 'value', 1) #1が割り当てられているリテラル
            node0 = find_node(G, 'value', 0) #0が割り当てられているリテラル
            node0 = [-1*i for i in node0]
            ans = sorted(node1+node0, key=abs) #結合して絶対値順でソート
            return ans
        else:
            while True:
                [G, conflict] = bcp(cnf, G, d_level)
                if(not conflict): #コンフリクトしていない→（現時点では）バックトラックの必要無→break
                    break

                b_level = analyze_conflict(G)
                if(b_level==0): #一度もdecideせずにconflictしているということは，充足不可能
                    return [False]
                else:
                    d_level = b_level-1
                    G = back_track(G, b_level, cnf)
# }}}

if __name__ == '__main__':
    fnc = [[-1, -3], [1, 2], [1, -2, -3]] # A'B'C' + BC'+ AB'
    print("Input DNF: ", end="")
    print(fnc)

    simplest_dnf = qm(fnc)
    print("Simplest DNF: ", end="")
    print(simplest_dnf)

    cnf = tseitin(simplest_dnf)
    print("CNF: ", end="")
    print(cnf)

    solver = dpll(cnf)
    print("Result: ", end="")
    if(solver == [False]):
        print("Unsatisfiable..")
    else:
        print("Satisfiable with ", end="")
        print(solver, end="")
        print(" etc.")

# vim: fdm=marker
