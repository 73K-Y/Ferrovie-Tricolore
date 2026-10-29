# Diario di bordo

Cosa è cambiato a ogni sessione, dal più recente. Lo stato attuale del progetto sta nel [README](README.md).

🟢 funziona, provato davvero &nbsp; 🟡 funziona con un limite &nbsp; 🔴 ancora aperto

---

### 28 ottobre 2026 &nbsp;·&nbsp; Porta Nuova prende vita

Due giorni passati quasi tutti dentro la stazione. Porta Nuova adesso ha tabelloni, tornelli, arredi e linea aerea, e i treni IA si comportano meglio. Fuori dalla stazione la linea aerea arriva fino a Lingotto.

| | Cosa | Note |
|---|---|---|
| 🟢 | Tabelloni arrivi/partenze di Porta Nuova | LED ambra, orologio e pubblicità al centro, solo treni veri (giocatori + IA) |
| 🟢 | Ora italiana corretta ovunque | il calcolo dell'ora legale sbagliava il giorno del cambio: corretto in 72 script |
| 🟢 | Annunci | partenza al momento della richiesta, arrivi in tutte le stazioni, altoparlante di Porta Nuova sistemato |
| 🟢 | Tabelloni al sedersi | il treno del giocatore compare su cartelli e tabelle quando si siede in cabina |
| 🟢 | Tornelli ai binari | 4 varchi, si entra solo con il biglietto, porte che si richiudono dopo 1 s |
| 🟢 | Linea aerea Porta Nuova → Lingotto | pali a ombrello e singoli scelti in base ai binari, nessun filo che finisce nel vuoto |
| 🟢 | Banchine | panchine con posti a sedere, cestini, estintori, cartelli binario, colonne rivestite |
| 🟢 | Chioschi distributori | snack + caffè + snack, interni visibili, pubblicità sul retro |
| 🟢 | Depositi | treni fermi in sosta, mai sopra uno scambio |
| 🟢 | Traffico IA | fino a 20 treni, a Lingotto ripartono, niente binari occupati |
| 🟡 | Priorità ai giocatori | vale alla generazione del treno, non ancora ai semafori |
| 🟡 | Pantografi | toccano il filo sulla E464; POP ed E652 da verificare |
| 🟡 | Cancelli di servizio | modellati, ma non si aprono ancora |
| 🔴 | Linea aerea Lingotto → Asti | c'è ancora quella vecchia |

> [!WARNING]
> I tornelli bloccano chi non ha un biglietto: per entrare ai binari dalla galleria bisogna prima comprarne uno.

<details>
<summary>Note tecniche</summary>

- **Ora legale.** Il vecchio calcolo dell'ultima domenica di ottobre cadeva sul 1° novembre (quest'anno è domenica), e alcuni script usavano il fuso del PC del giocatore. Ora tutti usano la stessa funzione su UTC: dall'ultima domenica di marzo all'ultima di ottobre, alle 01:00 UTC.
- **Altoparlante duplicato.** C'erano due `AnnuncioSpeaker_PortaNuova` e `FindFirstChild` prendeva quello ruotato, con i punti audio fuori dalla stazione. Il duplicato è ora in ServerStorage.
- **Pallini dei cartelli.** Il lampeggio comandato dal server non arrivava ai client: ora lo fa `DepartureBoardsController` leggendo l'attributo `Lampeggia` della riga.
- **Linea aerea.** I ganci dei pali sono misurati con raycast sui modelli e il palo viene scelto in base a quanti binari ci sono a sinistra e a destra. Le campate sono generate (filo, fune portante con freccia, pendini) e si toccano negli stessi punti, quindi niente scalini.
- **Lingotto.** `lingottoOccupato` controlla anche dove sono fisicamente testa e coda dei treni, e l'attesa della linea di ritorno è salita da 60 s a 5 minuti.
- **Tornelli.** `TornelliServer`: ingresso con `BigliettoCodice`, uscita libera, e conta solo la posizione dell'HumanoidRootPart (saltando, le gambe attraversavano l'anta). Una barriera invisibile sopra i varchi impedisce di scavalcarli.

