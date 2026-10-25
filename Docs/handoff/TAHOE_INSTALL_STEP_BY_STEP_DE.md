# Tahoe auf Hyper-V: Schritt fuer Schritt

Stand: 25.10.2026. Erklaerungen auf Deutsch; Menuebezeichnungen auf Englisch.
Diese Datei ist eine Vorbereitung und Installations-Checkliste, kein bereits
vollstaendig validierter Ein-Klick-Installer. Alle folgenden Befehle sind zum
Nachlesen; beim Schreiben dieser Anleitung wurde keine VM angelegt oder geaendert.

**Nachtrag zum laufenden Praxistest:** In einem spaeteren, ausdruecklich
beauftragten Neuinstallationstest wurde eine neue VM angelegt. Apple-Tahoe-
Recovery startete direkt, und die neue leere Systemplatte wurde initialisiert.
Die Installation ist noch nicht abgeschlossen. Der tatsaechlich benutzte
Windows-Recovery-Weg steht in Schritt6a und im [Testprotokoll](FRESH_INSTALL_TEST.md).
Die urspruenglichen Vollinstaller-Schritte6 und die fertige Neuinstallation
bleiben davon getrennt; noch keine Ende-zu-Ende-Erfolgsgarantie.

## 1. Zuerst verstehen, was bereits funktioniert

Unser Intel-Testsystem startet macOS Tahoe 26.7.1, Build 25G241. Der bereinigte
Release-Core und Release-Framebuffer sind geladen; ihre UUIDs stimmen mit den
originalen CI-Binaries ueberein. Ein vollstaendiger Release-Start ist nachgewiesen.
Zuvor lief die instrumentierte Debug-Variante mehr als elf Stunden.

**Eine direkte Neuinstallation von Tahoe auf eine komplett leere Hyper-V-Platte
haben wir noch nicht von Anfang bis Ende getestet.** Die bestehende Installation
entstand im Kontext eines Sequoia/Tahoe-Upgrades. Insbesondere eine allgemein
verteilbare, startfertige EFI und ein universeller Framebuffer-Erstinstaller
fehlen noch. Diese Luecken werden unten als Kontrollpunkte benannt.

Du musst nicht zuerst Sequoia installieren, um den hier beschriebenen direkten
Tahoe-Installationsweg zu versuchen. Das ist aber ein geplanter Installationsweg,
kein durch unseren bisherigen Test bewiesenes Versprechen.

Begriffe:

| Begriff | Bedeutung |
| --- | --- |
| Host | Der Windows-Rechner mit Hyper-V |
| Gast / VM | Der virtuelle Mac |
| VHDX | Eine Datei, die Hyper-V als Festplatte verwendet |
| EFI / OpenCore | Der Bootloader, der macOS in dieser VM starten hilft |
| Kext | Ein macOS-Kerneltreiber |
| Core | Unser Hyper-V-Treiber fuer Bus, Storage, Netzwerk und Eingabe |
| Framebuffer | Der separate Bildschirmtreiber |
| Serial-Log | Bootprotokoll auf dem Windows-Host, auch wenn das Bild schwarz ist |

## 2. Was du brauchst

Fuer einen moeglichst nahen Vergleich mit unserem Aufbau:

1. Intel-x64-Windows-Rechner mit aktivierter Hardwarevirtualisierung und Hyper-V.
2. Genug Arbeitsspeicher fuer Windows plus 24 GiB festen VM-Speicher.
3. Acht virtuelle Prozessoren fuer die VM.
4. Eine neue dynamische 400-GiB-Systemplatte. Die Datei waechst mit der Belegung;
   400 GiB sind die virtuelle Obergrenze, keine sofortige Reservierung.
5. Zusaetzlichen Platz fuer Installer, EFI und eine vollstaendige Rueckfallkopie.
6. Internet und einen vorhandenen passenden virtuellen Netzwerk-Switch.
7. Zugriff auf einen Mac fuer den hier beschriebenen Apple-Vollinstaller-Weg.
   Unser bereits laufender Mac kann Material vorbereiten; sein Systemlaufwerk
   darf dabei nicht geloescht oder als Installerziel verwendet werden.

Intel ist unsere getestete Plattform. AMD- und ARM-Hosts sind durch diese Arbeit
nicht validiert. Ein Hyper-V-Haken emuliert keinen Apple-M-Chip.

## 3. Downloadliste: diese Links verwenden

Bei GitHub: Seite oeffnen, gegebenenfalls **Assets** ausklappen, Datei laden.
Bei Werkzeugen ohne feste Version: Version und Download-Pruefsumme fuer deinen
Versuch notieren. Nicht mitten im ersten Vergleich alle Komponenten aktualisieren.

