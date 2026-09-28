# WD 1 TB on this Mini (after APFS conversion)

Not ExFAT `Elements` anymore.

One APFS container, two volumes sharing the 1 TB:

- `/Volumes/Arquivo` — cold files (CURADORIA, Dados, regi, …)
- `/Volumes/Time Machine` — `diskutil apfs addVolume … APFS "Time Machine" -role T`

`tmutil setdestination` needs admin; user adds the **Time Machine** volume in System Settings (not Arquivo). Never TM on `/Volumes/Trabalho`.

ExFAT → APFS: copy with a walk that skips `OSError` (ghost iCloud/Windows paths); `ditto`/`rsync` abort on the first miss. Staging on Trabalho, erase WD, copy back, then delete staging.
