
"""


Nome: Pedro Thomas Silveira de Alcantara
Matricula: 23200955
Agente de Recebimento e Validação Utilizando valores randomicos e metadatas


"""

# BIBLIOTECAS

from spade import agent, behaviour
from spade.message import Message
from os import system
import asyncio
from random import randint

def ThinkNumber():
    val = randint(0,1000)
    intervalmin = randint(0, val)
    intervalmax = randint(val, 1000)
    return val, str(intervalmin) , str(intervalmax)

    

class MyAgent(agent.Agent):
    async def setup(self):
        self.number,self.intervalmin,self.intervalmax = ThinkNumber()
        self.msgToSend = ""
        self.msgRCV = ""
        self.add_behaviour(self.ReceiveBehaviour())   
        self.add_behaviour(self.SendBehaviour(period=1))

    class ReceiveBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.msgRCV = msg.body
                print(f"Mensagem recebida: {msg.body}")

    class SendBehaviour(behaviour.PeriodicBehaviour):

        def TextToCommand(self):
            if "[request]" in self.agent.msgRCV:
                self.agent.msgToSend = f"[inform] O intervalor é ({self.agent.intervalmin},{self.agent.intervalmax})"
            elif "[subscribe]" in self.agent.msgRCV: #Recebe no tipo [subscribe] int
                ReceivedValue = int(self.agent.msgRCV.strip().split()[-1])

                if ReceivedValue < self.agent.number:
                    self.agent.msgToSend = "[failure] >"
                elif ReceivedValue > self.agent.number:
                    self.agent.msgToSend = "[failure] <"
                elif ReceivedValue == self.agent.number:
                    self.agent.msgToSend = f"[inform-done] {self.agent.number} Valor Correto"
                else:
                    self.agent.msgToSend = f"[error] linguagem não aceita"
                    

            
        async def run(self):
            if not self.agent.msgRCV or self.agent.msgRCV == "":
                return  
            try:
                self.TextToCommand()
                msg = Message(to="AgtGustavo@localhost")
                msg.body = self.agent.msgToSend
                await self.send(msg)
                print(f"Mensagem enviada: {msg.body}")
                
                self.agent.msgRCV = ""
                
            except ValueError:
                print(f"Erro: mensagem recebida não é um número válido: '{self.agent.msgRCV}'")
                self.agent.msgRCV = ""  

async def main():
    agt = MyAgent("AgentePedro@localhost", "senha123")
    try:
        await agt.start(auto_register=True)
    except Exception as e:
        print("Erro ao iniciar agente:", e)
        return

    await asyncio.sleep(1)
    #   system("clear")
    print("Agente iniciado. Pressione CTRL+C para sair.\n")

    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("Encerrando agente...")
        await agt.stop()

if __name__ == "__main__":
    asyncio.run(main())