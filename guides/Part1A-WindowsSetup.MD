Teil 1A: Einrichtung von Ghidra

Diese Anleitung wurde für Windows 10/11 erstellt und setzt voraus, dass du eine Git-Shell installiert hast und in der Lage bist, CMD/PowerShell-Terminals an gewünschten Speicherorten zu öffnen.

1. Lade OpenJDK 21 LTS entweder von https://adoptium.net/ oder https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.4%2B7/OpenJDK21U-jdk_x64_windows_hotspot_21.0.4_7.msi herunter
2. Installiere das heruntergeladene OpenJDK (stelle sicher, dass während der Installation der JAVA_HOME-Pfad gesetzt wird)
3. Lade Ghidra von https://github.com/NationalSecurityAgency/ghidra/releases/latest herunter
4. Entpacke die Datei (zum Beispiel ghidra_11.2_PUBLIC_20240926.zip) und verschiebe den Ordner (zum Beispiel "ghidra_11.2_PUBLIC_20240926") nach C:/ghidra/ghidra_11.2_PUBLIC
5. Hole dir das Code-Repository mit dem Befehl "git clone https://github.com/borntohonk/Ghidra-Switch-Loader"
6. Öffne ein CMD-Terminal im gerade geklonten Ordner und gib (set "GHIDRA_INSTALL_DIR" "C:/ghidra/ghidra_11.2_PUBLIC") ohne die Klammern in dein CMD-Terminal oder PowerShell ein, oder setze es manuell als Umgebungsvariable. (dieser Wert bleibt nur bestehen, solange das CMD-Fenster geöffnet ist, verlasse dich nicht auf den "set"-Befehl für verschiedene Sitzungen)
7. Führe gradlew im Ghidra-Switch-Loader-Verzeichnis aus, indem du auf "gradlew.bat" klickst oder ./gradlew in deinem CMD/PowerShell-Terminal eingibst
8. Gehe zu deinem Ghidra-Ordner (sollte in diesem Beispiel C:\ghidra\ghidra_11.2_PUBLIC sein)
9. Klicke oben links auf "File" und dann auf "Install extensions"
10. Drücke den +-Button in der oberen rechten Ecke
11. Navigiere zu deinem Ghidra-Switch-Loader-Ordner und dann in den "dist"-Ordner, den er erstellt hat, und wähle die .zip-Datei aus, die sich dort befinden sollte
12. Starte Ghidra neu

Anleitung für Winget-Benutzer (Windows 11 hat Winget bereits vorinstalliert), öffne PowerShell als Administrator und führe folgende Befehle aus:

# (stelle sicher, dass das Java-Home-Verzeichnis gesetzt ist)
1. winget install -i EclipseAdoptium.Temurin.21.JDK
# (nur nötig, wenn du noch keine Git-Shell installiert hast)
2. winget install git.git
3. curl -fsSL https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.2_build/ghidra_11.2_PUBLIC_20240926.zip -O
4. mkdir C:/ghidra
5. Expand-Archive -LiteralPath "ghidra_11.2_PUBLIC_20240926.zip" -DestinationPath "C:/ghidra"
6. rm ghidra_11.2_PUBLIC_20240926.zip
7. git clone https://github.com/borntohonk/Ghidra-Switch-Loader
8. cd Ghidra-Switch-Loader
# (beachte, dass dies die Ausführung des Terminals als Administrator erfordert)
9. [Environment]::SetEnvironmentVariable("GHIDRA_INSTALL_DIR", "C:/ghidra/ghidra_11.2_PUBLIC" ,"Machine")
10. ./gradlew
11. cd dist
12. Get-ChildItem './' -Filter *.zip | Expand-Archive -DestinationPath 'C:/ghidra/ghidra_11.2_PUBLIC/Ghidra/Extensions' -Force
Du kannst Ghidra jetzt über ghidraRun.bat in C:\ghidra\ghidra_11.2_PUBLIC starten


![alt text](https://github.com/borntohonk/Switch-Ghidra-Guides/blob/master/img/ghidra-w.png?raw=true)