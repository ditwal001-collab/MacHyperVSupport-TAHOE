# HOW-TO: macOS Tahoe direkt auf Hyper-V installieren

Stand: 26.10.2026. Voraussetzung: Hyper-V ist installiert und funktioniert.
Die Windows-Menues koennen deutsch sein; die macOS-Menues sind hier auf Englisch.
Diese Anleitung beschreibt eine Vollinstallation auf einer neuen leeren Platte.
Sie veraendert keine vorhandene VM. Befehle sind zum bewussten Nachmachen bestimmt.

## 1. Was am Ende vorhanden ist

Eine Generation-2-VM mit 8 virtuellen CPUs, 24 GiB festem RAM, einer dynamischen
512-GiB-Systemplatte und macOS Tahoe 26.7.1 / Build 25G241. Dazu gehoeren unser
Release-Hyper-V-Treiber, der Framebuffer mit Software-Cursor und 1920 x 1080.
Sprache: English; Region: Switzerland; Tastatur: Swiss German; Zeitzone: Zurich.
Die persoenliche Apple-Anmeldung erfolgt ausschliesslich durch den Benutzer.

Der nachvollziehbar gepruefte Ablauf hat zwei Abschnitte: Eine leere VM bekommt
zuerst Tahoe ueber Apple Recovery. Dieses frisch eingerichtete, entbehrliche Tahoe
startet danach Apples Vollinstaller mit unserem Setup-Paket. Dabei wird das
System erneut geloescht und frisch angelegt; das temporaere Konto wird verworfen.
Dieser zweite Durchlauf ist noetig, um den tatsaechlich geprueften Transport des
integrierten Setup-Pakets nachzubauen. Einfaches Kopieren des Pakets in Recovery
ist kein Ersatz. Eine einzige Installation auf voellig leerer VM mit automatisch
vorinstalliertem Setup-Paket haben wir nicht als vollstaendigen Ablauf validiert.

Bestaetigt sind die einzelnen Recovery- und Vollinstaller-Durchlaeufe, die
Release-Treiber, die automatische Aufloesung, ein weiterer normaler Neustart und
die vom Benutzer bestaetigte Apple-Anmeldung. Der letzte Apple-Dialog
**Match Settings** benoetigte einen regulaeren Shutdown/Start. Deshalb ist dies
kein vollstaendig unbeaufsichtigter Ein-Klick-Installer. Die neue Windows-VM-
Erstellung ist getrennt von der zuletzt getesteten Installation auf bestehender
VM-Firmware geprueft. Eine neue Freigabehistorie kann weitere Apple-Dialoge zeigen.

## 2. Das Uebergabepaket entpacken

Die Datei mit dem Namen `Tahoe-FullInstall-Handoff-....zip` vollstaendig entpacken.
Nicht direkt aus dem ZIP arbeiten. Im entpackten Ordner liegt diese Datei als
`HOW_TO_TAHOE_DE.md`; `WO_IST_WAS.md` erklaert alle Unterordner.

| Ordner | Inhalt |
| --- | --- |
| changed-files/ | Geaenderte C++-, Header-, Setup-, Build- und Dokumentationsdateien mit Projektpfaden |
| installer/ | MacHyperVSetup.pkg, SetupMedia.zip und die dazugehoerige Provenance |
| installer/IntegratedSetup.iso | Fertiges DVD-Abbild des geprueften Setup-Produkts |
| drivers/ | Originales Release-Treiber-ZIP und Provenance |
| maintainer/ | Patchserie, technische Berichte, anonymisierte Nachweise und Hilfswerkzeuge |

Das Setup-Paket ist fuer Intel Tahoe **25G241** bestimmt. Es installiert keinen
macOS-Vollinstaller. Apple-Installer, KDK, persoenliche EFI und VM-Platten sind
nicht Teil des Pakets. Entwicklertools und persoenliche Kontodaten ebenfalls nicht.

## 3. Werkzeuge und Downloads bereitlegen

Oeffne die Links und lade die angegebenen Werkzeuge. GitHub-Artefakte koennen eine
Anmeldung benoetigen oder ablaufen; die geprueften Originaldateien liegen deshalb
auch im Uebergabepaket. Die Versionsnummern hier gehoeren zum getesteten Aufbau.

