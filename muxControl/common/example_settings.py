#-------------------------------------------------------------------------------
# Name:        example_settings
# Purpose:      Hold the default settings for things
#
# Author:      Robert Walker
#
# Created:     11/01/2015
#-------------------------------------------------------------------------------

example = """
{
	"__root__": true,
	"first_run": true,
    "devices": {
      "trans": {
        "enabled": false,
        "type": "Transmission Light",
        "host": "trans.ystv",
        "port": 2000
      },
      "tarantula": {
        "enabled": false,
        "type": "Tarantula",
        "host": "tarantula.ystv",
        "port": 9815
      },
      "hub": {
        "enabled": false,
        "type": "Videohub",
        "host": "192.168.1.1",
        "port": 9990,
        "labels": {
          "input": [
            {
              "num": 0,
              "label": "Patch 81",
              "enabled": true
            },
            {
              "num": 1,
              "label": "Patch 82",
              "enabled": true
            },
            {
              "num": 2,
              "label": "Patch 83",
              "enabled": true
            },
            {
              "num": 3,
              "label": "Patch 91",
              "enabled": true
            },
            {
              "num": 4,
              "label": "Patch 92",
              "enabled": true
            },
            {
              "num": 5,
              "label": "Patch 93",
              "enabled": true
            },
            {
              "num": 6,
              "label": "Strmre",
              "enabled": true
            },
            {
              "num": 7,
              "label": "Vidsrv",
              "enabled": true
            },
            {
              "num": 8,
              "label": "Program",
              "enabled": true
            },
            {
              "num": 9,
              "label": "Preview",
              "enabled": true
            },
            {
              "num": 10,
              "label": "Multiview",
              "enabled": true
            },
            {
              "num": 11,
              "label": "Aux 1",
              "enabled": true
            },
            {
              "num": 12,
              "label": "Aux 2",
              "enabled": true
            },
            {
              "num": 13,
              "label": "Aux 3",
              "enabled": true
            },
            {
              "num": 14,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 15,
              "label": "PiVT",
              "enabled": true
            }
          ],
          "output": [
            {
              "num": 0,
              "label": "ATEM Input 1",
              "enabled": true
            },
            {
              "num": 1,
              "label": "ATEM Input 2",
              "enabled": true
            },
            {
              "num": 2,
              "label": "ATEM Input 3",
              "enabled": true
            },
            {
              "num": 3,
              "label": "ATEM Input 4",
              "enabled": true
            },
            {
              "num": 4,
              "label": "ATEM Monitor 1",
              "enabled": true
            },
            {
              "num": 5,
              "label": "ATEM Monitor 2",
              "enabled": true
            },
            {
              "num": 6,
              "label": "ATEM Monitor 3",
              "enabled": true
            },
            {
              "num": 7,
              "label": "ATEM Monitor 4",
              "enabled": true
            },
            {
              "num": 8,
              "label": "Program Monitor",
              "enabled": true
            },
            {
              "num": 9,
              "label": "Program Monitor 2",
              "enabled": true
            },
            {
              "num": 10,
              "label": "Vidsrv",
              "enabled": true
            },
            {
              "num": 11,
              "label": "Vision Mixer",
              "enabled": true
            },
            {
              "num": 12,
              "label": "Graphics Monitor",
              "enabled": true
            },
            {
              "num": 13,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 14,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 15,
              "label": "Stream",
              "enabled": true
            }
          ]
        }
      },
      "tally": {
        "enabled": false,
        "type": "Tally",
        "host": "tally.ystv",
        "port": 2000,
        "map": []
      },
      "vik": {
        "enabled": false,
        "type": "V1616",
        "host": "192.168.1.2",
        "port": 2001,
        "labels": {
          "input": [
            {
              "num": 0,
              "label": "Cam 1 Prime",
              "enabled": true
            },
            {
              "num": 1,
              "label": "Cam 1 Sec",
              "enabled": true
            },
            {
              "num": 2,
              "label": "Cam 2 Prime",
              "enabled": true
            },
            {
              "num": 3,
              "label": "Cam 2 Sec",
              "enabled": true
            },
            {
              "num": 4,
              "label": "Cam 3 Prime",
              "enabled": true
            },
            {
              "num": 5,
              "label": "Cam 3 Sec",
              "enabled": true
            },
            {
              "num": 6,
              "label": "Cam 4 Prime",
              "enabled": true
            },
            {
              "num": 7,
              "label": "Cam 4 Sec",
              "enabled": true
            },
            {
              "num": 8,
              "label": "Cam 5 Prime",
              "enabled": true
            },
            {
              "num": 9,
              "label": "Cam 5 Sec",
              "enabled": true
            },
            {
              "num": 10,
              "label": "Cam 6 Prime",
              "enabled": true
            },
            {
              "num": 11,
              "label": "Cam 6 Sec",
              "enabled": true
            },
            {
              "num": 12,
              "label": "VT",
              "enabled": true
            },
            {
              "num": 13,
              "label": "DaVE Prog",
              "enabled": true
            },
            {
              "num": 14,
              "label": "GFX Prog",
              "enabled": true
            },
            {
              "num": 15,
              "label": "Multiview",
              "enabled": true
            }
          ],
          "output": [
            {
              "num": 0,
              "label": "DaVE 1",
              "enabled": true
            },
            {
              "num": 1,
              "label": "DaVE 2",
              "enabled": true
            },
            {
              "num": 2,
              "label": "DaVE 3",
              "enabled": true
            },
            {
              "num": 3,
              "label": "DaVE 4",
              "enabled": true
            },
            {
              "num": 4,
              "label": "Multi 1",
              "enabled": true
            },
            {
              "num": 5,
              "label": "Multi 2",
              "enabled": true
            },
            {
              "num": 6,
              "label": "Multi 3",
              "enabled": true
            },
            {
              "num": 7,
              "label": "Multi 4",
              "enabled": true
            },
            {
              "num": 8,
              "label": "Multi 5",
              "enabled": true
            },
            {
              "num": 9,
              "label": "Multi 6",
              "enabled": true
            },
            {
              "num": 10,
              "label": "Multi 7",
              "enabled": true
            },
            {
              "num": 11,
              "label": "Multi 8",
              "enabled": true
            },
            {
              "num": 12,
              "label": "Clean rec",
              "enabled": true
            },
            {
              "num": 13,
              "label": "Multi Patch",
              "enabled": true
            },
            {
              "num": 14,
              "label": "Corio",
              "enabled": true
            },
            {
              "num": 15,
              "label": "Stream",
              "enabled": true
            }
          ]
        }
      },
      "casparcg": {
        "enabled": false,
        "type": "CasparCG",
        "host": "192.168.1.3",
        "port": 5250
      }
    }
}
"""