</details>

<details>
<summary>English summary</summary>

Two days spent mostly inside Torino Porta Nuova. New LED arrival and departure boards showing only real trains, ticket gates on all four platform groups, benches, bins, extinguishers and platform signs, triple vending kiosks, and parked trains in both depots. Overhead wires now run from Porta Nuova to Lingotto with the real pole models. Fixes: Italian daylight-saving time was off by a day across 72 scripts, a duplicated station speaker made announcements inaudible, and AI trains now leave Lingotto and avoid occupied tracks. Still open: overhead wires towards Asti, player priority at signals, and the service gates don't open yet.

</details>

---

### 6 – 27 ottobre 2026 &nbsp;·&nbsp; Fino ad Asti

Tre settimane per far uscire il gioco da Torino. Dalla linea posata il 5 ottobre si è passati a una linea vera fino ad Asti, con traffico IA, treni componibili, merci, biglietti e un primo playtest chiuso.

| | Cosa | Note |
|---|---|---|
| 🟢 | Linea Lingotto → Asti | stazioni intermedie con banchine, segnali lungo la linea e portali segnali |
| 🟢 | Partenze da Lingotto e da Asti | Lingotto → Porta Nuova sul binario dispari banalizzato |
| 🟢 | Traffico IA (v1) | blocco automatico a 3 aspetti, giallo a 60 km/h, ostacoli sul percorso, 6 treni su 10 proseguono per Asti |
| 🟢 | Composizione personalizzata | fino a 12 veicoli dal catalogo, cabine girate da sole |
| 🟢 | Ripartenza con lo stesso treno | dal binario dove si è arrivati, senza rigenerarlo |
| 🟢 | Merci fino ad Alessandria | uscita dal deposito, carri di lunghezza reale (~26 m), binario d'arrivo prenotato |
| 🟢 | Biglietti e timbratrici | biglietto da comprare e timbrare prima di salire |
| 🟢 | Monete e negozio | saldo in alto a destra, negozio con categorie e schede |
| 🟢 | Paesaggio | rilievi fra Torino e Trofarello/Cambiano, prati e scarpate |
| 🟢 | Treni mai uno dentro l'altro | spawn solo su binari davvero liberi, prenotati subito |
| 🟢 | Giocatore che esce | il suo treno sparisce invece di restare a occupare i blocchi |
| 🟡 | Playtest privato | esperienza separata solo per i tester scelti |

<details>
<summary>Note tecniche</summary>

- **Percorsi verso Asti.** `PercorsiAsti` costruisce il percorso sul grafo dei binari: andata e ritorno, binari d'arrivo scelti a caso tra quelli liberi, fermate solo nelle stazioni del RV quando serve.
- **Binario dispari a Lingotto.** Usato nei due sensi, con un blocco di linea contrario; i ritorni che passano su TLI01 controllano che la sezione sia libera (dopo lo scontro del 22/10 con un treno IA di ritorno).
- **IA.** I treni guidati dal server occupano e liberano i blocchi come un treno vero, rispettano i limiti (anche il rango P del POP) e l'autorizzazione di partenza.
- **Porte.** I pulsanti delle porte compaiono solo se nel convoglio c'è almeno un veicolo passeggeri.

</details>

<details>
<summary>English summary</summary>

Three weeks to get the game out of Turin. The line now runs to Asti with intermediate stations and signals, and trains can start from Lingotto and Asti too. Server-driven AI trains share the line and respect blocks and speed limits. Players can build their own consist (up to 12 vehicles), freight trains run to Alessandria, tickets must be bought and validated, coins can be spent in a new shop, and the landscape gained hills between Turin and Trofarello. A private playtest started.

</details>

---

### 5 ottobre 2026 &nbsp;·&nbsp; I binari escono da Torino

Questa settimana la ferrovia ha smesso di essere solo Porta Nuova. Ho preso i dati veri delle mappe ferroviarie e li ho posati in gioco: prima il tratto fino a Lingotto, con lo scalo merci e il deposito, poi tutta la linea fino a Genova Brignole. Lingotto l'ho rifatta da capo, perché la mia era dritta e quella vera è in curva.

