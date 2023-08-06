import copy

from .static import ARR

class Chess:
    def __init__(self,id:int,name:str,belong:int,is_captain:bool,move:list[list[tuple]],tran_con:list[tuple],tran_move:list[list[tuple]],attr:dict[str],map_data):
        self.id = id
        self.name = name
        self.belong = belong
        self.is_captain = is_captain
        self.move = move
        self.tran_con = tran_con
        self.tran_move = tran_move
        self.attr = copy.copy(attr) # 每个棋子都有独特的attr
        self.map_data = map_data
        self.is_tran = False

    # 当前可移动位置
    @property
    def now_move(self):
        arr = self.map_data.get_chess_arr(self)
        move = list[list[int]]()
        for i in (self.tran_move if self.is_tran else self.move):
            move.append([])
            for j in i:
                if len(j) == 1: # 没有判断条件
                    move[-1].append(j[0])
                elif len(j) == 2:
                    if self.map_data.is_in_position(arr,j[1]):
                        move[-1].append(j[0])
        return move

class Map:
    def __init__(self,chesses:list,map:list[list[int]],rules:dict):
        self.chesses = chesses
        self.map = map
        self.rules = rules
        self.rl = len(self.map) # 地图行数
        self.cl = len(self.map[0]) # 地图列数
        self.red_move_ne = 0 # 红方移动中立棋子次数
        self.blue_move_ne = 0

    # 初始化棋盘，每局初始化一次
    def init_chessboard(self,win_func):
        self.win = win_func
        self.chessboard = list[list[Chess]]()
        for i in self.map:
            self.chessboard.append([])
            for j in i:
                if j:
                    self.chessboard[-1].append(Chess(j,*self.chesses[j - 1],self))
                else:
                    self.chessboard[-1].append(None)

    # 根据方向距离返回目标棋盘格
    def get_arr_by_rd(self,arr:ARR,r:int,d:int) -> ARR:
        rs_list = {
            1:(-1,-1),
            2:(-1,0),
            3:(-1,1),
            4:(0,-1),
            5:(0,1),
            6:(1,-1),
            7:(1,0),
            8:(1,1)
        } # 方向对应列表
        d_arr = (arr[0] + rs_list[r][0] * d,arr[1] + rs_list[r][1] * d)
        if 0 <= d_arr[0] < self.rl and 0 <= d_arr[1] < self.cl:
            return d_arr
        return None

    # 获取棋子位置
    def get_chess_arr(self,chess:Chess):
        for i in range(self.rl):
            for j in range(self.cl):
                if self.chessboard[i][j] is chess:
                    return (i,j)

    # 根据id获取棋子位置
    def get_chess_arr_by_id(self,id:int):
        x = None
        for i in range(self.rl):
            for j in range(self.cl):
                if self.chessboard[i][j] and self.chessboard[i][j].id == id:
                    if x:
                        return None
                    x = (i,j)
        return x

    # 棋子位置是否符合规则
    def is_in_position(self,arr:ARR,loc:list[tuple]):
        get_abs_pos = lambda a,al:(a - 1) if a > 0 else a + al # 把输入的含正负坐标转换为0-n的坐标
        for i in loc:
            command = i[0]
            if command == "X": # 函数X（行）
                for j in i[1:]:
                    if arr[0] == get_abs_pos(j,self.rl):
                        return True
            elif command == "Y": # 函数Y（列）
                for j in i[1:]:
                    if arr[1] == get_abs_pos(j,self.cl):
                        return True
            elif command == "P": # 函数P（点）
                for j in range(1,len(i),2):
                    if arr == (get_abs_pos(i[j],self.rl),get_abs_pos(i[j + 1],self.cl)):
                        return True
            for j in self.ext_manager.loc_rules: # 扩展中的函数
                if command == j:
                    if self.ext_manager.loc_rules[j](i[1:],arr):
                        return True
        return False

    # 是否可以吃子
    def can_eat(self,chess1:Chess,chess2:Chess):
        return chess1.belong != 3 and chess2.belong != 3 and chess1.belong != chess2.belong

    # 移动棋子
    def move(self,arr1:ARR,arr2:ARR,turn:int):
        if self.rules["restrict_move_ne"] and self.chessboard[arr1[0]][arr1[1]] and self.chessboard[arr1[0]][arr1[1]].belong == 3:
            if turn == 1:
                self.red_move_ne += 1
            else:
                self.blue_move_ne += 1
        else:
            if turn == 1:
                self.red_move_ne = 0
            else:
                self.blue_move_ne = 0
        if arr1 != arr2 and self.chessboard[arr2[0]][arr2[1]] and self.chessboard[arr2[0]][arr2[1]].is_captain:
            self.win(turn)
        self.chessboard[arr1[0]][arr1[1]],self.chessboard[arr2[0]][arr2[1]] = None,self.chessboard[arr1[0]][arr1[1]]
        if self.rules["tran"]:
            self.tran()

    # 棋子升变
    def tran(self):
        for i in range(self.rl):
            for j in range(self.cl):
                chess = self.chessboard[i][j]
                if not chess:
                    continue
                if chess.is_tran:
                    continue
                if self.is_in_position((i,j),chess.tran_con):
                    chess.is_tran = True

    # 添加棋子
    def add_chess(self,id:int,arr:ARR):
        self.chessboard[arr[0]][arr[1]] = Chess(id,*self.chesses[id - 1],self)
