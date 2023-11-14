Program służy do grania w grę zwaną "Pan" z botem. Poziom przeciwnika nie jest oszałamiająco mocny, jednym z powodów takiego stanu rzeczy jest fakt iż sam nie jestem najlepszym graczem tej gry i zbytnio nie mam pomysłu jak skutecznie usprawnić mechanikę programu. Mógłbym to zrobić natomiast kosztowałoby to program znacznie większego wydatku obliczeniowego co byłoby niemiarodajne.
Natomiast uważam, że rozgrywka z takim przeciwnikiem dla początkujących graczy może być wyzwaniem.

Bot podejmuje decyzje w oparciu o analize przyszłych, potencjalnych ruchów zarówno swoich jak i przeciwnika.
Jedyny algorytm jakim się posługuje bot do oceny danego posunięcia  jest analiza swojej siły ręki w stosunku do siły ręki przeciwnika. Co prawda nie jest to rozbudowany system podejmowania decyzji, natomiast jak na swój minimalizm sprawdza się w wielu posunięciach całkiem przyzwoicie.

Uruchomienie:
-
1. Pobierz aplikację i załącz ją,
2. Wchodząc w ustawienia możesz wybrać poziom przeciwnika. Im wyższy tym dłużej przeciwnik będzie podejmował ruch,
3. Zasady zgodne z tymi samymi, które obowiązują na stronie www.kurnik.pl,
4. Rozgrykwa rozpoczyna się po naciśnięciu przycisku "Rozpocznij grę",
5. Aby zagrać kartę lub kilka na raz należy kliknąć w interesujące nas karty (ręka gracza jest pokazana na dole), a następnie nacisnąć przycisk "Zagraj". Ponowne kliknięcie na tą samę kartę "odznacza ją".

<b> Głównie korzystałem z: </b>

1. Pygame,
2. Sqlalchemy,
3. Drzewo decyzyjne,
4. Rekurencja.

Całość grafik wykonałem samodzielnie. Kilka rzeczy jest jeszcze do poprawienia. Ruch bota przerywa wątek główny przez co interfejs gry nie reaguje na komendy gracza.
Optymalizacja drzewa decyzyjnego (skrócenie czasu podejmowania decyzji przez bota). Zwiększenie poziomu programu.

Zasady gry:
-
Gracze na zmianę wykonują swój ruch. Jest kilka dostępnych zagrań:
1. Wyłożenie pojedynczej karty,
2. Wyłożenie 4 kart o takiej samej wartości,
3. Dobranie kart.

Grę zawsze zaczyna gracz który posiada dziewiątke serce. Ta karta musi zostać wyłożona na stół w pierwszym ruchu i już nigdy go nie opuszcza. Karta zagrana musi być równej lub większej wartości jak karta, która została jako ostatnia wyłożona na stół.

Można również zagrać 4 karty o takich samych figurach na raz. Obowiązują te same zasady co w przypadku zagrywania pojedynczej karty. Wyjątek stanowią dziewiątki. Można zagrać 4 na raz lub 3 na raz (w tym wypadku tylko i wyłącznie, gdy dziewiątka serce znajduje się już na stole).

Kolejną z dostępnych opcji jest dobranie kart. Karty dobieramy ze stołu i dobieramy zawsze 3 (pod warunkiem, że odpowiednia ilość kart znajduje się na stole). Dobieramy z góry kupki (zaczynając od tych, które zostały wyłożone jako ostatnie), karta która została na samej górze, od tej pory jest traktowana jako ostatnio wyłożona. Jeżeli na stole leży tylko jedna karta (dziewiątka serce) lub nie ma żadnej, to nie można dobierać kart. Jeżeli kart na stole jest mniej niż 4, to gracz dobiera tyle kart ile może (poza 9 serce, ona po zagraniu zawsze zostaje na stole)

Wygrywa gracz, który jako pierwszy wyłoży swoje karty na stół.