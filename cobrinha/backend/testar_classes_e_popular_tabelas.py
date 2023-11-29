from servidor import *


# cria um jogador
jogador1 = Jogador(id= 1, nome="Jack Good", pontuacao= 5)
jogador2 = Jogador(id= 2, nome="Maria", pontuacao= 6)
db.session.add(jogador1)
db.session.add(jogador2)
db.session.commit()

print(jogador1, jogador2)
print("Dados inseridos")
