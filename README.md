Dieses Repository enthält Reverse-Engineering-Notizen und Anleitungen zu Bildungszwecken, die Open-Source-Tools wie Ghidra verwenden, um Binärdateien für die Nintendo Switch zu analysieren. Es enthält auch grundlegende Methoden zur Verwendung von Ghidra für die Untersuchung von "ARM"-Binärdateien, die auf der Nintendo Switch laufen.

Dieses Repository hostet keine Anleitungen zur Umgehung von Sicherheitsmaßnahmen, die digitale Inhalte schützen, und enthält auch keine entsprechenden Guides.

Das gesamte Material dient ausschließlich als Forschungsreferenz.

* Ghidra/Patch-Erstellung Tutorial:
  - Teil 1A erklärt die Einrichtung von Ghidra und dem Switch-Loader für Windows [(link)](guides/Part1A-WindowsSetup.MD)
  - Teil 1B erklärt die Einrichtung von Ghidra und dem Switch-Loader für Linux [(link)](guides/Part1B-LinuxSetup.MD)
  - Teil 2 erklärt die Einrichtung von Hactoolnet zur Ausgabe von Dateien für die weitere Verarbeitung und eine grundlegende Einführung in Ghidra mit der Erstellung von Patches für nifm als Beispiel. [(link)](guides/Part2.MD)
  - Die resultierenden "Patches" aus dieser Anleitung findest du unter https://github.com/misson20000/exefs_patches/tree/master/atmosphere/exefs_patches/nfim_ctest

**Hinweis: Der erwähnte "Loader" bezieht sich auf die Re-Implementierung des "Atmosphere"-Projekts: https://github.com/Atmosphere-NX/Atmosphere/tree/master/stratosphere/loader**

* Hier ist eine Liste von Skripten, die dem Beispiel aus Teil 2 der obigen Anleitung folgen:

  - Python-Skript zur Ableitung des gesamten Keysets. [aes_sample.py](scripts/aes_sample.py)
    * Dieses Skript macht "Lockpick" jeglicher Art überflüssig, solange der Benutzer Firmware-Dateien bereitstellt.
    * Die beschriebene Kryptografie-Logik kann mit diesem Python-Skript getestet werden, Ausgabe-Keydatei (Standard "prod.keys", kann mit -k geändert werden): [aes_sample.py](scripts/aes_sample.py)
    * Es gibt auch eine Entwickler-Variante, die auf die gleiche Weise funktioniert, [aes_sample_dev.py](scripts/aes_sample_dev.py)

  - Python-Skript zum Abrufen der neuesten mariko_master_kek_source_%% aus bereitgestellten Firmware-Dateien und zur Bereitstellung von Strings zum Aktualisieren der Arrays für key_sources.py, benötigt lz4 von pip
    * Beispielverwendung: "python scripts/mariko_master_kek_source.py --firmware firmware" [mariko_master_kek_source.py](scripts/mariko_master_kek_source.py)

  - Python-Skript zur Generierung von Patches für Atmospheres Open-Source-Loader-Reimplementierung, benötigt lz4 von pip
    * Verwendung: Führe "python scripts/atmosphere_loader_patch.py" aus, es wird automatisch heruntergeladen, der Patch für den Loader erstellt und anschließend aufgeräumt. [atmosphere_loader_patch.py](scripts/atmosphere_loader_patch.py)

  - Python-Skript zur Batch-Erstellung von Patches für bereitgestellte Firmware-Dateien.
    * Verwendung: Lege Firmware-Dateien in einem Ordner namens "firmware" ab oder gib einen Speicherort mit -l oder --location an, stelle Keys mit -k oder --keys bereit, ansonsten wird standardmäßig ~/.switch/prod.keys verwendet
    * Beispielverwendung: "python scripts/make_patches.py --location temp_folder --keys prod.keys"
    * Wenn der Endbenutzer über mariko_bek und mariko_kek verfügt (erhältlich mit der release.nfo für die Scene-Release von "Marvel's Spider-Man: Miles Morales" von BigBlueBox), wird auch die Keygenerierung versucht.
    * [make_patches.py](scripts/make_patches.py)

  - Python-Skript zur Generierung des "[disable_ca_verification patch](https://github.com/misson20000/exefs_patches#disable-ca-verification)", [(link)](scripts/disable_ca_verification_patch.py)

  - Python-Skript zur Generierung des "[disable_browser_ca_verification patch](https://github.com/misson20000/exefs_patches#disable-browser-ca-verification)", [(link)](scripts/disable_browser_ca_verification_patch.py)

  - Python-Skript zur Generierung des "[nifm_ctest patch](https://github.com/misson20000/exefs_patches#nifm-ctest)", [(link)](scripts/nifm_ctest_patch.py)

* Danksagungen: 
* [@sciresm](https://github.com/SciresM) - hactool - [(scripts/aes128.py)](scripts/aes128.py)
* [@reswitched](https://github.com/reswitched) - [(scripts/nxo64.py)](scripts/nxo64.py)
* [@Thealexbarney](https://github.com/Thealexbarney) - libhac/hactoolnet
* [@blawar](https://github.com/blawar) - für Referenzen zu verschiedenen Dingen in [nut](https://github.com/blawar/nut)
* Alles andere:
* [@borntohonk](https://github.com/borntohonk)