Dieses Repository enthält Reverse-Engineering-Notizen und Anleitungen zu Bildungszwecken, die Open-Source-Tools wie Ghidra verwenden, um Binärdateien für die Nintendo Switch zu analysieren. Es enthält auch grundlegende Methoden zur Verwendung von Ghidra für die Untersuchung von "ARM"-Binärdateien, die auf der Nintendo Switch laufen.

Dieses Repository hostet keine Anleitungen zur Umgehung von Sicherheitsmaßnahmen, die digitale Inhalte schützen, und enthält auch keine entsprechenden Guides.

Das gesamte Material dient ausschließlich als Forschungsreferenz.

* Ghidra/Patch-Erstellung Tutorial:
  - Teil 1A erklärt die Einrichtung von Ghidra und dem Switch-Loader für Windows [(link)](guides/Part1A-WindowsSetup.MD)
  - Teil 1B erklärt die Einrichtung von Ghidra und dem Switch-Loader für Linux [(link)](guides/Part1B-LinuxSetup.MD)
  - Teil 2 erklärt die Einrichtung von Hactoolnet zur Ausgabe von Dateien für die weitere Verarbeitung und eine grundlegende Einführung in Ghidra mit der Erstellung von Patches für nifm als Beispiel. [(link)](guides/Part2.MD)
  - Die resultierenden "Patches" aus dieser Anleitung findest du unter https://github.com/misson20000/exefs_patches/tree/master/atmosphere/exefs_patches/nfim_ctest

**Hinweis: Der erwähnte "Loader" bezieht sich auf die Re-Implementierung des "Atmosphere"-Projekts: https://github.com/Atmosphere-NX/Atmosphere/tree/master/stratosphere/loader**

* Hier ist eine Liste von Skripten, die dem Beispiel aus Teil 2 der obigen Anleitung folgen und in diesem Repository enthalten sind:

  - Python-Skript zum Abrufen der neuesten mariko_master_kek_source_%% aus bereitgestellten Firmware-Dateien und zum Bereitstellen von Strings zur Aktualisierung der Arrays für key_sources.py, benötigt lz4 von pip  
    * Beispielverwendung: "python scripts/mariko_master_kek_source.py --firmware firmware" [mariko_master_kek_source.py](scripts/mariko_master_kek_source.py)
    * Benötigt pycryptodome/pycryptodomex (oder python3-pycryptodome aus apt für debian/ubuntu, was pycryptodomex ist, python-pycryptodome aus den arch linux pacman Repositories, was pycryptodome ist)
    * Die Aktualisierung von scripts/key_sources.py kommt der Schlüsselgenerierung für [aes_sample.py](scripts/aes_sample.py) zugute

  - Python-Skript zur Ableitung des gesamten Schlüsselsatzes [aes_sample.py](scripts/aes_sample.py)
    * Die beschriebene kryptographische Logik kann mit diesem Python-Skript getestet werden, Ausgabe-Schlüsseldatei (Standard "prod.keys", kann mit -k geändert werden): [aes_sample.py](scripts/aes_sample.py)
    * Es gibt auch eine Entwicklervariante, die auf die gleiche Weise funktioniert, [aes_sample_dev.py](scripts/aes_sample_dev.py)
    * Benötigt pycryptodome/pycryptodomex (oder python3-pycryptodome aus apt für debian/ubuntu, was pycryptodomex ist, python-pycryptodome aus den arch linux pacman Repositories, was pycryptodome ist)

  - Python-Skript zum Überprüfen bekannter Muster für sys-patch
    * Verwendung: Firmware-Dateien in einen Ordner namens firmware legen oder einen Speicherort mit -l oder --location angeben, Schlüssel mit -k oder --keys bereitstellen, ansonsten wird standardmäßig ~/.switch/prod.keys verwendet
    * Beispielverwendung: "python scripts/check_patches.py --location temp_folder --keys prod.keys"
    * [check_patches.py](scripts/check_patches.py)
    * Benötigt pycryptodome/pycryptodomex (oder python3-pycryptodome aus apt für debian/ubuntu, was pycryptodomex ist, python-pycryptodome aus den arch linux pacman Repositories, was pycryptodome ist)

  - Python-Skript zur Generierung des "[disable_ca_verification patch](https://github.com/misson20000/exefs_patches#disable-ca-verification)", [(link)](scripts/disable_ca_verification_patch.py) - wird seit Firmware-Version 19.0.0 nicht mehr gepflegt

  - Python-Skript zur Generierung des "[disable_browser_ca_verification patch](https://github.com/misson20000/exefs_patches#disable-browser-ca-verification)", [(link)](scripts/disable_browser_ca_verification_patch.py) - wird seit Firmware-Version 19.0.0 nicht mehr gepflegt

* Danksagungen: 
* [@sciresm](https://github.com/SciresM) - hactool - [(scripts/aes128.py)](scripts/aes128.py)
* [@reswitched](https://github.com/reswitched) - [(scripts/nxo64.py)](scripts/nxo64.py)
* [@Thealexbarney](https://github.com/Thealexbarney) - libhac/hactoolnet
* [@blawar](https://github.com/blawar) - für Referenzen zu verschiedenen Dingen in [nut](https://github.com/blawar/nut)
* Alles andere:
* [@borntohonk](https://github.com/borntohonk)