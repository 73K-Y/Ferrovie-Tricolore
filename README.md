<div align="center">

<img src="docs/ferrovie-tricolore.png" width="100%" alt="Ferrovie Tricolore">

<img src="https://readme-typing-svg.demolab.com?font=Inconsolata&weight=700&size=20&duration=2600&pause=1400&color=FFCD28&background=0C0C0EFF&center=true&vCenter=true&width=640&height=46&lines=R+4001++TORINO+P.NUOVA++GENOVA+BRIGNOLE++BIN.+1;IC+652++TORINO+P.NUOVA++MILANO+CENTRALE++BIN.+7;REG+1820++GENOVA+P.PRINCIPE++VENTIMIGLIA++BIN.+3" alt="Tabellone partenze">

[Changelog](CHANGELOG.md) &nbsp;·&nbsp; [Game design](GAME_DESIGN.md) &nbsp;·&nbsp; [Discord](https://discord.gg/pH62fm3nkG)

</div>

<br>

Sto costruendo un simulatore ferroviario su Roblox partendo da una regola sola: i binari devono essere quelli veri. Le stazioni sono ricostruite dalle mappe ferroviarie, i segnali funzionano a blocchi come sulla linea vera, e in Sala Comandi un altro giocatore può fare il dirigente movimento mentre tu guidi.

È iniziato da Torino Porta Nuova e da lì si sta allungando verso Genova.

> [!NOTE]
> Il gioco è in sviluppo e non ancora pubblico. Gli aggiornamenti escono prima sul [Discord](https://discord.gg/pH62fm3nkG).

## Partenze

| Treno | Destinazione | Binario | Stato |
|:--|:--|:--:|:--|
| `R` | **Genova Brignole** via Asti, Alessandria | 1 | 🟡 binari posati, guidabile fino a Lingotto |
| `RV` | **Ventimiglia** via Savona | 3 | ⚪ in programma |
| `IC` | **Milano Centrale** via Novara | 7 | ⚪ in programma |

<p align="center">
<code>🟢 Torino P.Nuova ─── 🟢 Lingotto ─── 🟡 Trofarello ─── 🟡 Asti ─── 🟡 Alessandria ─── 🟡 Novi Ligure ─── 🟡 Genova P.Principe ─── 🟡 Genova Brignole</code><br>
<sub>🟢 si guida &nbsp; 🟡 binari posati, percorsi e segnali in arrivo</sub>
</p>

## In cabina

<!-- Metti qui 2 o 3 screenshot o una GIF: cabina, Sala Comandi, mappa delle stazioni.
<p align="center">
  <img src="docs/screenshots/cabina.png" width="32%">
  <img src="docs/screenshots/sala-comandi.png" width="32%">
  <img src="docs/screenshots/mappa.png" width="32%">
</p>
-->

Componi il treno veicolo per veicolo, alzi il pantografo, carichi i freni e aspetti il verde. In banchina apri le porte dal lato giusto e lasci salire i passeggeri. Se in Sala Comandi c'è qualcuno, la partenza la decide lui.

## Parco mezzi

| Rotabile | Stato | Livree |
|:--|:--|:--|
| Mazinga | in gioco | XMPR, poi Regionale |
| MDVC | in gioco | XMPR in lavorazione |
| MDCE | in lavorazione | XMPR in lavorazione |
| E464 | in gioco | |
| POP | in gioco | |
| E652 | in gioco, treni merci | |
| Rock, Italo, Taurus, E405, TAF, Frecciargento | in lavorazione | |

Ogni rotabile avrà anche le sue varianti di livrea, così lo stesso mezzo potrà girare in più versioni, come la Mazinga in livrea XMPR o Regionale.

## Come è fatto

<details>
<summary>Per chi è curioso del lato tecnico</summary>

<br>

- Il treno non usa la fisica delle ruote: segue i punti del tracciato, e ogni cassa è costruita dai suoi due carrelli, così in curva si comporta come quella vera.
- I binari sono tile da 20 studs posati sui dati di OpenStreetMap, alla scala di 3,011 studs per metro, ricavata dalla distanza reale fra Porta Nuova e il ponte di corso Bramante.
- I percorsi dei treni vengono generati dai binari stessi, uno per ogni coppia di binario e destinazione.
- Il segnalamento è a blocchi con due sezioni di preavviso, e in stazione la partenza va autorizzata.

</details>

## Stato dei lavori

- [x] Torino Porta Nuova con 20 binari, gola e deposito
- [x] Sala Comandi e segnali di partenza
- [x] Collegamento reale Porta Nuova e Lingotto
- [ ] Linea per Genova guidabile fino in fondo
- [ ] Marciapiedi della nuova Lingotto
- [ ] Varianti di livrea dei rotabili
- [ ] Carri merci
- [ ] Genova Ventimiglia e Torino Milano

<details>
<summary>🇬🇧 English</summary>

<br>

I'm building a railway simulator on Roblox around one rule: the tracks have to be the real ones. Stations are rebuilt from railway map data, signals work in blocks like on the real line, and in the Control Room another player can dispatch traffic while you drive.

It started at Torino Porta Nuova and is now stretching towards Genova. The game is in development and not public yet; updates go out first on Discord.

| Train | Destination | Status |
|:--|:--|:--|
| `R` | Genova Brignole | tracks laid, drivable up to Lingotto |
| `RV` | Ventimiglia | planned |
| `IC` | Milano Centrale | planned |

Every vehicle will also get its livery variants, so the same train can run in more than one version, like the Mazinga in XMPR or Regionale livery.

</details>
