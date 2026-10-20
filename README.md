# Labirinto

O programa procura um caminho da entrada `I` até a saída `F`. As paredes são `#` e os espaços livres são `.`. O labirinto tem 10 por 10 casas.

O programa mostra o caminho que cada busca encontrou. A DFS usa uma pilha, a BFS usa uma fila e a gulosa escolhe a casa que parece mais perto da saída. Para essa estimativa, ela conta a distância até a saída sem levar as paredes em conta.

As buscas guardam de qual casa vieram para poder montar o caminho no final. O tamanho é contado em passos. Casas visitadas são as casas que o algoritmo pegou da pilha ou fila para processar.

| Busca | Passos | Casas visitadas |
| DFS   | 28     | 30 |
| BFS   | 18     | 41 |
| Gulosa| 28     | 30 |

A BFS achou o caminho mais curto. A DFS e a gulosa foram pela parte de cima e acharam um caminho maior. A gulosa foi nessa direção porque parecia que estava chegando mais perto da saída, mas uma parede bloqueou a descida.