Teil 2 dieser Anleitung setzt voraus, dass du Ghidra erfolgreich wie in Teil 1A (für Windows-Nutzer) oder Teil 1B (für Linux-Nutzer) beschrieben eingerichtet hast.

Teil 2 behandelt die Grundlagen zum Erhalt der benötigten Switch-Binärdateien. Du brauchst dafür Hactoolnet (https://github.com/Thealexbarney/LibHac/releases), hactool (https://github.com/SciresM/hactool) zum Dekomprimieren der Binärdateien. Die Binärdateien für hactool können aus den Artifacts bezogen (GitHub-Login erforderlich) oder selbst kompiliert werden. Richte eine Umgebungsvariable für hactool & hactoolnet ein oder platziere sie unter /usr/local/bin/hactool und /usr/local/bin/hactoolnet, falls du Linux verwendest.

1. Um den aktuellen Schlüsselsatz zum Entschlüsseln der Nintendo Switch Firmware-Dateien zu erhalten, benötigst du den Schlüssel "tsec_root_key_02". Die Beschaffung dieses Schlüssels musst du selbst recherchieren.

2. Speichere diesen Schlüssel in einer Textdatei namens keys.txt mit einer einzigen Zeile, wobei die f's durch den tatsächlichen Schlüssel ersetzt werden, zum Beispiel "tsec_root_key_02 = fffffffffffffffffffffffffffffff". Öffne dann ein Terminal und führe ```bash:terminal
hactoolnet -k keys.txt -t keygen >> prod.keys``` aus (alternativ kannst du [aes_sample.py](../scripts/aes_sample.py) verwenden, Nutzungsanweisungen findest du in der README.md).

3. Kopiere die erzeugte prod.keys nach ~/.switch/prod.keys (das entspricht /home/deinbenutzername/.switch/prod.keys unter Linux und C:/users/deinbenutzername/.switch/prod.keys unter Windows).

4. Sichere deine eigenen Systemversionsdateien oder beziehe sie von https://darthsternie.net/switch-firmwares/. Dieses Beispiel verwendet Version 14.1.1.

5. Für dieses spezielle Beispiel verwenden wir die TitleID für NIFM: 010000000000000F. Unter https://switchbrew.org/wiki/Title_list findest du Informationen zum Umgang mit anderen Modulen.

6. Platziere die Firmware-Dateien in einem Ordner namens "firmware" und führe dann aus: ```bash:terminal
hactoolnet -t switchfs firmware --title 010000000000000f --exefsdir exefs```

7. Führe den Befehl ```bash:terminal
hactool -t nso0 exefs/main --uncompressed=uncompressed_nifm.nso0``` aus und notiere dir die Build-ID.

8. Öffne Ghidra und erstelle ein neues Projekt an deinem gewünschten Speicherort.
   - Klicke auf Datei -> Datei importieren -> Wähle die gerade extrahierte uncompressed_nifm.nso0 (stelle sicher, dass als Format Nintendo Switch Binary angezeigt wird)
   - Klicke auf den Drachen, um den Ghidra CodeBrowser zu öffnen
   - Klicke auf Datei -> öffne uncompressed_nifm.nso0 (die du zum Projekt hinzugefügt hast)
   - Bestätige die Analyse und aktiviere die switch-ipc Option, dann klicke auf Analysieren. Warte, bis der Prozess abgeschlossen ist. Bei eventuellen Fehlermeldungen einfach "Ok" klicken

![alt text](https://github.com/borntohonk/Switch-Ghidra-Guides/blob/master/img/ghidra-nso.png?raw=true)

9. In diesem speziellen Beispiel soll eine Funktion, die normalerweise nach X-Organization: Nintendo sucht, umgekehrt werden. Wenn sie dies nicht als wahr erkennt, wird dein WLAN/LAN-Adapter deaktiviert. Wir werden das Gegenteil bewirken.
   - Um den Offset dieser Funktion zu finden, drücke S für den Speichersuchmodus und suche nach dieser HEX-Zeichenfolge: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. f0 03 00 aa .. .. .. .. f3 03 14 aa e0 03 14 aa 9f 02 01 39 7f 8e 04 f8". Der Startoffset des Ergebnisses ist der für den Patch benötigte Offset.

![alt text](https://github.com/borntohonk/Switch-Ghidra-Guides/blob/master/img/ghidra-nifm-offset.png?raw=true)

10. Der Patch, den wir erstellen wollen, ersetzt die Anweisung an diesem Offset durch 'MOV X0, #0xD180 + MOVK X0, #0x8F0, LSL #16 + SVC #0XB + MOV X0, XZR + RET' (00 30 9A D2 00 1E A1 F2 61 01 00 D4 E0 03 1F AA C0 03 5F D6) - Dies bewirkt, dass die Funktion am Offset 04 42 0C endet, anstatt ihre ursprüngliche Funktion auszuführen. *Aktualisierte Zeichenfolge enthält einen Patch mit hinzugefügtem Sleep, da das vorherige Muster bei einigen Nutzern zu Problemen führte. (Dies sind ARM-Befehle)

**Hinweis 1:** Die Offsets von ghidra-loader sind um -0x100 verschoben, daher ist der resultierende Offset, den wir im nächsten Teil verwenden, +0x100 (04 43 0C, statt 04 42 0C)
**Hinweis 2:** Die Beispielwerte unten gelten für Version 14.1.1 und können von den Beispielbildern oben abweichen.
**Hinweis 3:** Diese Art der Patch-Generierung (".ips") ist für Systemanwendungen, die als "execute-only" markiert sind, ab Version 19.0.0 veraltet (möglicherweise einschließlich des hier gezeigten Beispiels "NIFM")

11. "50 41 54 43 48" steht für "PATCH", "04 43 0C" ist der Offset, den wir patchen, "00 14" ist die Länge des anzuwendenden Patches, "00 30 9A D2 00 1E A1 F2 61 01 00 D4 E0 03 1F AA C0 03 5F D6" ist der Patch, den wir an diesem Offset anwenden ('MOV X0, #0xD180 + MOVK X0, #0x8F0, LSL #16 + SVC #0XB + MOV X0, XZR + RET'), und 45 4F 46 steht für EOF. Dies umgeht effektiv den "Konnektivitätstest" und ermöglicht die Nutzung von Netzwerkfunktionen in geschlossenen Netzwerken, wo normalerweise X-Organization: Nintendo nie an die Konsole zurückgegeben würde. (Die untenstehende Tabelle gibt dir einen besseren visuellen Überblick über die Struktur des Patches)

| PATCH-Magic | Offset | Patch-Größe | Anzuwendender Patch | EOF-Magic |
| :---: | :---: | :---: | :---: | :---: |
| 50 41 54 43 48 | 04 43 0C | 00 14 | 00 30 9A D2 00 1E A1 F2 61 01 00 D4 E0 03 1F AA C0 03 5F D6 | 45 4F 46 |