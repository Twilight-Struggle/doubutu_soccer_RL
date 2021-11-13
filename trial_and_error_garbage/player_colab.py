class GreedyPlayer:
    def __init__(self, device):
        self.device = device
        self.model = DQN().to(device)
        checkpoint = torch.load("")
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.eval()
        self.features = np.empty((1, 9, 5, 3), np.float32)

    def action(self, Board):
        with torch.no_grad():
            self.features[0] = Board.tensor_state_parsed()
            state = torch.from_numpy(self.features).to(self.device)
            q = self.model(state)
            # 合法手に絞る
            legalmoves_num_act_dict = Board.legalmoves_to_num_parsed()
            legal_moves = list(legalmoves_num_act_dict.keys())
            next_actions = torch.tensor([legal_moves],
                                        device=self.device,
                                        dtype=torch.long)
            legal_q = q.gather(1, next_actions)
            return legalmoves_num_act_dict[legal_moves[legal_q.argmax(
                dim=1).item()]]


class RandomPlayer:
    def __init__(self):
        pass

    def action(self, Board):
        not_lose = []
        legalmoves = Board.legal_moves()
        legalmoves_p = Board.parse_legal_moves()
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

    def action(self, Board):
        while True:
            legalmoves = Board.legal_moves()
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


class MonteCarlo:
    def __init__(self):
        pass

    def policy(self, Board):
        not_lose = []
        legalmoves = Board.legal_moves()
        legalmoves_p = Board.parse_legal_moves()
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
        if len(not_lose) != 0:
            ret_index = not_lose[random.randrange(len(not_lose))]
        else:
            # print("Error: not_lose is 0")
            # print(legalmoves)
            # print(legalmoves_p)
            ret_index = 0
        return legalmoves[ret_index]

    def trial(self, Board, act):
        kaisu = 0
        tempboard = Board.clone()
        myturn = tempboard.turn
        success, winner = tempboard.action_parser(act)
        if not success:
            print("act is not recieved")
        if winner is not None:
            if winner == myturn:
                return 10
            else:
                return -10
        while True:
            kaisu += 1
            legal_moves_l = tempboard.legal_moves()
            # if len(legal_moves_l) == 0:
            #     print("trial legalmove is 0:kaisu is {}".format(kaisu))
            #     tempboard.display()
            #     print(tempboard.turn)
            while True:
                if len(legal_moves_l) == 0:
                    action = None
                else:
                    action = self.policy(tempboard)
                success, winner = tempboard.action_parser(action)
                if success is True:
                    break
                else:
                    print("fuck")
            if winner is not None:
                if winner == myturn:
                    return 1
                else:
                    return -1

    def action(self, Board):
        scores = {}
        n = 50
        legalmoves = Board.legal_moves()
        for i, act in enumerate(legalmoves):
            scores[i] = 0
            for j in range(n):
                scores[i] += self.trial(Board, act)
            scores[i] /= n

        max_score = max(scores.values())
        for i, v in scores.items():
            if v == max_score:
                return legalmoves[i]
