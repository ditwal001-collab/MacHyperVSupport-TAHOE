# Resume after restarting Codex

The functional candidate with compile follow-ups is `0756f1d`, successfully built
and observed at a live normal Tahoe login screen on test copies. Read
TAHOE_BOOT_RESULT.md and UNATTENDED.md for exact inputs and limitations, then
inspect actual Git status/history. Do not reset/clean the working tree or the
ignored directory containing attached VM disk images. Automatic approval review
works in the current session; existing target-VM authorization is documented.

A fresh maintainer export and a local restart snapshot were created under
`evidence/packages/` before restart. The restart snapshot includes tracked and
non-ignored untracked files, including the exporter and existing scratch files.
It excludes Git metadata, ignored build outputs and previous package archives.
It is a local recovery copy, not a package for publication. The repository and
its `.git` directory remain in their original location.

From a new PowerShell terminal:

```powershell
Set-Location 'C:\DATA\VM\REPO\MacHyperVSupport-TAHOE\SOURCE'
codex.cmd resume --last --approve-for-me
```

Do not combine --approve-for-me with -a/--ask-for-approval: the installed CLI
rejects that combination. The .cmd entrypoint avoids the host's unsigned .ps1
execution-policy problem without changing the policy. Automatic review is active
in the current session and is not unrestricted approval of every possible action.
Read UNATTENDED.md and TAHOE_BOOT_RESULT.md for the latest running-copy state.

If the resumed session retains the old managed permissions, do not change
Windows ACLs or disable protections. Inspect `/status` and the active permission
settings, or start a fresh session in this directory with the same flags and
the following prompt:

```text
Setze die Entwicklung des SynIC-EOM-Fixes fort. Lies zuerst AGENTS.md,
CODEX_HANDOFF.md und Docs/handoff/RESTART.md sowie die dort verlinkten Berichte.
Erhalte alle uncommitted Änderungen und vorhandenen Backups. Prüfe Branch,
Git-Status und den neuesten Actions-Lauf aus CODEX_HANDOFF.md. Halte
Quellcode, CI und Dokumentation in getrennten Commits und führe den Build-Zyklus fort.
Ausschliesslich die autorisierte Test-VM srv-maos-devs11 bearbeiten; vorhandene
Backups erhalten. Keine Loeschung/Formatierung oder andere VM bearbeiten.
Lies UNATTENDED.md und TAHOE_BOOT_RESULT.md zuerst. Keine Rueckfragen oder
Aufforderung zu weiter; bei laufender Installation warten. Serial-Logging
pruefen. Nicht auf Originalplatten zurueckschreiben. Blocker sofort dokumentieren.
```

Automatic review can still reject actions; do not bypass security boundaries.
Do not stage existing `.bak` files or generated package archives.
