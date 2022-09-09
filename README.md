# E-platforma dla szkoły

## Autor
Autorem projektu jest Jakub Klonowski (jakubpklonowski@gmail.com).

## Opis
Projekt to aplikacja webowa typu e-dziennik, przeznaczona dla szkoły. 
W ramach aplikacji mogą poruszać się trzy rodzaje użytkowników: gość, uczeń i nauczyciel. 
Każdemu rodzajowi użytkownika przysługują inne uprawnienia w ramach aplikacji.

Gość może wyświetlić stronę główną, ogłoszenia, zalogować i zarejestrować się.

Uczeń może przeglądać dodatkowo swoje oceny, wymaga zalogowania.

Nauczyciel może dodatkowo przeglądać i wystawiać oceny, publikować ogłoszenia, przeglądać listę uczniów. 
Wymaga bycia zalogowanym.

## Funkcjonalności:
- rejestracja, logowanie i sesje użytkowników;
- różne poziomy uprawnień użytkowników;
- wprowadzanie do bazy danych informacji np ogłoszeń, ocen;
- wyświetlanie danych zgromadzonych w bazie.

## Technologie
Projekt powstał w języku CPython, z wykorzystaniem frameworka Flask i bazy SQLite.

## Uruchomienie projektu
### Inicjalizacja bazy
- flask db init
- flask db migrate
- flask db upgrade

## Kierunki rozwoju
- zmiana struktury bazy danych np. rozbicie tabeli User na Students i Teacher;
- udostępnienie narzędzi do edycji i usuwania wprowadzonych danych np. loginów, ocen, ogłoszeń.