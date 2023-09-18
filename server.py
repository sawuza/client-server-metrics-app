import asyncio


class ServerError(BaseException):
    pass


class ClientServerProtocol(asyncio.Protocol):
    repository = {}

    def process_data(self, data):
        try:
            data = data[:len(data) - 1].split(" ")
            resp = "ok\n"

            if data[0] == "put":
                if len(data) != 4:
                    raise ServerError
                data = [str(data[0]), str(data[1]), float(data[2]), int(data[3])]

                if data[1] not in self.repository:
                    self.repository[data[1]] = []
                    self.repository[data[1]].append((data[2], data[3]))

                if data[1] in self.repository:
                    update = False
                    for i in range(len(self.repository[data[1]])):
                        if data[3] == self.repository[data[1]][i][1]:
                            self.repository[data[1]][i] = (data[2], data[3])
                            update = True
                            break
                    if not update:
                        self.repository[data[1]].append((data[2], data[3]))

                return resp + "\n"

            if data[0] == "get":
                if len(data) != 2:
                    raise ServerError
                data = [str(data[0]), str(data[1])]

                if data[1] == "*":
                    for i in self.repository:
                        for j in range(len(self.repository[i])):
                            resp += f"{i} {self.repository[i][j][0]} {self.repository[i][j][1]}\n"
                if data[1] in self.repository:
                    for num in range(len(self.repository[data[1]])):
                        resp += f"{data[1]} {self.repository[data[1]][num][0]} {self.repository[data[1]][num][1]}\n"
                return resp + "\n"
            raise ServerError
        except BaseException:
            return "error\nwrong command\n\n"

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
