Teil 2 dieser Anleitung setzt voraus, dass du Ghidra erfolgreich wie in Teil 1A (für Windows-Nutzer) oder Teil 1B (für Linux-Nutzer) beschrieben eingerichtet hast.

Teil 2 behandelt die Grundlagen zum Erhalt der benötigten Switch-Binärdateien. Du brauchst dafür Hactoolnet (https://github.com/Thealexbarney/LibHac/releases), hactool (https://github.com/SciresM/hactool) zum Dekomprimieren der Binärdateien. Die Binärdateien für hactool können aus den Artifacts bezogen (GitHub-Login erforderlich) oder selbst kompiliert werden. Richte eine Umgebungsvariable für hactool & hactoolnet ein oder platziere sie unter /usr/local/bin/hactool und /usr/local/bin/hactoolnet, falls du Linux verwendest.

1. Um den aktuellen Schlüsselsatz zum Entschlüsseln der Nintendo Switch Firmware-Dateien zu erhalten, benötigst du den Schlüssel "tsec_root_key_02". Wie du diesen heutzutage erhältst, musst du selbst herausfinden.

2. Speichere diesen Schlüssel in einer Textdatei namens keys.txt mit einer einzigen Zeile, wobei die f's durch den tatsächlichen Schlüssel ersetzt werden, zum Beispiel "tsec_root_key_02 = fffffffffffffffffffffffffffffff". Öffne dann ein Terminal und führe "hactoolnet -k keys.txt -t keygen >> prod.keys" aus (alternativ kannst du [aes_sample.py](../scripts/aes_sample.py) verwenden, Nutzungsanweisungen findest du in der README.md).

3. Kopiere die erzeugte prod.keys nach ~/.switch/prod.keys (das entspricht /home/deinbenutzername/.switch/prod.keys unter Linux und C:/users/deinbenutzername/.switch/prod.keys unter Windows).

4. Sichere deine eigenen Systemversionsdateien oder beziehe sie von https://darthsternie.net/switch-firmwares/. Dieses Beispiel verwendet Version 14.1.1.

5. Für dieses spezielle Beispiel verwenden wir die TitleID für NIFM: 010000000000000F. Unter https://switchbrew.org/wiki/Title_list findest du Informationen zum Umgang mit anderen Modulen.

6. Platziere die Firmware-Dateien in einem Ordner namens "firmware" und führe dann aus: "hactoolnet -t switchfs firmware --title 010000000000000f --exefsdir exefs"

7. Führe den Befehl "hactool -t nso0 exefs/main --uncompressed=uncompressed_nifm.nso0" aus und notiere dir die Build-ID.

8. Öffne Ghidra und erstelle ein neues Projekt an deinem gewünschten Speicherort.
   - Klicke auf Datei -> Datei importieren -> Wähle die gerade extrahierte uncompressed_nifm.nso0 (stelle sicher, dass als Format Nintendo Switch Binary angezeigt wird)
   - Klicke auf den Drachen, um den Ghidra CodeBrowser zu öffnen
   - Klicke auf Datei -> öffne uncompressed_nifm.nso0 (die du zum Projekt hinzugefügt hast)
   - Bestätige die Analyse und aktiviere die switch-ipc Option, dann klicke auf Analysieren. Warte, bis der Prozess abgeschlossen ist. Bei eventuellen Fehlermeldungen einfach "Ok" klicken

![alt text](https://github.com/borntohonk/Switch-Ghidra-Guides/blob/master/img/ghidra-nso.png?raw=true)

9. In diesem speziellen Beispiel soll eine Funktion, die normalerweise nach X-Organization: Nintendo sucht, umgekehrt werden. Wenn sie dies nicht als wahr erkennt, wird dein WLAN/LAN-Adapter deaktiviert. Wir werden das Gegenteil bewirken.
   - Um den Offset dieser Funktion zu finden, drücke S für den Speichersuchmodus und suche nach dieser HEX-Zeichenfolge: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. f0 03 00 aa .. .. .. .. f3 03 14 aa e0 03 14 aa 9f 02 01 39 7f 8e 04 f8". Der Startoffset des Ergebnisses ist der für den Patch benötigte Offset.

![alt text](https://github.com/borntohonk/Switch-Ghidra-Guides/blob/master/img/ghidra-nifm-offset.png?raw=true)

10. The patch we want to make is to change out the instruction at that offset, with 'MOV X0, #0xD180 + MOVK X0, #0x8F0, LSL #16 + SVC #0XB + MOV X0, XZR + RET' (00 30 9A D2 00 1E A1 F2 61 01 00 D4 E0 03 1F AA C0 03 5F D6) - This will make the function at offset 04 42 0C to end instead of doing the function it previously did, essentially cutting it short. *updated string to include patch with a sleep added as apparently the previous pattern would cause issues to some users. (These are ARM instructions)




**note 1:** the offsets ghidra-loader gives you are -0x100, so the resulting offset we use in the next part is +0x100 (04 43 0C, up from 04 42 0C)
**note 2:** the example values below are for 14.1.1, and may be inconsistent with the example images from above.
**note 3:** this kind of patch generation (".ips") is deprecated for system applications that are marked as "execute-only" as of 19.0.0 (potentially including the one provided example for; "NIFM")

11. "50 41 54 43 48" is "PATCH", "04 43 0C" is the offset we're patching, "00 14" is the length of patch we're applying, "00 30 9A D2 00 1E A1 F2 61 01 00 D4 E0 03 1F AA C0 03 5F D6" Is the patch we are applying at that offset ('MOV X0, #0xD180 + MOVK X0, #0x8F0, LSL #16 + SVC #0XB + MOV X0, XZR + RET'), and 45 4F 46 is EOF. This effectively patches out the "connectivity test" and lets you use network functionality on closed networks where otherwise X-Organization: Nintendo would never be returned to the console. (You can look at the table below to get a more visual concept of how this patch is structured)

| PATCH magic | Offset | Size of patch | Patch to be applied | EOF magic |
| :---: | :---: | :---: | :---: | :---: |
| 50 41 54 43 48 | 04 43 0C | 00 14 | 00 30 9A D2 00 1E A1 F2 61 01 00 D4 E0 03 1F AA C0 03 5F D6 | 45 4F 46 |