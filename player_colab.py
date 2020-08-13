class GreedyPlayer:
    def __init__(self, device):
        self.device = device
        self.model = DQN().to(device)
        checkpoint = torch.load("")
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.eval()
        self.features = np.empty((1, 9, 5, 3), np.float32)

    def tensor_state(self, board_cells):
        tensored_board = np.empty((9, 5, 3), dtype=np.float32)
        piece_list = ["さ", "り", "う", "お", "サ", "リ", "ウ", "オ", "ボ"]
        for i in range(9):
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if board_cells[y][x] == piece_list[i]:
                        tensored_board[i][y][x] = 1
                    else:
                        tensored_board[i][y][x] = 0
        return tensored_board

    def tensor_state_parsed(self, Board):
        cells = []
        if Board.turn == PlayPos.BACKPLAYER:
            piece_dict = {
                "サ": "さ",
                "リ": "り",
                "ウ": "う",
                "オ": "お",
                "さ": "サ",
                "り": "リ",
                "う": "ウ",
                "お": "オ",
                "ボ": "ボ"
            }
            for i in range(BOARD_HEIGHT):
                yokocell = Board.cells[BOARD_HEIGHT - 1 - i]
                newyokocell = []
                for nakami in yokocell[::-1]:
                    if nakami is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(piece_dict[nakami.identity])
                cells.append(newyokocell)
        else:
            for i in range(BOARD_HEIGHT):
                newyokocell = []
                for j in range(BOARD_WIDTH):
                    if Board.cells[i][j] is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(Board.cells[i][j].identity)
                cells.append(newyokocell)
        return self.tensor_state(cells)

    def action(self, Board, legalmoves):
        with torch.no_grad():
            self.features[0] = self.tensor_state_parsed(Board)
            state = torch.from_numpy(self.features).to(self.device)
            q = self.model(state)
            # 合法手に絞る
            legalmoves_num_act_dict = Board.legalmoves_to_num_parsed()
            legal_moves = list(legalmoves_num_act_dict.keys())
            next_actions = torch.tensor([legal_moves],
                                        device=self.device,
                                        dtype=torch.long)
            legal_q = q.gather(1, next_actions)
            return legalmoves_num_act_dict[legal_q.argmax(dim=1).item()]


class Random:
    def __init__(self):
        pass

    def parse_board(self, Board, turnplayer):
        cells = []
        piece_number_dict = {
            "さ": 0,
            "り": 1,
            "う": 2,
            "お": 3,
            "サ": 4,
            "リ": 5,
            "ウ": 6,
            "オ": 7,
            "ボ": 8,
        }
        if turnplayer == PlayPos.BACKPLAYER:
            piece_dict = {
                "サ": "さ",
                "リ": "り",
                "ウ": "う",
                "オ": "お",
                "さ": "サ",
                "り": "リ",
                "う": "ウ",
                "お": "オ",
                "ボ": "ボ"
            }
            for i in range(BOARD_HEIGHT):
                yokocell = Board.cells[BOARD_HEIGHT - 1 - i]
                newyokocell = []
                for nakami in yokocell[::-1]:
                    if nakami is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(
                            piece_number_dict[piece_dict[nakami.identity]])
                cells.append(newyokocell)
        else:
            for i in range(BOARD_HEIGHT):
                newyokocell = []
                for j in range(BOARD_WIDTH):
                    if Board.cells[i][j] is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(
                            piece_number_dict[Board.cells[i][j].identity])
                cells.append(newyokocell)
        return cells

    def parse_action(self, legal, turnplayer):
        parsed_legalmoves = []
        if turnplayer == PlayPos.BACKPLAYER:
            for action in legal:
                piece_dict = {"サ": "さ", "リ": "り", "ウ": "う", "オ": "お"}
                new_move_command = [
                    BOARD_HEIGHT - 1 - action.move_command[0],
                    BOARD_WIDTH - 1 - action.move_command[1],
                    piece_dict[action.move_command[2]]
                ]
                new_kick_commands = None
                if action.kick_command is not None:
                    new_kick_commands = []
                    for kick_to in action.kick_command:
                        if kick_to is not None:
                            new_kick_to = [
                                BOARD_HEIGHT - 1 - kick_to[0],
                                BOARD_WIDTH - 1 - kick_to[1]
                            ]
                        else:
                            new_kick_to = None
                        new_kick_commands.append(new_kick_to)
                new_action = Act(new_move_command, new_kick_commands)
                parsed_legalmoves.append(new_action)
        else:
            parsed_legalmoves = legal
        return parsed_legalmoves

    def action(self, Board, legalmoves):
        not_lose = []
        legalmoves_p = self.parse_action(legalmoves, Board.turn)
        for i, action in enumerate(legalmoves_p):
            if action.kick_command is None:
                not_lose.append(i)
            else:
                lose_flag = False
                last_stop = action.kick_command[-1]
                if last_stop[0] == -1:
                    lose_flag = True
                elif last_stop[0] == 5:
                    return legalmoves[i]
                if not lose_flag:
                    not_lose.append(i)
        ret_index = not_lose[random.randrange(len(not_lose))]
        return legalmoves[ret_index]


class Human:
    def __init__(self):
        pass

    def action(self, Board, legalmoves):
        while True:
            print("合法手")
            for i, action in enumerate(legalmoves):
                printn(str(i) + '):')
                printn(action.move_command)
                printn(" ")
                print(action.kick_command)
            tmp = input()
            try:
                inp = int(tmp)
                ret = legalmoves[inp]
                break
            except Exception:
                pass
        return ret