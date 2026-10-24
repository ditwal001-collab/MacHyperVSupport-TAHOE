# Resume after restarting Codex

The functional commit `670b352156c0cdd044e9f211577741c1d0f7dfcc` was pushed
to `tahoe/fix/synic-eom-cpu-affinity`. Subsequent source and CI corrections are
committed and pushed through `0756f1d`; documentation/export work remains local.
Read CODEX_HANDOFF.md for current build conclusions. Do not reset or clean the
working tree. Targeted Git/network escalation works again after restart.

A fresh maintainer export and a local restart snapshot were created under
`evidence/packages/` before restart. The restart snapshot includes tracked and
non-ignored untracked files, including the exporter and existing scratch files.
It excludes Git metadata, ignored build outputs and previous package archives.
It is a local recovery copy, not a package for publication. The repository and
its `.git` directory remain in their original location.

From a new PowerShell terminal:

```powershell
Set-Location 'C:\DATA\VM\REPO\MacHyperVSupport-TAHOE\SOURCE'
codex --sandbox workspace-write --ask-for-approval on-request resume --last
```

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
Keine VM-, VHDX- oder Backup-Änderungen ohne meine ausdrückliche Freigabe.
Melde einen Blocker sofort und sage klar, ob du angehalten hast.
```

Approval mode permits targeted requests; it does not grant every operation
automatically. Persist only appropriately scoped command rules when offered.
Do not stage existing `.bak` files or generated package archives.
