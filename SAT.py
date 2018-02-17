import sys
import networkx as nx
import matplotlib.pyplot as plt

def find_node(G, attr, value): #G内のnodeのうちattr=valueのものをリストで抽出

    result = []

    d = nx.get_node_attributes(G, attr)

    for key, v in d.items():
        if(v == value):
            result.append(key)

    return result

def find_max(G, attr): #G内のnodeがもつattrのうち最大値を出力．Gが空グラフの場合は0．
    maxi = -1

    d = nx.get_node_attributes(G, attr)
    
    v_list = [v for key,v in d.items()]

    if(v_list==[]):
        return 0
    else:
        return max(v_list)

def flatter(lst): #二重リストをフラットする
    x = []
    for i in lst:
        abs_lst = [abs(j) for j in i]
        x.extend(abs_lst)
    
    return x

def BCP(cnf,G,dl):
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
                return [G,True]
            
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
                            G.add_edge(k,name,factor=fct)
                else: #そのリテラルが既にグラフに追加されていた場合→値次第ではコンフリクト
                    if(G.node[name]['value']==v): #値が等しい→コンフリクト無→辺の追加のみ
                        for k in p_list: #辺の追加
                                G.add_edge(k,name,factor=fct)
                    else: #値が異なる→コンフリクト→（暫定）追加せずに返す
                        return [G,True]

    return [G,False]


def DECIDE(cnf,G,dl):
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
        return [G,True]
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
        return [G,False]

def ANALYZE_CONFLICT(G):
    maxi = find_max(G,'d_level')
    return maxi
    

def BACK_TRACK(G,b_level,cnf):
    dl_lst = find_node(G,'d_level',b_level)
    
    min_wl = find_max(G,'w_level')
    for i in dl_lst:#w_levelの最小値を探す
        tmp = G.node[i]['w_level']
        if(tmp<min_wl):
            min_wl = tmp
    
    wl_lst = find_node(G,'w_level',min_wl) #指定されたd_levelを持つノードのうち，最小のw_levelを持つノードのリスト
    
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


def DPLL(cnf):
    d_level = 0
    G = nx.DiGraph()
    
    [G,conflict] = BCP(cnf,G,d_level)
    if(conflict):
        print('Unsatisfiable!')
        return [False]
    
    while True:
        d_level += 1
        [G,sat] = DECIDE(cnf,G,d_level)
        if(sat): #充足可能
            node1 = find_node(G,'value',1) #1が割り当てられているリテラル
            node0 = find_node(G,'value',0) #0が割り当てられているリテラル
            node0 = [-1*i for i in node0]
            ans = sorted(node1+node0,key=abs) #結合して絶対値順でソート
            print('Satisfiable!')
            #nx.draw_networkx(G)
            #plt.show()
            return ans
        else:
            while True:
                [G,conflict] = BCP(cnf,G,d_level)
                if(not conflict): #コンフリクトしていない→（現時点では）バックトラックの必要無→break
                    break

                b_level = ANALYZE_CONFLICT(G)
                if(b_level==0): #一度もDECEDEせずにconflictしているということは，充足不可能
                    print('Unsatisfiable!')
                    return [False]
                else:
                    d_level = b_level-1
                    G = BACK_TRACK(G,b_level,cnf)



if __name__ == '__main__':
    test = [[-5,6],[-1,2],[-1,3,5],[-2,4],[-3,-4],[1,-2,5],[2,3],[2,-3]]
    print(DPLL(test))

