import hisock
import _shared as shared
import random


class ServerData:
    def __init__(self):
        self.client_pairs: list[list] = []

    def add_client(self, clt_data):
        if not self.client_pairs:
            # clt data(s), conn4 board, num confirmations of replay
            self.client_pairs.append([clt_data, shared.Board(), 0])
            return

        # Last element in list is always the most recently updated
        last = self.client_pairs[-1]
        if len(last) == 3:
            # Only one client is connected in this pair
            last.insert(1, clt_data)

            # List now: [client_one, client_two, board]
            goes_first = random.choice((0, 1))
            goes_last = not goes_first
            server.send_client(
                last[goes_first],
                "start",
                {"turn": "first", "opp_name": last[goes_last].name},
            )
            server.send_client(
                last[goes_last],
                "start",
                {"turn": "last", "opp_name": last[goes_first].name},
            )
        else:
            # Both are connected; no open spots, create one
            self.client_pairs.append([clt_data, shared.Board()])

    def remove_client(self, clt_data):
        for client_pair in self.client_pairs[:]:
            if clt_data in client_pair:
                if len(client_pair) == 3:
                    other_client_idx = not client_pair.index(clt_data)

                    print(
                        f"[DEBUG] Left clt: {clt_data}, Other clt: {client_pair[other_client_idx]}\n"
                        f"List of paired clients: {self.client_pairs}\nTime: {__import__('time').time()}"
                    )

                    other_client = client_pair[other_client_idx]
                    self.client_pairs.remove(client_pair)

                    server.send_client(
                        client_pair[other_client_idx],
                        "disconn",
                        b"Opponent Disconnected",
                    )

                    server.disconnect_client(other_client, force=False)
                else:
                    self.client_pairs.remove(client_pair)
                print("[DEBUG] BYE BYE CLIENTS")
                break

    def find_client(self, clt_data):
        for client_pair in self.client_pairs:
            if clt_data in client_pair:
                return client_pair


addr, port = hisock.input_server_config()
server = hisock.HiSockServer((addr, port))

data = ServerData()


@server.on("join")
def on_join(clt_data):
    data.add_client(clt_data)
    clt_pair = data.find_client(clt_data)

    print(f"Player {clt_data.name} joined, total players {len(server.clients)}\n"
          f"    - Paired? {len(clt_pair) == 4}\n"
          f"    - Client obj: {clt_data}\n"
          f"    - Board obj: {clt_pair[-2]}")


@server.on("leave")
def on_leave(clt_data):
    print(f"[DEBUG] in on_leave: {clt_data} LEFT, REMOVING CLIENT")
    data.remove_client(clt_data)
    print(data.client_pairs)


@server.on("replay")
def on_replay(clt_data):
    client_pair = data.find_client(clt_data)
    client_pair[3] += 1

    if client_pair[3] == 2:
        client_pair[2].reset()
        client_pair[3] = 0
        server.send_client(client_pair[0], "replay_confirm")
        server.send_client(client_pair[1], "replay_confirm")
    else:
        print("YEE")
        print(client_pair[1 - client_pair.index(clt_data)])
        server.send_client(client_pair[1 - client_pair.index(clt_data)], "opp_replay")


@server.on("player_exit")
def on_player_exit(clt_data):
    clt_pair = data.find_client(clt_data)
    server.disconnect_client(clt_pair[0])
    server.disconnect_client(clt_pair[1])


@server.on("turn_made")
def on_turn_made(clt_data, move_info: dict):
    x, y = move_info["x"], move_info["y"]

    client_pair = data.find_client(clt_data)
    client_pair[2].board[y][x] = move_info["piece"]

    other_client = client_pair[not client_pair.index(clt_data)]

    if client_pair[2].player_win((x, y)):
        server.send_client(clt_data, "win")
        server.send_client(other_client, "lose")

    server.send_client(
        other_client, "new_move", {"opp_move": [x, y], "opp_piece": move_info["piece"]}
    )

    client_pair[2].total_moves += 1
    if client_pair[2].total_moves % 2 == 0:
        for client in (clt_data, other_client):
            server.send_client(client, "new_turn", client_pair[2].total_moves // 2 + 1)

print("Successfully started server!")

server.start()