| Werkzeug / Download | Link | Verwendung |
| --- | --- | --- |
| Projekt | [MacHyperVSupport-TAHOE](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE) | Quellen und Anleitungen |
| Release-Treiber | [Actions 40189441511](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/actions/runs/40189441511) | Originale Artifacts und Provenance |
| Setup-Installer | [Actions 40269870810](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/actions/runs/40269870810) | IntegratedSetup mit SetupMedia.zip |
| Python fuer Windows | [python.org](https://www.python.org/downloads/windows/) | Log- und Pruefwerkzeuge; Launcher `py` mitinstallieren |
| OpenCore 1.0.6 | [Release](https://github.com/acidanthera/OpenCorePkg/releases/tag/1.0.6) | X64-Bootloader und passendes ocvalidate.exe |
| Apple-Recovery-Downloader | [macrecovery, festes Commit](https://github.com/acidanthera/OpenCorePkg/tree/78d5ff824992d5b227f842e34d8221eb8f31baf1/Utilities/macrecovery) | macrecovery.py, boards.json, README.md |
| Hyper-V-EFI-Vorgaben | [Upstream README](https://github.com/acidanthera/MacHyperVSupport#opencore-configuration) | Erforderliche ACPI-/OpenCore-Einstellungen |
| OpenCore-Grundlagen | [Dortania](https://dortania.github.io/OpenCore-Install-Guide/) | Eigene EFI erstellen |
| ProperTree | [Projekt](https://github.com/corpnewt/ProperTree) | config.plist bearbeiten |
| GenSMBIOS | [Projekt](https://github.com/corpnewt/GenSMBIOS) | Eigene konsistente Mac-Identitaet |
| Lilu 1.7.2 | [Release](https://github.com/acidanthera/Lilu/releases/tag/1.7.2) | EFI-Komponente |
| VirtualSMC 1.3.7 | [Release](https://github.com/acidanthera/VirtualSMC/releases/tag/1.3.7) | EFI-Komponente |
| Apple-Vollinstaller | [Apple Download-Hilfe](https://support.apple.com/102662) | Originales macOS; Download im Gast siehe Schritt 8 |
| KDK 25G241 | [Signiertes Apple-KDK](https://github.com/dortania/KdkSupportPkg/releases/tag/25G241) | Vom Setup automatisch mit Hash-/Signaturpruefung geladen |
| Git / GitHub CLI | [Git](https://git-scm.com/download/win), [gh](https://cli.github.com/) | Nur fuer Quellen und eigene Builds erforderlich |

Keine Installation von Hyper-V oder Aenderung vorhandener Host-Switches noetig.
Du brauchst einen vorhandenen passenden Switch und Internetzugang fuer die VM.
Der Host benoetigt zusaetzlich zu seinem eigenen Bedarf 24 GiB freien RAM und
freien Speicher fuer die wachsende Systemplatte, EFI und Downloads. 512 GiB ist
die virtuelle Plattengroesse, keine sofortige Reservierung aller 512 GiB.

## 4. Eigene EFI vorbereiten - zwingende Voraussetzung

**Das Paket enthaelt keine startfertige EFI.vhdx und keine vollstaendige config.plist.**
Du benoetigst eine unabhaengig gepruefte, eigene Intel-Hyper-V-EFI. Ohne sie hier
anhalten: Ein OpenCore-Download allein macht noch keine bootfaehige VM. Dieser
Teil bleibt technische Vorarbeit; eine universelle Anfaenger-EFI liefern wir nicht.

Das Layout auf einem separaten FAT32-EFI-Datentraeger muss unter anderem enthalten:

```text
EFI/BOOT/BOOTx64.efi
EFI/OC/OpenCore.efi
EFI/OC/config.plist
EFI/OC/ACPI/SSDT-HV-VMBUS.aml
EFI/OC/ACPI/SSDT-HV-DEV.aml
EFI/OC/ACPI/SSDT-HV-PLUG.aml
EFI/OC/Drivers/OpenRuntime.efi
EFI/OC/Kexts/Lilu.kext/
EFI/OC/Kexts/VirtualSMC.kext/
EFI/OC/Kexts/MacHyperVSupportMonterey.kext/
```

ACPI aus den Upstream-Vorgaben kompilieren, nicht .dsl in .aml umbenennen.
Sample.plist, Treiber und ocvalidate muessen zur OpenCore-Version passen.
Core aus `drivers/MacHyperVSupport-0.9.10-RELEASE.zip` verwenden, nicht die
Legacy-Kext und nicht Debug-Dateien. Den Framebuffer **nicht** per OpenCore laden.
Er wird spaeter im Gast installiert. Eine eigene SMBIOS-Identitaet verwenden;
keine fremden Seriennummern oder identische Identitaeten fuer parallele VMs.

Im beobachteten Profil: ProvideCurrentCpuInfo=true, passende Hyper-V-ACPI-Patches,
AvoidRuntimeDefrag/ProvideCustomSlide und DisableSecurityPolicy gemaess Upstream.
CPU-Spoofing ist hostabhaengig. Der gepruefte Bestand hatte csr-active-config
03000000; unsere Helfer schalten SIP/Gatekeeper nicht um. Andere Sicherheits-
oder Hardwareprofile sind durch diesen Test nicht validiert.

Fuer Apple-Dienste muessen beide vorhandenen, zusammengehoerigen Kernel-Patches des
VM-Erkennungs-Workarounds aktiv sein. Unser `prepare-tahoe-efi.ps1` prueft deren
exakte Form, aktiviert nur den fehlenden Teil auf einer neuen Offline-Kopie und
fuehrt ocvalidate aus. Er erzeugt keine vollstaendige EFI und ergaenzt keine fehlenden
Patchvorlagen. Die Quelle muss ungemountet, unabhaengig und keiner VM zugeordnet sein.

Bootargumente fuer die Installation:

```text
-v keepsyms=1 debug=0x12a serial=5 msgbuf=1048576 -hvgfxfbswcursor
```

Kein `-hvstormsgdbg` hinzufuegen. Einen vorhandenen `-nobsdmgroot`-Eintrag in der
Installationskopie entfernen. ShowPicker=true, HideAuxiliary=false verwenden.
Mit ocvalidate pruefen und das Image auf Windows sauber auswerfen.

## 5. Apple Recovery auf die EFI-Arbeitskopie laden

1. Einen neuen lokalen Arbeitsordner anlegen, beispielsweise `Tahoe-NewInstall`.
2. Darin `Recovery`, `Logs` und `Downloads` anlegen. Die eigene ungemountete
   EFI-Kopie unter `EFI.source.vhdx` ablegen. Vorhandene Dateien nie ueberschreiben.
3. macrecovery.py und boards.json in `Downloads` speichern. PowerShell dort oeffnen:

   ```powershell
   py -3 ./macrecovery.py -b Mac-CFF7D910A743CAAF -m 00000000000000000 -os latest -o ../Recovery download
   ```

4. **Image verification complete!** abwarten. Im Test lieferte Apple Recovery
   26.6.2/25G83; das ist nicht die endgueltige installierte OS-Version. Apples
   Angebot kann sich aendern; diese Anleitung prueft nicht live dessen Verfuegbarkeit.
5. Nur die unzugeordnete EFI-Arbeitskopie mounten. BaseSystem.dmg und
   BaseSystem.chunklist nach `com.apple.recovery.boot` auf dem FAT32-Volume kopieren.
   Dann Image sauber auswerfen. Keine laufende EFI und keine Backup-Datei bearbeiten.

## 6. Neue VM anlegen

PowerShell mit den fuer Hyper-V noetigen Rechten oeffnen. Verwende einen neuen
VM-Namen und einen vorhandenen Switch. Die folgenden Pfade sind Beispiele;
`PFAD_ZUM_PAKET`, `PFAD_ZUM_ARBEITSORDNER`, `SWITCHNAME` und `PFAD_ZU_OCVALIDATE`
muessen durch die eigenen Werte ersetzt werden. Nichts auf bestehende VMs anwenden.

```powershell
$tools = 'PFAD_ZUM_PAKET/maintainer/tools'
$work = 'PFAD_ZUM_ARBEITSORDNER'
& "$tools/new-tahoe-test-vm.ps1" -VMName 'Tahoe-NewInstall' -Directory $work -PreparedEFI "$work/EFI.source.vhdx" -SwitchName 'SWITCHNAME' -SerialPipe '\\.\pipe\TahoeNewInstall' -OCValidatePath 'PFAD_ZU_OCVALIDATE/ocvalidate.exe'
```

Das zeigt zunaechst nur den Plan. Stimmen alle Angaben, denselben Befehl mit
zusaetzlichem `-Create` ausfuehren. Existierende VM-Namen oder Ausgaben werden
abgelehnt. Keine globale Skriptrichtlinie abschalten, wenn Windows das Skript
blockiert; dann technisch klaeren, wie es unter der bestehenden Richtlinie laeuft.

Der Helfer bereitet eine neue `EFI.setup.vhdx` vor und legt die VM ausgeschaltet
an: Generation 2, 8 CPUs, 24 GiB fester RAM, dynamische512-GiB-Systemplatte,
Single1920x1080, Secure Boot nur an dieser neuen VM aus, automatische Checkpoints
aus. Er veraendert keinen vorhandenen Switch und startet die VM nicht.

Im Hyper-V Manager vor dem Start kontrollieren:

| Einstellung | Sollwert |
| --- | --- |
| SCSI 0:0 | Neue EFI.setup.vhdx |
| SCSI 0:1 | Neue System.blank.vhdx,512 GiB |
| Firmware / Boot order | EFI-Festplatte zuerst |
| Network Adapter | Vorgesehener vorhandener Switch |
| COM1 | Eigene Pipe aus obigem Befehl |
| Fremde/originale/Backup-Platten | Nicht angeschlossen |

## 7. Logging starten und Tahoe auf die leere Platte installieren

1. In einem zweiten PowerShell-Fenster den seriellen Empfaenger starten:

   ```powershell
   py -3 PFAD_ZUM_PAKET/maintainer/tools/capture-hyperv-serial.py --pipe '\\.\pipe\TahoeNewInstall' --output PFAD_ZUM_ARBEITSORDNER/Logs/boot-01
   ```

2. Fenster offen lassen. Pro Pipe nur einen Empfaenger verwenden. Er verbindet
   sich nach Neustarts wieder. Erst jetzt im Hyper-V Manager **Start > Connect**.
3. In OpenCore **EFI (dmg)** waehlen. Es muss **Reinstall macOS Tahoe** erscheinen.
   Bei einem anderen macOS nicht installieren, sondern Recovery pruefen.
4. **Disk Utility > View > Show All Devices**. Ausschliesslich die neue512-GiB-
   Systemplatte identifizieren. BSD-Nummern wie disk1 oder disk2 sind nicht fest.
5. Nur diese leere Platte mit **Erase** initialisieren: Name **Macintosh HD**,
   Format **APFS**, Scheme **GUID Partition Map**. EFI nicht loeschen.
6. Disk Utility schliessen, **Reinstall macOS Tahoe > Continue**, Macintosh HD
   waehlen. Automatische Neustarts abwarten. Im OpenCore-Picker jeweils den
   begonnenen macOS Installer auf der Zielplatte fortsetzen, spaeter Macintosh HD.
7. Im ersten Setup ein temporaeres lokales Administratorkonto erstellen, keine
   Datenmigration und noch keine persoenliche Apple-Anmeldung. Dieses System und
   Konto werden in Schritt 8 wieder geloescht. Internet muss funktionieren.

Waehrend aktiver Installation nicht ausschalten oder zuruecksetzen. Einzelne
Prozentwerte koennen lange stehen. Ein schwarzes Bild allein beweist keinen
Stillstand; VMConnect, serielle Ausgabe und Installationsphase gemeinsam pruefen.

## 8. Vollinstallation mit unserem integrierten Setup-Paket

Dieser Schritt laeuft **nur in der neuen entbehrlichen Tahoe-VM**, niemals auf
einem wertvollen Mac. Er loescht deren aktuelle APFS-Installation vollstaendig.
Es ist keine Aktualisierung unter Erhalt des temporaeren Kontos.

1. Im Hyper-V Manager die mitgelieferte `installer/IntegratedSetup.iso` als DVD
   dieser neuen VM einlegen. Im Gast muss `/Volumes/HVSETUP` erscheinen.
2. **Applications > Utilities > Terminal** oeffnen:

   ```sh
   softwareupdate --fetch-full-installer --full-installer-version 26.7.1
   ```

3. Download vollstaendig abwarten. Wird die Version nicht angeboten, abbrechen;
   ein anderer Build ist ein neuer, nicht durch diesen Ablauf gepruefter Stand.
4. Paket und Installationsziel pruefen:

   ```sh
   shasum -a 256 /Volumes/HVSETUP/MacHyperVSetup.pkg
   diskutil list
   diskutil info /System/Volumes/Data
   "/Applications/Install macOS Tahoe.app/Contents/Resources/startosinstall" --usage
   ```

   Der Paket-Hash muss sein:
   `2092d73838908edb86418cc16983052c19b0625bc1d265f33402abf8c5723443`.
   Data muss zur neuen512-GiB-Systemplatte gehoeren, nicht zur EFI oder einem
   anderen Datentraeger. Die Host-Zuordnung aus Schritt 6 mitpruefen. Bei Unklarheit
   nicht fortfahren. Der Installer muss --eraseinstall und --installpackage kennen.
5. Erst nach dieser Pruefung den exakten Vollinstallationsbefehl ausfuehren:

   ```sh
   sudo "/Applications/Install macOS Tahoe.app/Contents/Resources/startosinstall" \
     --eraseinstall --newvolumename "Macintosh HD" \
     --installpackage /Volumes/HVSETUP/MacHyperVSetup.pkg \
     --agreetolicense --rebootdelay 15 --user "$USER" --passprompt
   ```

6. Das temporaere lokale Admin-Passwort nur an den nativen Passwortabfragen eingeben;
   nicht in Befehle oder Dateien schreiben. Vorbereitung und automatische Neustarts
   vollstaendig abwarten. Im letzten Test dauerte die Vorbereitung etwa23Minuten.
   Das ist eine Beobachtung, kein Zeitlimit fuer andere Rechner.

Das Produkt laedt das hashgepruefte Apple-signierte KDK und installiert den
geprueften Framebuffer ueber die Auxiliary Kernel Collection. Unser Core bleibt
auf der EFI. Das Paket umgeht keine native Erweiterungsfreigabe und setzt
keine persoenliche Apple-Anmeldung. Eine normale Erstinstallations-DVD von Apple
plus in Recovery kopiertes Paket ist nicht als gleichwertiger Ablauf geprueft.

## 9. Endgueltiges macOS einrichten

1. **English**, **Switzerland**, **Swiss German** waehlen. Keine Migration.
2. Endgueltigen lokalen Benutzer anlegen. Vollstaendigen Namen und Kurzname getrennt
   kontrollieren. Ein eigenes Passwort waehlen; keine vorgegebenen Testpasswoerter.
3. Apple-Anmeldung nach Wunsch persoenlich durchfuehren. Keine Zugangsdaten teilen.
   Im finalen Test hat der Benutzer die erfolgreiche Anmeldung bestaetigt.
4. FileVault und persoenliche Synchronisation bewusst auswaehlen. Im finalen Test
   blieb FileVault aktiv; es wird von unserem Setup nicht abgeschaltet.
5. Wenn macOS eine Erweiterungsfreigabe verlangt: **System Settings > Privacy &
   Security > Allow**, lokal authentifizieren und den angeforderten normalen
   Neustart durchfuehren. Keine Sicherheitsdatenbanken oder Keychains loeschen.
6. **Match Settings** kann haengen. Zuerst Setup-/Serial-Fortschritt pruefen und
   warten. Im Test war nach mehr als6Minuten ein regulaerer Gast-Shutdown/Start
   erfolgreich. Keine aktive Installation hart ausschalten. Wenn der Gast nicht
   regulaer herunterfaehrt, Zustand und Logs sichern statt einen Reset zu erzwingen.
7. FileVault beim Start persoenlich entsperren. Danach sollte die Setup-App die
   Aufloesung automatisch auf1920x1080 stellen. Im FileVault-Vorstartbildschirm
   kann die Aufloesung niedriger sein; das ist nicht der normale Desktop.
8. In **System Settings > General > About** den Computernamen setzen. Unter
   **General > Date & Time** Europe/Zurich kontrollieren. Unter **Users & Groups**
   den ausgeschriebenen Kontonamen pruefen. Diese Profilwerte mussten wir im Test
   nachkorrigieren; das Setup-Paket setzt sie nicht automatisch.

## 10. Pruefen, ob wirklich alles fertig ist

Im Terminal ausfuehren:

```sh
sw_vers
sysctl kern.hv_vmm_present
kextstat -b fish.goldfish64.MacHyperVSupport
kextstat -b fish.goldfish64.MacHyperVFramebuffer
/Applications/MacHyperVSetup.app/Contents/MacOS/MacHyperVSetup --verify-display
shasum -a 256 /Library/Extensions/MacHyperVFramebuffer.kext/Contents/MacOS/MacHyperVFramebuffer
fdesetup status
```

| Pruefung | Erwartet |
| --- | --- |
| macOS | 26.7.1 / 25G241 |
| kern.hv_vmm_present | 0 bei vorbereitetem Patchpaar |
| Core-UUID | 7CAF03F1-3631-33A9-AAAF-581270B665B0 |
| Framebuffer-UUID | 3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6 |
| Display | width1920, height1080 |
| Framebuffer-SHA256 | d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122 |
| FileVault | Entsprechend der persoenlichen Auswahl |

- [ ] Finder, Downloads und Safari oeffnen; Maus, Klick-Fokus und Tastatur testen.
- [ ] Cursor bleibt sichtbar; eine HTTPS-Webseite laedt.
- [ ] Computername, vollstaendiger Kontoname, Uhrzeit und Tastaturlayout stimmen.
- [ ] ueber **Apple menu > Restart** normal neu starten, FileVault entsperren und
      die obigen Pruefungen wiederholen.
- [ ] Setup-DVD auswerfen und im Hyper-V Manager deren ISO-Zuordnung entfernen.
      **EFI-Festplatte angeschlossen lassen.**
- [ ] Serial-Logging zunaechst weiterlaufen lassen und spaetere Auffaelligkeiten notieren.

Zur automatischen Aufloesungspruefung nicht manuell Displays umstellen oder
--set-display aufrufen: Das wuerde einen Fehler des Setup-Ablaufs verdecken.

Bei Fehlern liegen die Setup-Logs unter
`/Library/Application Support/MacHyperVSetup/activation.log`, `setup.log` und
`status.txt`. Version, UUIDs, EFI-Konfigurationshash, Zeit und serielle Ausgabe
zusammen sichern. Private Namen, IPs, Seriennummern und Authentifizierungsdaten
vor einer Weitergabe entfernen.

## 11. Was der Maintainer bekommt und was der Test beweist

Die Changed-Files-Liste nennt fuer jede gelieferte Datei deren Quellstand und
Projektpfad. Treiberquelle:6c3568178ba21136b8c21dd45597476c74ec31d1,
Actions40189441511. Setup-Quelle:00f70ee358e4d9ddad2fccca39bc19ede1d55365,
Actions40269870810. Das Release-ZIP hat SHA256
162f47670ef9f4640bdfdefd8ba9495b1a039ca6828a52f5ec4498e9d3cb5d6c;
SetupMedia.zip hat SHA256
81a7b6a4706ecde370351ad1a9d2b739f75b0843efa3cae49237942821630633.

Die Treiber-Patchserie baut auf dem bestehenden GraphicsBridge-Fix von startergo
c48fc5ccade272ec79f633dcb23e45ba1c40d6cc auf; dessen Attribution und Qonfused-
Credit bleiben erhalten. SynIC-CPU-Zuordnung, Frame-Refresh und opt-in Software-
Cursor sind getrennte Aenderungen. Der Software-Cursor ist ein Workaround;
die Ursache des Hardware-Cursor-Problems ist damit nicht erklaert.

Der finale Vollinstallationstest erreichte den Desktop, beide Release-Treiber,
automatische1920x1080 und einen weiteren normalen Neustart. Der Benutzer bestaetigte
Apple-Anmeldung. Match Settings und die Profilkorrekturen bleiben dokumentierte
Einschraenkungen. Die Freigabehistorie der VM wurde nicht geloescht. Clean Release
enthaelt keine einzelnen EOM-CPU-Messzeilen; ein erfolgreiches Boot beweist deshalb
keine neue CPU-Lokalitaetsmessung oder allgemeine Langzeitstabilitaet.

Diese Anleitung benoetigt keine historischen Betriebsversuche zum Nachmachen.
Die technischen Nachweise bleiben getrennt unter `maintainer/` erhalten.
