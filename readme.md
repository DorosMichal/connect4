# Implementacja gry connect4 oraz gracza MCTS

### Game
Klasa gry jest generyczną grą turową dla dwóch graczy.
Prowadzi rozgrywkę wołając na przemian graczy oraz sprawdza czy ruchy są prawidłowe i czy gra się zakończyła korzystajac z metod klasy GameState

### GameState
Reprezentuje stan generycznej gry - utrzymuje planszę, liczbę ruchów, jest w stanie sprawdzić czy gra się zakończyła.

### ConnectNState
Implementacja konkretnie gry ConnectN.
Reprezentuje planszę jako tablicę liczb [Y, X], ma również licznik ile jest już krążków w każdej kolumnie.
Ma również policzone na początku winning_schemas - wszystkie konfiguracje wygrywające - dzieki czemu może szybko sprawdzać czy dany ruch jest wygrywający.

### Player
Gra przyjmuje instancje dwóch graczy, którzy będą w nią grali poprzez wykonywanie metody make_move, mogą oni również implementować metodę end, która może być wykonana na końcu gry, aby np. poinformować graczy o wyniku

### ManualPlayer
Komunikuje się z użytkownikiem przy pomocy konsoli tekstowej i w ten sposób wykonuje ruchy.

### RandomPlayer
Wykonuje losowe ruchy

### MCTSPlayer
Odpytuje algorytm MCTS o najlepszy ruch i gra zgodnie z jego odpowiedzią

### MCTS
Implementacja klasycznego Monte Carlo Tree Search, wystawia publiczne metody make_best_move oraz make_opponents_move, pierwsza proponuje najlepszy ruch po przeszkuaniu drzewa, druga aktualizuje stan drzewa po wykoaniu ruchu przez przeciwnika.

### MCTS_Node
Klasa reprezentująca pojedynczy wierzchołek drzewa (czyli pewien stan gry). Posiada atrybuty/metody takie jak:
 - move - jaki ruch reprezentuje pójście do tego wierzchołka
 - priority() - z jakim priorytetem powinniśmy odwiedzić dany wierzchołek patrząc po porzednich wynikach
 - rollout() - przeprowadzenie losowej symulacji z tego wierzchołka