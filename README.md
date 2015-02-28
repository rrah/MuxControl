
MuxControl
==========

GUI for controlling various devices around YSTV

*** Currently supported and tested devices ***
- Vikinx V1616
- BMD Micro Videohub


*** Note  ***
Only supported for wxpython2.9 and later.

*** Known issues ***
- Segfaults at any wizards if using wxpython2.8 under Linux. Use wxpython2.9 or later instead.
- Labels on buttons don't wrap.
- Tally doesn't have default settings for settings dialog
- V1616 sometimes gets confused and needs its buffer clearing. Normally when MuxControl has error'd out