| | |
|:--|:--|
| 🟢 | Tratto corso Bramante - via Vigliani dai dati reali, con scalo, deposito e Linea Passante |
| 🟢 | Lingotto in curva, nella posizione vera |
| 🟢 | Compositore: il treno si monta veicolo per veicolo, con l'anteprima |
| 🟢 | Le porte non si richiudono più da sole quando scendi |
| 🟢 | Mappa per scegliere la stazione di partenza |
| 🟡 | Linea per Genova posata ma senza percorsi e segnali |
| 🟡 | Marciapiedi di Lingotto da rifare sui binari nuovi |
| 🔴 | A via Vigliani c'è un gradino di 14 studs fra il tratto vecchio e quello nuovo |

> [!WARNING]
> La linea per Genova si vede ma non si guida ancora fino in fondo.

<details>
<summary>Il resto della sessione</summary>

<br>

Torcia sul tasto L, free cam in cabina con il tasto destro e zoom con la rotellina, schermata di caricamento, impostazioni e crediti nuovi, bordo giallo sul pulsante delle porte dal lato della banchina. Le locomotive con una cabina sola, come la E464, si girano da sole nel verso giusto. Il POP ha due appoggi per cassa e tutti i rotabili hanno i carrelli nuovi.

</details>

<details>
<summary>Note tecniche</summary>

<br>

La scala viene dalla distanza reale fra Porta Nuova e il ponte di corso Bramante: 2.284 metri contro 6.876 studs, cioè 3,011 studs per metro. Torna anche con i 12 studs fra due binari paralleli, che diventano 3,9 metri.

Il primo tentativo di allineare i dati è uscito storto di 60 gradi: in OpenStreetMap i due binari della Torino Genova sono disegnati in versi opposti, e sommandoli la direzione si annullava.

Le porte si chiudevano da sole per un motivo fisico. Ogni anta è saldata alla cassa e la saldatura ricordava la posizione chiusa: quando il treno veniva rilasciato, la fisica la riportava indietro. Ora la saldatura si aggiorna alla fine di ogni apertura.

La linea per Genova arrivava spezzata in 24 pezzi, perché in OpenStreetMap i binari in galleria hanno il nome della galleria e non della linea. L'ho presa dalla relazione ufficiale della linea, che comprende tutti i pezzi.

</details>

<details>
<summary>🇬🇧 English</summary>

<br>

This week the railway stopped being just Porta Nuova. I took real railway map data and laid it in game: first the section to Lingotto, with the freight yard and depot, then the whole line to Genova Brignole. I rebuilt Lingotto from scratch, because mine was straight and the real one is curved. Also new: train composer, station map, loading screen, flashlight, cab free cam. Still open: no routes or signals on the Genova line yet, and a 14 stud step at via Vigliani.

</details>

---

### 4 ottobre 2026 &nbsp;·&nbsp; Porta Nuova in ordine

Ho diviso il ventaglio di Porta Nuova in binari, gola, deposito e uscite, e da lì il gioco ha generato da solo 59 percorsi, uno per ogni binario e destinazione. Niente più rotte scritte a mano.

| | |
|:--|:--|
| 🟢 | 59 percorsi generati dai binari veri |
| 🟢 | Il controllore in Sala Comandi ha la precedenza sul macchinista |
| 🟢 | Pannello di cabina nuovo, con arco della velocità e semaforo |
| 🟢 | E652 riservata al Macchinista Merci |
| 🟡 | Il binario 3 non arriva ancora verso Porta Susa |
| 🟡 | Il deposito di Porta Nuova si raggiunge solo in manovra |

<details>
<summary>🇬🇧 English</summary>

<br>

I split the Porta Nuova track fan into tracks, throat, depot and exits, and from there the game generated 59 routes on its own. Also: dispatcher priority in the Control Room, new cab panel, E652 for the Freight Driver only.

