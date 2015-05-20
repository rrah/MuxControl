
MuxControl
==========

GUI for controlling various devices around YSTV

<h2> Currently supported and tested devices </h2>
- Vikinx V1616
- BMD Micro Videohub


<h2> Notes  </h2>
Only supported for wxpython2.9 and later.

<h3> Known issues </h3>
- Segfaults at any wizards if using wxpython2.8 under Linux. Use wxpython2.9 or later instead.
- Labels on buttons don't wrap.
- Tally doesn't have default settings for settings dialog
- V1616 sometimes gets confused and needs its buffer clearing. Normally when MuxControl has error'd out
