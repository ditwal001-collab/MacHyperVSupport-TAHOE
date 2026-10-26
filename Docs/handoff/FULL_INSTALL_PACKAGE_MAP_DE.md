# Was liegt wo?

Zuerst `HOW_TO_TAHOE_DE.md` im Hauptordner lesen. Das ist die einzige Anleitung
zum Nachmachen: Hyper-V ist bereits installiert; danach folgen alle Schritte
zur direkten Tahoe-Vollinstallation. Die technischen Berichte sind Beilagen.

| Pfad im Paket | Inhalt / Verwendung |
| --- | --- |
| HOW_TO_TAHOE_DE.md | Zentrale Schritt-fuer-Schritt-Anleitung mit Downloads, Voraussetzungen, Installation und Kontrollen |
| changed-files/MacHyperVSupport/ | Geaenderte Core-/Graphics-C++-Dateien und Header in der Projektstruktur |
| changed-files/MacHyperVFramebuffer/ | Geaenderte Framebuffer-C++-Datei und Header |
| changed-files/Tools/Setup/ | Objective-C-App, Bootstrap und Paket-Nachinstallation |
| changed-files/.github/workflows/main.yml | Build-Workflow mit Setup-Auswahl |
| changed-files/BuildScripts/ | Build-, EFI-, Logging-, Medien- und Exportwerkzeuge |
| changed-files/Docs/handoff/ | Oeffentliche Dokumentationsdateien |
| CHANGED_FILES.json | Jede gelieferte Quelldatei mit Projektpfad, Quellcommit und SHA256 |
| installer/MacHyperVSetup.pkg | Ausfuehrbares macOS-Installationspaket; im geprueften Ablauf ueber Apples --installpackage verwenden |
| installer/IntegratedSetup.iso | Fertige Werkzeug-DVD fuer Hyper-V; kein bootfaehiger macOS-Vollinstaller |
| installer/SetupMedia.zip | Unveraendertes originales CI-Produkt, einschliesslich App, Daemon und Paket |
| installer/provenance.json | Originale CI-Provenance und Nutzdatei-Hashes |
| drivers/MacHyperVSupport-0.9.10-RELEASE.zip | Originale Release-Treiber; Monterey-Core fuer Tahoe verwenden |
| drivers/Provenance/ | Originale Treiber-Buildnachweise |
| maintainer/patches/ | Fuenf getrennte, auf dem dokumentierten GraphicsBridge-Basiscommit aufbauende Patches |
| maintainer/integrated-setup/ | Optionaler Setup-Patch0006 und originale Produktnachweise |
| maintainer/documentation/ | Technische Berichte, Testgrenzen und anonymisiertes Testprotokoll |
| maintainer/evidence/ | Kuratierte anonymisierte Build-/Boot-/Installationsergebnisse |
| maintainer/tools/ | Direkt nutzbare Hilfswerkzeuge fuer die Anleitung |
| MANIFEST.json / SHA256SUMS.txt | Inhaltsverzeichnis mit SHA256 fuer die enthaltenen Nutzdateien |

`changed-files/` enthaelt tatsaechliche vollstaendige Dateistaende, keine leeren
Platzhalter und keine komplette Repository-Kopie. Die Dateien dienen dem Review.
Zum Anwenden der Aenderungen verwendet der Maintainer die getrennte Patchserie
gegen den gepinnten Basiscommit; bestehende Projektdateien nicht blind ersetzen.
Der Workflow enthaelt die spaetere Setup-Auswahl. CHANGED_FILES.json unterscheidet
dessen Stand von dem urspruenglichen reinen Treiber-CI-Stand.

Das Installationspaket ist ein macOS-Paket, keine Windows-EXE. Es enthaelt unsere
Hilfsprogramme und den geprueften Treiber. Der Apple-Installer wird separat von
Apple geladen. Keine persoenliche EFI, VHDX, Seriennummern, Kennwoerter oder
Apple-Kontodaten werden geliefert. Lokale Betriebsnotizen und Scratch-Backups
gehoeren nicht zum Ordner der geaenderten Quelldateien.

PowerShell: eine einzelne Datei pruefen, beispielsweise:

```powershell
Get-FileHash -Algorithm SHA256 ./installer/MacHyperVSetup.pkg
```

Erwarteter Paket-SHA256:
`2092d73838908edb86418cc16983052c19b0625bc1d265f33402abf8c5723443`.
Die Pruefsumme des gesamten ZIP wird separat im Lieferbeleg genannt.
