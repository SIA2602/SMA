import time
import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class SenderAgent(Agent):
    PrimeiroGrau = False  #Variavel que indica que ele sabe o grau
    listaDeEnviados = []
    listaDeRecebidos = []

    class comunica(OneShotBehaviour):
        async def run(self):
            msg = Message(to="acir@jix.im")  # Instantiate the message
            msg.set_metadata("performative",
                             "inform")  # Set the "inform" FIPA performative
            msg.body = "Grau?"  # Set the message content

            await self.send(msg)

            msg = await self.receive(timeout=5)
            if msg:
                if (msg.body == "1grau"):
                    print("Mensagem recebida: {}".format(msg.body))
                    SenderAgent.PrimeiroGrau = True
            else:
                print(
                    "Não foi recebida nenhuma mensagem no intervalo de 5s...")

    class enviaValor(CyclicBehaviour):
        async def run(self):
            #caso seja uma funcao do primeiro grau e a lista de enviados e recebidos seja menor que 2
            if (SenderAgent.PrimeiroGrau == True
                    and len(SenderAgent.listaDeEnviados) < 3):
                msg = Message(to="acir@jix.im")  # Instantiate the message
                msg.set_metadata(
                    "performative",
                    "inform")  # Set the "inform" FIPA performative

                msg.body = str(int(random.randint(
                    -100, 100)))  # Set the message content
                await self.send(msg)
                print("Valor enviado: {}".format(msg.body))
                SenderAgent.listaDeEnviados.append(
                    msg.body)  #colocando valor enviado na lista
                SenderAgent.primeiraTroca = False  #ja foi realizada a primeira troca de mensagem

                msg = await self.receive(timeout=5)
                if msg:
                    print("Valor recebido: {}".format(msg.body))
                    SenderAgent.listaDeRecebidos.append(
                        msg.body)  #colocando valor enviado na lista
                else:
                    print(
                        "Não foi recebida nenhuma mensagem no intervalo de 5s..."
                    )

            #caso seja uma funcao do primeiro grau e a lista de enviados e recebidos seja maior ou igual que 2
            elif (SenderAgent.PrimeiroGrau == True
                  and len(SenderAgent.listaDeRecebidos) >= 3):
                SenderAgent.listaDeRecebidos.pop(0)
                SenderAgent.listaDeEnviados.pop()

                msg = Message(to="acir@jix.im")  # Instantiate the message
                msg.set_metadata(
                    "performative",
                    "inform")  # Set the "inform" FIPA performative

                #print(SenderAgent.listaDeRecebidos,SenderAgent.listaDeEnviados)

                #calculando variaveis
                tamanhoList = len(SenderAgent.listaDeRecebidos) - 1
                a = (int(SenderAgent.listaDeRecebidos[-1]) -
                     int(SenderAgent.listaDeRecebidos[tamanhoList - 1])) / (
                         int(SenderAgent.listaDeEnviados[-1]) -
                         int(SenderAgent.listaDeEnviados[tamanhoList - 1]))
                #print("Valor a: {}".format(a))

                b = int(SenderAgent.listaDeRecebidos[tamanhoList - 1]) - (
                    (int(SenderAgent.listaDeRecebidos[-1]) -
                     int(SenderAgent.listaDeRecebidos[tamanhoList - 1])) /
                    (int(SenderAgent.listaDeEnviados[-1]) -
                     int(SenderAgent.listaDeEnviados[tamanhoList - 1]))) * int(
                         SenderAgent.listaDeEnviados[tamanhoList - 1])
                #print("Valor b: {}".format(b))

                x = int(-int(b) / int(a))

                msg.body = str(x)  # Set the message content
                await self.send(msg)
                print("Valor enviado: {}".format(msg.body))
                SenderAgent.listaDeEnviados.append(
                    msg.body)  #colocando valor enviado na lista

                msg = await self.receive(timeout=5)
                if msg:
                    print("Valor recebido: {}".format(msg.body))
                    SenderAgent.listaDeRecebidos.append(
                        msg.body)  #colocando valor enviado na lista
                    if (msg.body == "0"):
                        print("finished")
                        exit()
                else:
                    print(
                        "Não foi recebida nenhuma mensagem no intervalo de 5s..."
                    )
                # stop agent from behaviour
                #await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.comunica()
        self.add_behaviour(b)
        b = self.enviaValor()
        self.add_behaviour(b)


if __name__ == "__main__":
    senderagent = SenderAgent("miro30i10@jix.im", "sistemasinteligentes")
    senderagent.start()

    while senderagent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
    print("Agent finished")
