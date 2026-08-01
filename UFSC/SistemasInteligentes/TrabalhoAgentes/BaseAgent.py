"""

Agente De envio de mensagem em localhost
Gustavo Piaz Da Silva - 23200958 

"""




"""
IMPORTS
"""
from spade import agent, behaviour
from spade.message import Message
import asyncio

#=============================================================

class MyAgent(agent.Agent):
    async def setup(self):
        #print(f"Agente {self.jid} iniciado.")
        self.add_behaviour(self.SendBehaviour(period = 4))  
        self.add_behaviour(self.ReceiveBehaviour())
        self.choose = True

    class SendBehaviour(behaviour.PeriodicBehaviour):
        async def run(self):
            """
            for i in msga:
                msg = Message(to="AgentePedro@localhost")
                msg.body = i
                await self.send(msg)
                print(f"{msg.body}",end="")
                await asyncio.sleep(0.05)
            """
            msg = Message(to="AgentePedro@localhost")
            if self.agent.choose:
                msg.body = input("Defina o intervalo de numeros min,max: ")
                self.agent.choose = False
            else:
                msg.body = input("Digite um Numero: ")
            await self.send(msg)
            print(f"Enviado: {msg.body}")

            
    class ReceiveBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Mensagem recebida: {msg.body}")
                if msg.body == "correto":
                    await self.agent.stop()

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

