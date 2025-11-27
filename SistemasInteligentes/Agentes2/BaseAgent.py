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
from time import sleep
#=============================================================

def ShowMenu():
    print("""
    Digite o numero Correspondente ao que deseja:

    [1] [request]
    [2] [subscribe]
    [3] [history]
    """)

def ClearChat():
    os.system("clear" if os.name == 'posix' else 'cls')

class MyAgent(agent.Agent):
    async def setup(self):
        self.ChatHistory = []
        self.add_behaviour(self.SendBehaviour())  
        self.add_behaviour(self.ReceiveBehaviour())
        self.lastReceivedMSG = ""
    class SendBehaviour(behaviour.CyclicBehaviour):
        def ShowHistory(self):
            ClearChat()
            print("Historico de Comunicações")
            for chat in self.agent.ChatHistory:
                if chat is not None:
                    print(chat)
            input("Pressione Enter Para Retornar...")

        async def run(self):
            try:

                choose = await asyncio.get_event_loop().run_in_executor(
                    None, self.get_user_input
                )
                
                if choose == 3:
                    await asyncio.get_event_loop().run_in_executor(None, self.ShowHistory)
                    return
                    
                msg = Message(to="AgentePedro@localhost")
                
                if choose == 1:
                    msg.body = "qual o intervalo?"
                    msg.set_metadata("performative", "request")
                elif choose == 2:
                    msg.body = await asyncio.get_event_loop().run_in_executor(
                        None, input, "Digite um Valor para envio: "
                    )
                    msg.set_metadata("performative", "subscribe")
                
                if msg.body and msg.body.strip():
                    self.agent.ChatHistory.append(f"Enviado: {msg.body}")
                    await self.send(msg)
                    print(f"Mensagem enviada: {msg.body}")
                    
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Erro em SendBehaviour: {e}")

        def get_user_input(self):
            while True:
                try:
                    ClearChat()
                    ShowMenu()
                    if self.agent.lastReceivedMSG != "":
                        print(f"Ultima Mensagem Recebida: {self.agent.lastReceivedMSG }")
                    choice = int(input("Opção: "))
                    if 1 <= choice <= 3:
                        return choice
                    else:
                        print("Opção inválida! Digite 1, 2 ou 3.")
                except ValueError:
                    print("Por favor, digite um número válido.")

    class ReceiveBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            try:
                msg = await self.receive(timeout=1)  # Timeout menor para responsividade
                if msg:
                    received_msg = f"{msg.body}"
                    self.agent.ChatHistory.append(received_msg)
                    self.agent.lastReceivedMSG = received_msg
                    # Pequena pausa assíncrona em vez de sleep bloqueante

                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Erro em ReceiveBehaviour: {e}")

#=============================================================

if __name__ == "__main__":
    async def main():
        agt = MyAgent("AgtGustavo@localhost", "senha123")

        try:
            await agt.start(auto_register=True)
            print("Agente iniciado... Pressione Ctrl+C para encerrar.")
            
            # Manter o agente rodando
            while agt.is_alive():
                await asyncio.sleep(1)
                
        except Exception as e:
            print("Erro ao iniciar agente:", e)
        finally:
            if agt.is_alive():
                await agt.stop()
            print("Agente encerrado.")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEncerrando agente...")