</details>

---

### 30 settembre 2026 &nbsp;·&nbsp; Si gioca in più di uno

Il treno ora lo vedono muoversi tutti, non solo chi guida, e le carrozze seguono le curve. I percorsi vengono ricavati dal tracciato vero, e il quadro della Sala Comandi mostra Porta Nuova e Lingotto. Rifatto anche l'HUD di guida, con un tachimetro analogico.

<details>
<summary>🇬🇧 English</summary>

<br>

Everyone now sees the train move, not just the driver. Routes come from the real track layout, the Control Room panel shows Porta Nuova and Lingotto, and the driving HUD has an analog speedometer.

</details>

---

### 23 settembre 2026 &nbsp;·&nbsp; Nasce la Sala Comandi

Primo quadro sinottico, generato dai dati dei binari. Il controllore sceglie il binario di partenza e quello di arrivo e conferma l'itinerario. Tutti i deviatoi del ventaglio di Porta Nuova sono mappati uno per uno.

<details>
<summary>🇬🇧 English</summary>

<br>

First schematic panel, generated from the track data. The dispatcher picks departure and arrival track and confirms the route. Every Porta Nuova switch is mapped.

</details>

---

### 21 agosto 2026 &nbsp;·&nbsp; Le casse girano sui carrelli

Il treno non segue più un punto solo: ogni veicolo ha due carrelli che seguono il binario per conto loro, e la cassa sta in mezzo. In curva finalmente si vede. Ho rifatto anche i venti percorsi del ventaglio, al terzo tentativo, e ora sono tutti dritti.

| | |
|:--|:--|
| 🟢 | Movimento per carrelli: la cassa si costruisce dai suoi due bogie |
| 🟢 | Venti percorsi ricostruiti dai binari, tortuosità fra 1,00 e 1,03 |
| 🟢 | Il binario scelto nel menu decide davvero il percorso |
| 🟢 | Treno intero e fermo allo spawn |
| 🟢 | Binari con mesh texturizzata su 7.609 oggetti |
| 🟡 | Il treno si muove solo sullo schermo di chi guida |
| 🟡 | Il suono statico si interrompe, c'è un rimedio ma non la causa |
| 🔴 | Due errori di sintassi hanno bloccato interi script per un po' |

<details>
<summary>Note tecniche</summary>

<br>

I percorsi: raggruppare per nome tagliava binari veri, concatenare per vicinanza prendeva il binario sbagliato agli incroci. Ha funzionato un limite secco di 60 gradi fra tile consecutive: un binario non gira mai così di colpo.

Il treno che si smontava allo spawn aveva tre cause: lo spawn prendeva come riferimento un pezzo di porta, alcune locomotive hanno il PrimaryPart ruotato, e lo script Advanced Weld 2 disancorava tutto.

Velocimetro e barra di potenza restavano a zero perché leggevano la fisica, che per un treno spostato con PivotTo è immobile. Ora lo script di guida pubblica velocità e potenza come attributi.

</details>

<details>
<summary>🇬🇧 English</summary>

<br>

The train no longer follows a single point: each vehicle has two bogies following the track on their own, with the body in between. All twenty fan routes rebuilt and straight, the menu track choice now really sets the route, and the train spawns whole. Still open: the train only moves on the driver's screen.

</details>

---

### 27 luglio 2026 &nbsp;·&nbsp; Suoni veri e primi carrelli

Il treno ha cominciato a suonare come uno vero: tromba, pantografo, freni e porte, tutti collegati ai sistemi che c'erano già. E ho fatto il primo esperimento di carrelli che seguono il binario da soli.

| | |
|:--|:--|
| 🟢 | Suoni reali di tromba, pantografo, freni e porte |
| 🟢 | Un solo pulsante freno, con barra di caricamento |
| 🟢 | Barra di imbarco riusata anche per la chiusura delle porte |
| 🟢 | Trovate tre cause per cui il treno non si muoveva |
| 🟢 | Primo test di carrelli indipendenti, con marcatori visibili |
| 🟢 | Community Roblox creata e collegata al progetto |
| 🟡 | I carrelli usano ancora marcatori di prova |
| 🟡 | Curve non ancora provate |

