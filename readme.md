Uruchomienie tuningu na superkomputerze Ares:

`sbatch sc.sh`

Konfiguracja Irace znajduje się w pliku `tuning/parameters.txt` (wartości parametrów algorytmu) oraz w pliku `tuning/scenario.txt` (liczba wykonań algorytmu podczas tuningu).

Skrypt `graph.py` służy utworzeniu wykresów.

Podczas wykonania algorytmu wywołanie funkcji `save_population()` zapisuje informacje o populacji do pliku CSV, które następnie można zwizualizować. Do tuningu należy zakomentować linię 237, w której znajduje się to wywołanie.

Sprawdzenie stanu uruchomionych zadań:

`squeue`

Sprawdzenie zużycia przestrzeni dyskowej:

`hpc-fs`