| Download / Werkzeug | Link | Wofuer? |
| --- | --- | --- |
| Unser Projekt | [MacHyperVSupport-TAHOE](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE) | Quellcode und Dokumentation |
| Unser gepruefter Build | [Actions-Lauf 40189441511](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/actions/runs/40189441511) | Artefakte **Artifacts** und **Provenance**; ggf. GitHub-Anmeldung erforderlich |
| Unser Release-Quellstand | [Commit 6c356817](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/tree/6c3568178ba21136b8c21dd45597476c74ec31d1) | Exakter Treiberstand |
| Anleitung und Hilfswerkzeuge | [Delivery-Branch](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/tree/maintainer/hyperv-release-delivery) | Diese Anleitung und BuildScripts |
| Alle Hilfswerkzeuge als ZIP | [Delivery-Branch herunterladen](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/archive/refs/heads/maintainer/hyperv-release-delivery.zip) | Entpacken; fuer die Befehle den enthaltenen Repository-Ordner oeffnen |
| Apple macOS-Download | [Apple: macOS laden/installieren](https://support.apple.com/102662) | Originalinstaller; dort Tahoe waehlen, nicht automatisch das neueste andere macOS |
| Apple Installationsmedium | [Apple: bootfaehiges Installationsprogramm](https://support.apple.com/101578) | Erklaerung zu createinstallmedia |
| Hyper-V | [Microsoft: Hyper-V installieren](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/install-hyper-v) | Windows-Voraussetzungen und Installation |
| OpenCore 1.0.6 | [Release 1.0.6](https://github.com/acidanthera/OpenCorePkg/releases/tag/1.0.6) | Historisch berichtete EFI-Version; RELEASE-ZIP, X64-Verzeichnis |
| Lilu 1.7.2 | [Release 1.7.2](https://github.com/acidanthera/Lilu/releases/tag/1.7.2) | Lilu.kext; Versionsreferenz unseres Aufbaus |
| VirtualSMC 1.3.7 | [Release 1.3.7](https://github.com/acidanthera/VirtualSMC/releases/tag/1.3.7) | VirtualSMC.kext; historische Versionsreferenz |
| Hyper-V-EFI-Anforderungen | [Upstream MacHyperVSupport README](https://github.com/acidanthera/MacHyperVSupport#opencore-configuration) | ACPI und Hyper-V-spezifische OpenCore-Vorgaben |
| OpenCore-Anleitung | [Dortania](https://dortania.github.io/OpenCore-Install-Guide/) | Aufbau und Erklaerung der EFI |
| ProperTree | [Projekt und Download ZIP](https://github.com/corpnewt/ProperTree) | config.plist bearbeiten; ZIP ueber Code > Download ZIP |
| GenSMBIOS | [Projekt](https://github.com/corpnewt/GenSMBIOS) | Eigene virtuelle Mac-Identitaet erstellen |
| Python | [Windows-Downloads](https://www.python.org/downloads/windows/) | Unsere Log-/Pruefwerkzeuge und ProperTree |
| Git | [Git fuer Windows](https://git-scm.com/download/win) | Repository laden; fuer reine Binaerinstallation optional |
| GitHub CLI | [Download](https://cli.github.com/) | Artefakte per gh laden; alternativ Browser |
| QEMU / qemu-img | [Offizielle Downloadseite](https://www.qemu.org/download/#windows) | Offline-Image-Konvertierung; Windows-Builds sind dort verlinkt |
| QEMU-Befehlsreferenz | [qemu-img](https://www.qemu.org/docs/master/tools/qemu-img.html) | Imageformate und Konvertierung |
| Apple KDK | [Apple Developer Downloads](https://developer.apple.com/download/all/) | Passendes Kernel Development Kit; ggf. Anmeldung |
| KDK fuer unseren exakten Build | [25G241](https://github.com/dortania/KdkSupportPkg/releases/tag/25G241) | Apple-signiertes KDK, das in unserem Testgast installiert war |

Das Maintainer-ZIP bekommst du momentan als Datei vom Projektersteller. Es gibt
noch keinen veroeffentlichten GitHub-Release-Download dieses ZIPs. Actions-
Artefakte koennen ablaufen. Fehlt der Lauf, das archivierte Paket verwenden;
nicht irgendeinen aehnlich benannten Build ersetzen. OpenCore/Lilu/VirtualSMC
sind eigenstaendige Komponenten, nicht unser neuer SynIC-Fix.

## 4. Unseren richtigen Treiber auswaehlen

Im Maintainer-Paket:

```text
binaries/clean-rc1/MacHyperVSupport-0.9.10-RELEASE.zip
```

Entpacken. Darin unter `Kexts`:

| Datei | Verwendung bei Tahoe |
| --- | --- |
| MacHyperVSupportMonterey.kext | Core-Treiber fuer Tahoe; Name Monterey ist richtig |
| MacHyperVFramebuffer.kext | Separat im Gast installieren, siehe Schritt 12 |
| MacHyperVSupport.kext | Legacy-Treiber; nicht als Tahoe-Core einsetzen |

Das ganze `.kext`-Verzeichnis zusammenhalten. Es ist ein Bundle mit Info.plist
und ausfuehrbarer Datei, kein einzelnes Windows-Programm.

Release-ZIP SHA256:

```text
162f47670ef9f4640bdfdefd8ba9495b1a039ca6828a52f5ec4498e9d3cb5d6c
```

Windows PowerShell im Ordner der ZIP-Datei:

```powershell
Get-FileHash -Algorithm SHA256 .\MacHyperVSupport-0.9.10-RELEASE.zip
```

Die ausgegebene Zeichenfolge muss uebereinstimmen. Gross-/Kleinschreibung ist egal.
Keine Debug-Dateien aus den historischen Referenzordnern beimischen.

Optional per GitHub CLI statt Browser:

```powershell
gh auth login
gh run download 40189441511 --repo ditwal001-collab/MacHyperVSupport-TAHOE --dir .\downloaded-build
```

Zielordner neu waehlen. Anschliessend Paket und Provenance pruefen. Zum normalen
Installieren sind weder eigener Xcode-Build noch neuer Actions-Lauf notwendig.

## 5. Ordner anlegen und bestehende Installation schuetzen

Auf Windows einen **neuen**, eindeutig benannten Arbeitsordner anlegen:

```text
Tahoe-NewInstall/
  Downloads/
  EFI/EFI.vhdx
  Installer/TahoeInstaller.vhdx
  Disks/System.vhdx
  Logs/
  Backups/
```

EFI = Bootloader, Installer = Apple-Installationsmedium, System = Zielplatte.
Diese drei Dateien haben verschiedene Aufgaben. Keinen alten Datentraeger
umbenennen und als neue leere Systemplatte ausgeben. Bereits existierende
VMs/Backups bleiben unveraendert. Die folgende Anleitung erstellt keine
zusaetzliche VM automatisch; sie ist fuer einen spaeteren bewussten Neuaufbau.

## 6. Apple-Tahoe-Installer vorbereiten

1. Auf dem vorbereitenden Mac den vollstaendigen **Install macOS Tahoe.app**
   von Apple laden. Eine Recovery mit **Reinstall macOS Sequoia** ist falsch.
2. Liegt die App in **Applications**, einen automatisch geoeffneten Installer
   beenden. Noch nichts auf diesem Mac installieren.
3. Im Terminal die verfuegbaren Installer anzeigen:

   ```sh
   softwareupdate --list-full-installers
   ```

4. Wenn Apple exakt 26.7.1 anbietet, kann sie gezielt geladen werden:

   ```sh
   softwareupdate --fetch-full-installer --full-installer-version 26.7.1
   ```

   Ist die Version nicht verfuegbar, keine fremde ISO verwenden. Eine andere
   Tahoe-Version bedeutet einen neuen, separat zu pruefenden Versionsstand.
5. Neues, ausschliesslich fuer den Installer bestimmtes Image erstellen. Die
   folgenden Befehle sind ein **noch nicht im Projekt durchgetesteter** Weg
   mit Apples createinstallmedia und anschliessender RAW/VHDX-Konvertierung.
   Sie werden auf dem vorbereitenden Mac ausgefuehrt:

   ```sh
   work=$(mktemp -d /Users/Shared/TahoeMedia.XXXXXXXX)
   test ! -e /Volumes/TahoeInstallWork
   test ! -e '/Volumes/Install macOS Tahoe'
   hdiutil create -size 32g -layout GPTSPUD -fs HFS+J -volname TahoeInstallWork -type UDRW -o "$work/TahoeInstaller.dmg"
   hdiutil attach "$work/TahoeInstaller.dmg" -nobrowse
   ```

6. **Vor dem folgenden Befehl** mit `diskutil info /Volumes/TahoeInstallWork`
   pruefen: Das Volume muss zu dem gerade erzeugten Disk-Image gehoeren.
   createinstallmedia loescht sein Zielvolume. Es darf ausschliesslich dieses
   neue temporaere Image sein, niemals die Systemplatte oder ein Backup.

   ```sh
   sudo '/Applications/Install macOS Tahoe.app/Contents/Resources/createinstallmedia' --volume /Volumes/TahoeInstallWork
   ```

7. Die Loeschbestaetigung gilt nur fuer dieses neue Installationsmedium.
   Vollstaendigen Abschluss abwarten. Den von Apple ausgegebenen Volumenamen
   kontrollieren. Anschliessend das Image sauber auswerfen:

   ```sh
   hdiutil detach '/Volumes/Install macOS Tahoe'
   hdiutil convert "$work/TahoeInstaller.dmg" -format UDTO -o "$work/TahoeInstaller"
   ```

8. Die entstandene `TahoeInstaller.cdr` nach Windows in den neuen Installer-
   Ordner kopieren. `UDTO` liefert hier das RAW-CD/DVD-Master-Abbild; die
   folgende Konvertierung darf **nicht** blind auf irgendeine komprimierte
   heruntergeladene DMG angewandt werden.
9. Auf Windows im neuen Installer-Ordner, mit installiertem qemu-img:

   ```powershell
   if (Test-Path .\TahoeInstaller.vhdx) { throw 'Zieldatei existiert bereits' }
   qemu-img convert -p -f raw -O vhdx .\TahoeInstaller.cdr .\TahoeInstaller.vhdx
   qemu-img info .\TahoeInstaller.vhdx
   Get-FileHash -Algorithm SHA256 .\TahoeInstaller.vhdx
   ```

   Wenn qemu-img nicht gefunden wird, den vollstaendigen Pfad zu qemu-img.exe
   verwenden. Installer ist eine weitere SCSI-Festplatte, keine normale ISO-DVD.
   Konvertierungen nur offline; niemals ein laufendes Image bearbeiten.

**Kontrollpunkt A:** Apple-Installer stammt aus bekannter Quelle; Tahoe statt
Sequoia; neue Installer-VHDX fertig; keine bestehende Platte geloescht.

Windows-Alternative: [OpenCore macrecovery](https://github.com/acidanthera/OpenCorePkg/tree/master/Utilities/macrecovery)
laedt Apple-Recovery-Material. Es ist kein fertiges Hyper-V-Tahoe-Installations-
image. Ohne nachgewiesene Tahoe-Auswahl und korrektes Image-Layout ist dies hier
kein Ersatz fuer den Vollinstaller-Weg. Keine erfundene Board-ID kopieren.

## 6a. Im Praxistest benutzter direkter Recovery-Weg unter Windows

Damit brauchst du fuer den Download keinen zweiten Mac und kein QEMU. Die
Apple-Dateien kommen auf eine vorbereitete EFI-Arbeitskopie. Das ist ein
alternativer Weg zu Schritt6, kein zusaetzlich benoetigtes Vollinstaller-Medium.

1. Den offiziellen Downloader aus festem
   [OpenCore-Commit78d5ff8](https://github.com/acidanthera/OpenCorePkg/tree/78d5ff824992d5b227f842e34d8221eb8f31baf1/Utilities/macrecovery)
   laden: macrecovery.py, boards.json und README.md.
2. In einem neuen lokalen Downloadordner ausfuehren:

   ```powershell
   py -3 .\macrecovery.py -b Mac-CFF7D910A743CAAF -m 00000000000000000 -os latest -o .\recovery download
   ```

3. **Image verification complete!** abwarten. Bei uns lieferte Apple die Recovery
   26.6.2/build25G83. Das ist nicht automatisch die endgueltig installierte Version.
   Downloadangebot kann sich aendern.
4. Vorbereitete eigene EFI-Kopie nur offline und keiner VM zugeordnet mounten.
   BaseSystem.dmg und BaseSystem.chunklist in `com.apple.recovery.boot` auf dem
   FAT32-Volume ablegen. Vorhandenes Recovery-Verzeichnis der Kopie vorher
   ausserhalb des Images sichern; keine Dateien einer laufenden EFI ersetzen.
5. `-nobsdmgroot` in dieser Installationskopie entfernen, falls aus dem alten
   Laborprofil vorhanden. HideAuxiliary=false und ShowPicker=true setzen.
   Eigenes SMBIOS und gepruefte Release-Core-Kext wie in Schritt7 vorbereiten.
6. EFI auf dem Host auswerfen. Neue VM wie in Schritt8 anlegen, aber nur zwei
   Platten: EFI/Recovery an0:0 und neue leere Systemplatte an0:1. Keine dritte
   Installer-VHDX erforderlich. Serial-Logger zuerst starten.
7. In OpenCore **EFI (dmg)** auswaehlen. Im Test erreichte dies unmittelbar
   **Reinstall macOS Tahoe**, ohne vorher Sequoia zu installieren.
8. Neue leere Zielplatte eindeutig nach Groesse und Host-Dateizuordnung erkennen,
   dann nur diese mit APFS/GPT initialisieren. Bei uns war dies disk2/429.5GB und
   der Volumename FullTest. Die Nummer ist fuer andere Versuche nicht garantiert.
9. **Reinstall macOS Tahoe > Continue**. Der Installer laedt die Installations-
   informationen online; deshalb ist Gast-Netzwerk erforderlich. Weitere Phasen
   werden erst nach tatsaechlicher Beobachtung als bestaetigt protokolliert.

## 7. EFI/OpenCore vorbereiten: der entscheidende Kontrollpunkt

Unser Maintainer-Paket enthaelt **keine startfertige EFI.vhdx und keine komplette
config.plist**. Es enthaelt Treiber, Patches und anonymisierte Einstellungsprofile.
Ein OpenCore-Download allein reicht deshalb nicht fuer einen startfaehigen Mac.

Fuer einen einfachen privaten Wiederaufbau benoetigst du eine separat
vorbereitete und gepruefte EFI-Arbeitskopie. Fuer eine neue VM braucht sie eine
eigene konsistente SMBIOS-Identitaet. Seriennummern/UUIDs nicht veroeffentlichen
oder gleichzeitig fuer mehrere Macs verwenden.

Ohne eine solche EFI muss dieser Teil zuerst fertiggestellt werden:

1. OpenCore-X64-Layout auf einem eigenen FAT32-EFI-Volume anlegen:

   ```text
   EFI/
     BOOT/BOOTx64.efi
     OC/OpenCore.efi
     OC/config.plist
     OC/ACPI/SSDT-HV-VMBUS.aml
     OC/ACPI/SSDT-HV-DEV.aml
     OC/ACPI/SSDT-HV-PLUG.aml
     OC/Drivers/OpenRuntime.efi
     OC/Drivers/[zum Profil passender HFS-Treiber]
     OC/Kexts/Lilu.kext/
     OC/Kexts/VirtualSMC.kext/
     OC/Kexts/MacHyperVSupportMonterey.kext/
   ```

2. OpenCore **Sample.plist derselben Version** als Ausgangspunkt benutzen;
   Hyper-V-Vorgaben aus dem oben verlinkten Upstream-README einarbeiten.
   Eine Sample.plist ist noch keine fertige Konfiguration.
3. ACPI-Quellen aus OpenCore verwenden; die Kommentare in
   [SSDT-HV-VMBUS.dsl](https://github.com/acidanthera/OpenCorePkg/blob/master/Docs/AcpiSamples/Source/SSDT-HV-VMBUS.dsl)
   enthalten zusaetzlich erforderliche ACPI-Patches. `.dsl` muss mit passendem
   `iasl` zu `.aml` kompiliert werden; blosses Umbenennen funktioniert nicht.
   [ACPICA Downloads](https://github.com/acpica/acpica/releases).
4. ProperTree fuer plist-Bearbeitung und Kext-Eintraege verwenden. Pruefen,
   dass alle benoetigten Kexts aktiviert sind; keine doppelten Core-Treiber.
5. Eigenes Tahoe-kompatibles Intel-SMBIOS nach OpenCore-Anleitung einrichten.
   Ein zufaelliger Modellname oder ein ARM-Modell ist kein Ersatz.
6. Mit `ocvalidate` aus **derselben OpenCore-Version** pruefen. Null Meldungen
   bedeutet Schema-Konsistenz, nicht nachgewiesene Bootfaehigkeit.
7. Image nur bei ausgeschalteter VM und abgehaengt bearbeiten. Danach auf dem
   Host auswerfen, Hash notieren und erst dann in Hyper-V anhaengen.

Wichtige Orientierung aus unserem getesteten Profil:

| Einstellung | Beobachtung / Anwendung |
| --- | --- |
| Kernel > Quirks > ProvideCurrentCpuInfo | true |
| UEFI > Quirks > DisableSecurityPolicy | Upstream-Hyper-V-Anforderung; in neuer EFI pruefen |
| Booter > Quirks > AvoidRuntimeDefrag / ProvideCustomSlide | Upstream-Hyper-V-Anforderungen |
| CPU-Spoof | Getesteter Intel-Host: Data 55060a00000000000000000000000000, Mask ffffffff000000000000000000000000; keine universelle CPU-Einstellung |
| ACPI-Reihenfolge | Upstream: VMBUS/DEV/PLUG; unser geerbtes Profil: DEV/PLUG/VMBUS. Neue Reihenfolge ist noch separat zu validieren |
| Core | MacHyperVSupportMonterey.kext, ab Darwin 21.0.0 |
| Framebuffer | Nicht per OpenCore injizieren; separat in /Library/Extensions |
| SIP | Bestehendes Profil hat csr-active-config 03000000; wurde bei uns nicht neu gesetzt. Kein pauschales Abschalten empfehlen |

**Kontrollpunkt B:** Gepruefte, eigene, bootfaehige EFI liegt vor. Wenn sie fehlt,
hier anhalten: Das ist eine reale fehlende Voraussetzung, kein Schritt, den ein
Anfaenger durch Raten ersetzen sollte. Das Projekt liefert diesen privaten
Bootdatentraeger derzeit nicht als oeffentliches Downloadpaket aus.

## 8. Neue VM im Hyper-V Manager anlegen

Diese Schritte beschreiben einen spaeteren Neuaufbau, keine Aenderung der aktuell
funktionierenden VM. Im Hyper-V Manager immer den vorgesehenen Namen pruefen.

Zum Wiederholen gibt es inzwischen auch `BuildScripts/new-tahoe-test-vm.ps1`.
Es bildet die im Praxistest manuell benutzten Hardwarebefehle ab, startet die VM
aber nicht. Standardmaessig zeigt es nur einen Plan; `-Create` erstellt explizit
eine neue VM. Existiert der Zielname oder eine Ausgabedatei bereits, bricht es ab.
Es ersetzt weder die EFI-Vorbereitung noch die Installation. Der Helfer ist
syntaktisch geprueft und hat die bereits laufende Test-VM vor jeder Aenderung
korrekt abgewiesen; der laufende Praxistest verwendete die Einzelbefehle.
Falls lokale Skriptrichtlinien die Ausfuehrung blockieren, diese nicht global
abschalten; die oben beschriebenen Manager-Schritte bleiben verfuegbar.

1. **New > Virtual Machine**.
2. Eindeutiger neuer Name, zum Beispiel **Tahoe-NewInstall**.
3. **Generation 2**.
4. **Startup memory: 24576 MB**; **Use Dynamic Memory** abwaehlen.
5. Vorhandenen vorgesehenen External-Switch auswaehlen. Bestehende Host-Switches
   nicht fuer diesen Versuch umbauen.
6. Neue System-VHDX mit **400 GB** erzeugen. Noch kein Betriebssystem starten.
7. **Settings > Processor: 8**.
8. **Settings > Security**: Unser bestehender Aufbau hat **Enable Secure Boot**
   nicht aktiviert. Bei einer neuen VM ist das eine bewusste VM-spezifische
   Voraussetzung, keine Aufforderung, Schutzfunktionen des Hosts auszuschalten.
9. Automatische Checkpoints fuer diesen Aufbau nicht benutzen.
10. Unter **SCSI Controller** drei getrennte Festplatten zuordnen:

    | Position | Datei |
    | --- | --- |
    | 0 | Eigene vorbereitete EFI.vhdx |
    | 1 | Neue leere System.vhdx, 400 GiB |
    | 2 | TahoeInstaller.vhdx |

11. **Firmware > Boot order**: EFI-Festplatte zuerst. Network Boot nicht davor.
12. Aufloesung zunaechst 1920x1080 entsprechend unserem beobachteten Profil;
    keine weitere Display-Optimierung im ersten Versuch.

**Kontrollpunkt C:** EFI, Installer und leere Systemplatte sind eindeutig
unterscheidbar. Keine Originalplatte oder Backup-Datei haengt als Installationsziel.

## 9. Serial-Logging vor dem Start einschalten

Hierfuer gibt es unser Host-Werkzeug
[capture-hyperv-serial.py](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/blob/maintainer/hyperv-release-delivery/BuildScripts/capture-hyperv-serial.py).
Es installiert nichts im Gast, veraendert keine VM und legt neue Logdateien an.
Jede VM benoetigt einen eigenen Pipe-Namen; nie einen zweiten Empfaenger auf
die bereits benutzte Pipe der laufenden Testmaschine setzen.

Fuer die **neue, noch ausgeschaltete** VM COM1 beispielsweise auf
`\\.\pipe\TahoeNewInstall` setzen. Nur im bewusst gewaehlten neuen VM-Kontext:

```powershell
Set-VMComPort -VMName 'Tahoe-NewInstall' -Number 1 -Path '\\.\pipe\TahoeNewInstall'
```

OpenCore-Bootargumente fuer die Installationsdiagnose:

```text
-v keepsyms=1 debug=0x12a serial=5 msgbuf=1048576 -hvgfxfbswcursor
```

Das ist ein vorgeschlagener Startsatz, nicht der byte-identische Bestandstest.
Unser getestetes Profil hat zusaetzliche Debug-Argumente und `-nobsdmgroot`.
**-nobsdmgroot nicht vorab in eine neue Installation uebernehmen:** Es war ein
gezielter Workaround fuer unseren zurueckgebliebenen Installer-Bootpfad.
**-hvstormsgdbg nicht hinzufuegen:** Es erzeugte bei uns extreme Paket-Logmengen.

In einem zweiten PowerShell-Fenster im Repository-Hauptordner:

```powershell
py -3 .\BuildScripts\capture-hyperv-serial.py --pipe '\\.\pipe\TahoeNewInstall' --output .\evidence\local-tests\new-install-serial-01
```

Fenster offen lassen. Fuer einen neuen Versuch einen neuen Ausgabeordner waehlen.
Bei **Connected** schreibt das Werkzeug. Es verbindet sich nach Gast-Neustarts
erneut. Ctrl+C beendet nur den Empfaenger, nicht die VM.

## 10. Tahoe direkt installieren

1. Erst jetzt **Start > Connect** fuer die neue VM.
2. OpenCore erscheint. Falls noetig Leertaste fuer ausgeblendete Eintraege.
3. **Install macOS Tahoe** vom vorbereiteten Installer waehlen.
4. Im Installer Sprache waehlen, dann **Disk Utility**.
5. **View > Show All Devices**. Ausschliesslich die neue 400-GiB-Systemplatte
   aus Schritt 8 identifizieren. EFI-/Installer-Disk nicht anfassen.
6. Nur diese **neue, leere Zielplatte** initialisieren: Name **Macintosh HD**,
   Format **APFS**, Scheme **GUID Partition Map**. Wenn Zuordnung oder Inhalt
   unklar sind, abbrechen. Dieser Schritt ist niemals fuer die laufende
   Projekt-VM oder erhaltene Platten gedacht.
7. Disk Utility schliessen; **Install macOS Tahoe** starten; **Macintosh HD**
   als Ziel waehlen.
8. Installation arbeiten lassen. Automatische Neustarts sind normal.
9. Nach Neustarts in OpenCore die begonnene Installation auf der Zielplatte
   fortsetzen; den **macOS Installer**-Eintrag waehlen, solange die Installation
   ihn benoetigt. Nicht jedes Mal die externe Erstinstallation neu beginnen.
10. Wenn die Installation abgeschlossen ist, **Macintosh HD** starten und
    Setup Assistant durchlaufen. **English** als Systemsprache waehlen, wenn
    du wie bei unserem System englische Oberflaeche willst. Tastaturlayout
    entsprechend der echten Tastatur einstellen.

Keine feste Minutenangabe ist zuverlaessig. Neue Serial-Ausgaben und wechselnde
Installationsphasen sind Fortschrittsindikatoren. Ein schwarzes VMConnect-Fenster
allein ist kein Grund zum Ausschalten. Bei FileVault/Anmeldung Passwort direkt
in der VM eingeben; das wird durch Serial-Logging nicht automatisiert.

## 11. Ersten Desktop pruefen

Terminal oeffnen und einzeln eingeben:

```sh
sw_vers
kextstat -b fish.goldfish64.MacHyperVSupport
```

Bei unserem Referenzbuild zeigt sw_vers **26.7.1 / 25G241**. Der Bundle-Identifier
des Monterey-Core heisst trotzdem **fish.goldfish64.MacHyperVSupport**, ohne
Monterey am Ende. Erwartete geladene Release-Core-UUID:

```text
7CAF03F1-3631-33A9-AAAF-581270B665B0
```

Netzwerk, Finder und Tastatur ausprobieren. Noch keine anderen Erweiterungen
oder Optimierungen installieren; erst Grundfunktion nachweisen.

## 12. Release-Framebuffer installieren: Erstinstallation separat behandeln

Die Core-Kext auf der EFI ersetzt **nicht** den Framebuffer im Gast.
Unser erfolgreicher Release-Framebuffer liegt in
`/Library/Extensions/MacHyperVFramebuffer.kext` und wird ueber die Auxiliary
Kernel Collection geladen. Software-Cursor benoetigt `-hvgfxfbswcursor`.

Der mitgelieferte **InstallAux-example.command** ist **kein universeller
Erstinstaller**. Er verlangt absichtlich den bisherigen Debug-Framebuffer,
Build25G241 und genau vier bereits vorhandene Aux-Module. Eine frische
Installation erfuellt diese Voraussetzungen typischerweise nicht. Seine
Pruefungen nicht entfernen, um ihn zum Laufen zu zwingen.

Fuer eine frische Installation muss der technische Installationsschritt deshalb
zuerst an deren echten Zustand angepasst und getestet werden:

1. Vorhandene Kexts, Aux-Module, Boot/System-Collections und Sicherheitszustand
   erfassen. Aktuelle Daten und EFI auf eigenen Rueckfallkopien sichern.
2. Passendes Apple-signiertes KDK bereitstellen, falls die lokalen Werkzeuge es
   brauchen. Unser Test hatte das KDK25G241 installiert; ohne KDK wurde der
   erfolgreiche Aux-Weg nicht gegengeprueft.
3. Release-Bundle und erwarteten Hash pruefen; Dateirechte root:wheel,
   Ordner755, Dateien644, ausfuehrbare Datei755 korrekt setzen.
4. Eine private neue Aux-Collection mit dem tatsaechlichen Modulbestand bauen;
   alle bestehenden anderen Module erhalten. Unsere vier Testpfade sind keine
   allgemeingueltige Liste fuer einen neuen Mac.
5. Erst nach erfolgreichen Checks die gesicherten Aux-Ausgaben aktualisieren
   und den passenden Apple-Staging-Schritt ausfuehren. Boot/System-Collections
   unveraendert lassen. Bei Fehlern zurueckrollen und nicht neu starten.
6. Wenn macOS **New system extensions require a restart** meldet, erst den
   erfolgreichen Installer-Abschluss pruefen, dann normal neu starten.

Details: [Cursor-/Aux-Verfahren](CURSOR_WORKAROUND.md) und
[Release-Protokoll](RELEASE_RC1.md). Fuer einen vollstaendig anfaengertauglichen
Neuinstallationssatz fehlt hier noch ein validierter Erstinstaller. Nicht durch
blindes `kmutil install --update-all`, EFI-Framebuffer-Injektion oder pauschales
Abschalten von Sicherheitsfunktionen ersetzen.

Nach dem korrekten Installationsschritt und Neustart:

```sh
kextstat -b fish.goldfish64.MacHyperVFramebuffer
shasum -a 256 /Library/Extensions/MacHyperVFramebuffer.kext/Contents/MacOS/MacHyperVFramebuffer
```

Erwartete Release-UUID: `3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6`.
Erwarteter SHA256:

```text
d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122
```

## 13. Unser Werkzeugkasten: was macht welches Tool?

| Werkzeug | Zweck | Veraendert es den Gast? |
| --- | --- | --- |
| capture-hyperv-serial.py | Explizit ausgewaehlte COM1-Pipe mitschneiden | Nein |
| snapshot-serial-log.py | Unveraenderlichen Log-Prefix samt Hash/Markerzaehlern sichern | Nein |
| collect-hyperv-profile.ps1 | VM-Einstellungen gezielt und anonymisiert erfassen | Nein |
| new-tahoe-test-vm.ps1 | Neuen VM-Aufbau planen; mit -Create ausschliesslich neue VM/Dateien anlegen | Neue VM wird angelegt und bleibt Off |
| inspect-fresh-tahoe.command | Nach Erststart Version, Treiber und Aux-Bestand in neuem lokalen Bericht erfassen | Nur neues Berichtsverzeichnis; keine Treiber-/Sicherheitsaenderung |
| summarize-efi-profile.py | Gespeicherte EFI-Konfiguration zusammenfassen | Nein; keine Live-VHDX bearbeiten |
| verify-ci-delivery.py | Download gegen originale CI-Provenance pruefen | Nein |
| export-hyperv-maintainer.py | Gepruefte Patches/Binaries/Dokumente verpacken | Nein; benoetigt lokale archivierte Build-Eingaben |
| InstallAux-example.command | Bewachter Gast-spezifischer Framebuffer-/Aux-Austausch | Ja; nur bei exakt passenden Vorbedingungen |

Werkzeughilfe:

```powershell
py -3 .\BuildScripts\capture-hyperv-serial.py --help
py -3 .\BuildScripts\snapshot-serial-log.py --help
py -3 .\BuildScripts\verify-ci-delivery.py --help
```

Log-Prefix sichern: INPUT.log durch die wirkliche aktuelle Logdatei ersetzen:

```powershell
py -3 .\BuildScripts\snapshot-serial-log.py --input .\evidence\local-tests\new-install-serial-01\INPUT.log --output .\evidence\local-tests\new-install-check-01
```

Windows kann fuer offene Logdateien eine veraltete Groesse anzeigen. Unser
Snapshot-Werkzeug liest die wirkliche Dateigroesse am offenen Handle.
Im clean Release gibt es keine per-call EOM-CPU-Messzeilen: Null Messzeilen
bedeuten keine neue CPU-Zuordnungspruefung. Leeres Log ist kein Erfolg.

## 14. Wann ist die Installation wirklich fertig?

Abhaken und Datum/Build/Hashes notieren:

- [ ] sw_vers zeigt die beabsichtigte Tahoe-Version.
- [ ] Core- und Framebuffer-UUID stimmen mit dem ausgesuchten Release ueberein.
- [ ] Der normale Desktop erscheint; keine Recovery-/Installer-Schleife.
- [ ] Tastatur, Maus und Klick-Fokus funktionieren.
- [ ] Cursor bleibt beim Oeffnen von Finder/Downloads und Safari sichtbar.
- [ ] Netzwerk und normale Dateioperationen funktionieren.
- [ ] Normaler macOS-Neustart und erneute lokale Anmeldung funktionieren.
- [ ] Laengere Sitzung und mehrere Starts sind separat protokolliert.
- [ ] Serial-Log und Rueckfallkopien sind gesichert.

Nach erfolgreicher Installation das Installer-Medium auswerfen/abhaengen.
Die **EFI-Festplatte bleibt** notwendig. Erst nach verifiziertem Rueckfallweg
temporaere Kopien loeschen. Niemals alle VHDX-Dateien als vermeintlichen Muell
behandeln. Vorhandene Backups nicht ueberschreiben.

## 15. Wenn etwas nicht funktioniert

| Beobachtung | Naechster Schritt |
| --- | --- |
| Reinstall macOS Sequoia | Falsche Recovery; nicht installieren, Tahoe-Medium pruefen |
| PXE / Network Boot | EFI als erstes Firmware-Bootziel pruefen |
| Schwarzes Fenster | VMConnect neu verbinden, VM-Zustand und wirklichen Serial-Prefix pruefen; kein blinder Reset |
| FileVault-/Passwortbildschirm | Passwort lokal eingeben; keine Shellbefehle in das Passwortfeld |
| VM geht nach einigen Minuten vor Kernel-Output aus | Ereignisse und Vorstart-Anmeldung pruefen; bei uns blieb die Timeout-Ursache unbewiesen |
| Still waiting for root device | Core-Build/Hash, VMBus-/SCSI-Enumeration und Disk-Zuordnung pruefen; Logs erhalten |
| Cursor verschwindet | Geladenen Release-Framebuffer und -hvgfxfbswcursor pruefen |
| Neue Erweiterung braucht Neustart | Erfolgsmarker/Hashes pruefen, dann regulaer aus macOS neu starten |
| kmutil meldet Fehler | Kein Neustart auf halbfertiger Collection; Rollback und exakten Fehler sichern |
| Host-Shutdown scheitert | Normalen macOS-Menueweg benutzen; Restart-VM ist kein Ersatz fuer einen sauberen Gast-Neustart |

## Quellen und genaue Grenzen

Links geprueft am25.10.2026; Downloads und Apple-Angebot koennen sich aendern.
Apple dokumentiert Installererstellung fuer Macs, keine Hyper-V-Unterstuetzung.
Die Uebertragung auf Hyper-V ist Projektarbeit und muss als Ganzes validiert
werden. QEMU dokumentiert Offline-Konvertierung; Upstream MacHyperVSupport
beschreibt Hyper-V-OpenCore und DMG/VHDX-Grundlagen. Unsere lokalen Profile und
Testberichte sind die Quelle fuer die konkreten Referenzwerte und Hashes.

Die zwei offenen Lieferteile fuer einen komplett vorbereiteten Neuinstallations-
Satz sind: eine separat gepruefte, identitaetsbereinigte EFI-Vorlage samt
personalisierbarer Konfiguration und ein validierter Framebuffer-Erstinstaller.
Diese Anleitung behauptet nicht, dass sie schon im Maintainer-Paket liegen.