<details>
<summary>🇬🇧 English</summary>

<br>

Real sounds for horn, pantograph, brakes and doors, a single brake button with a loading bar, three causes found for the train not moving, a first test of independent bogies, and the official Roblox Community.

</details>

---

### 26 luglio 2026 &nbsp;·&nbsp; La rotta vera del binario 1

La sera prima del 27: sei suoni collegati, il pulsante freni rifatto, e la scoperta del perché il treno restava fermo. La cartella del percorso non era una lista di punti ma 101 sottocartelle. Da lì ho ricostruito una rotta vera dai 47 punti del binario 1.

| | |
|:--|:--|
| 🟢 | Rotta vera ricostruita dai 47 punti di Start Track 1 |
| 🟢 | Animazione porte con la durata vera dal server |
| 🟡 | Movimento a waypoint spento per il test dei carrelli |
| 🔴 | Navigare il menu da script per i test automatici: abbandonato |

<details>
<summary>🇬🇧 English</summary>

<br>

Six sounds wired in, brake button redesigned, and the real reason the train stood still: the route folder was 101 subfolders, not a list of points. A real route was rebuilt from the 47 points of track 1.

</details>

---

### 14 luglio 2026 &nbsp;·&nbsp; Tre linee che si toccano

Le tre linee del lancio sono decise e si incontrano a Genova: Torino Genova, Torino Milano e Genova Ventimiglia. È arrivata anche la scelta del ruolo, passeggeri o merci, con due tratte merci vere.

| | |
|:--|:--|
| 🟢 | Corridoi reali per Torino Milano e Genova Ventimiglia |
| 🟢 | Schermata di scelta del ruolo |
| 🟢 | Merci separato dai passeggeri, con scali veri |
| 🟢 | Trovato un calo di prestazioni: una funzione mai definita chiamata a ogni frame |
| 🟡 | 26 cartelli orari senza template |
| 🟡 | 5 file audio con permessi negati |

<details>
<summary>🇬🇧 English</summary>

<br>

The three launch lines are set and meet at Genova. Real corridors extracted for Torino Milano and Genova Ventimiglia, role selection screen, freight separated from passengers with real yards, and a performance drop traced to an undefined function called every frame.

</details>

---

### 13 luglio 2026 &nbsp;·&nbsp; Addio fisica delle ruote

Dopo un'intera sessione a far girare le ruote senza riuscirci, ho cambiato strada: il treno ora segue una sequenza di punti, senza fisica. Funziona al primo tentativo, dopo aver ancorato il treno perché le vecchie cerniere non lo facessero esplodere.

| | |
|:--|:--|
| 🟢 | Movimento a waypoint riscritto da zero |
| 🟢 | Ordine reale delle 10 fermate confermato |
| 🟡 | Dati del ventaglio importati ma non allineati |
| 🔴 | Divisione automatica del ventaglio in binari singoli |
| 🔴 | Tre tentativi di scalare i dati, abbandonati |

<details>
<summary>🇬🇧 English</summary>

<br>

After a whole session trying to make the wheels spin, I switched approach: the train now follows a sequence of points with no physics. It worked on the first try, once the train was anchored so the old hinges stopped blowing it up.

</details>

---

### 12 luglio 2026 &nbsp;·&nbsp; Il pantografo

Il treno non si muoveva e il motivo era l'ultima cosa che avrei controllato: con il pantografo abbassato, uno script azzerava la velocità a ogni frame. Nel frattempo sono arrivati i limiti di velocità con il cartello vero e il pannello di guida unificato.

| | |
|:--|:--|
| 🟢 | Limiti di velocità a zone, con cartello italiano |
| 🟢 | Pannello di guida unico |
| 🟢 | Prima persona sulla testa del personaggio e campo visivo regolabile |
| 🟢 | Tasto C per la camera, H per il clacson |
| 🟢 | Corridoio Torino Genova da OpenStreetMap |
| 🟡 | Trovato il blocco del motore, ma il treno resta fermo |
| 🔴 | Personaggio caricato solo dopo la scelta: rompeva tutta l'interfaccia, annullato |

