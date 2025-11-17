"""

Agente De envio de mensagem em localhost utilizando metadatas para validação
Gustavo Piaz Da Silva - 23200958 

"""




"""
IMPORTS
"""
from spade import agent, behaviour
from spade.message import Message
import asyncio
import os

#=============================================================
def ShowMenu():
    print("""
    Digite o numero Correspondente ao que deseja:

    [1] [request]
    [2] [subscribe]
    [3] [history]
    """)


def ClearChat():
    os.system("clear")

class MyAgent(agent.Agent):
    async def setup(self):
        #print(f"Agente {self.jid} iniciado.")
        self.ChatHistory = []
        self.add_behaviour(self.SendBehaviour(period = 4))  
        self.add_behaviour(self.ReceiveBehaviour())

    class SendBehaviour(behaviour.PeriodicBehaviour):
        def ShowHistory(self):
            print("Historico de Comunicações")
            ClearChat()
            for chat in self.agent.ChatHistory:
                if chat is not None:
                    print(chat)
            input("Pressione Enter Para Retornar...")

        async def run(self):
            msg = Message(to="AgentePedro@localhost")
            choose = 10
            while choose > 3 or choose < 1:
                ClearChat()
                ShowMenu()
                choose = int(input())

            if choose == 1:
                msg.body = "[request] qual Intervalo?"
            elif choose == 2:
                msg.body = "[subscribe] " + input("Digite um Valor para envio: ") 
            elif choose == 3:
                self.ShowHistory()
            if msg.body != "":
                self.agent.ChatHistory.append(msg.body)
            await self.send(msg)
            print(f"{msg.body}")

            
    class ReceiveBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.ChatHistory.append(msg.body)
                print(f"{msg.body}")

#=============================================================

if __name__ == "__main__":


    async def main():


        agt = MyAgent("AgtGustavo@localhost", "senha123")


        try:

            await agt.start(auto_register=True)
        except Exception as e:
            print("Erro ao iniciar agente:", e)
        print("Agente iniciado...")

        while True:
            await asyncio.sleep(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Encerrando agente...")