<details>
<summary>🇬🇧 English</summary>

<br>

The train wouldn't move, and the cause was the last thing I'd have checked: with the pantograph down, a script zeroed the speed every frame. Also new: speed limits with a real sign, unified driving panel, first person camera, C and H keys, Torino Genova corridor from OpenStreetMap.

</details>

---

### 11 luglio 2026 &nbsp;·&nbsp; Gli annunci di stazione

93 registrazioni vere, montate in sequenza: numero del treno, categoria, destinazione, orario e binario. Ogni stazione ha il suo altoparlante con il riverbero.

| | |
|:--|:--|
| 🟢 | Annunci vocali completi, 93 clip |
| 🟢 | Numeri oltre 59 letti cifra per cifra |
| 🟢 | Riverbero e pause fra le parole |
| 🟢 | Pannello annunci unito a quello admin |
| 🟢 | Testo scorrevole dei cartelli corretto |
| 🟢 | Menu tratte a tre colonne |
| 🟡 | Ventaglio di Porta Nuova solo come guida |

<details>
<summary>🇬🇧 English</summary>

<br>

93 real recordings played in sequence: train number, category, destination, time and platform, through a speaker per station with its own reverb. Also fixed the scrolling text on the boards and rebuilt the route menu in three columns.

</details>

---

### 10 luglio 2026 &nbsp;·&nbsp; Cartelli e icone

I tabelloni hanno le icone vere delle categorie e il logo, il pannello admin cambia il testo di tutti i cartelli insieme, e il display del prossimo segnale smette di mostrare quello appena superato.

| | |
|:--|:--|
| 🟢 | Icone R, RV, IC, ICN, Frecciarossa, Italo e logo |
| 🟢 | Icone sui pulsanti di cabina |
| 🟢 | Pannello admin per il testo dei cartelli |
| 🟢 | Prossimo segnale cercato davvero in avanti |
| 🟡 | Menu principale sistemato dopo tre cause diverse |
| 🔴 | Errore ripetuto nell'HUD di cabina |
| 🔴 | Cartella Test da 251 oggetti mai verificata |

<details>
<summary>🇬🇧 English</summary>

<br>

Real category icons and logo on the boards, an admin panel that changes every board's text at once, and a next signal display that no longer shows the one just passed.

</details>

---

### 9 luglio 2026 &nbsp;·&nbsp; I cartelli passano al server

Metà dei bug della giornata avevano la stessa causa: gli attributi scritti dal client non arrivano al server. I cartelli partenze ora li gestisce tutti il server.

| | |
|:--|:--|
| 🟢 | Trovato il problema degli attributi fra client e server |
| 🟢 | Cartelli orari gestiti interamente dal server |
| 🟢 | Indicatore lampeggiante corretto |
| 🔴 | Partenza e binario ancora scritti a mano |

<details>
<summary>🇬🇧 English</summary>

<br>

Half the day's bugs had one cause: attributes written by the client never reach the server. Departure boards are now fully managed by the server.

</details>

---

### 4 luglio 2026 &nbsp;·&nbsp; I primi segnali

Quattro segnali in fila che calcolano rosso, giallo e verde dall'occupazione vera dei blocchi. Verificati su un ciclo completo, dalla partenza all'arrivo.

| | |
|:--|:--|
| 🟢 | Blocco automatico con 4 segnali |
| 🟢 | Orario italiano corretto su ogni server |
| 🟢 | Ordine dei segnali di nuovo giusto |
| 🟢 | Selettore del binario con 20 pulsanti |
| 🟡 | I cartelli di Lingotto non hanno ancora il template |

<details>
<summary>🇬🇧 English</summary>

<br>

Four signals in a row computing red, yellow and green from real block occupancy, verified over a full departure to arrival cycle. Also: Italian time correct on every server, 20 button track selector.

</details>
