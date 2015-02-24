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
      "mux": {
        "enabled": false,
        "type": "Mux",
        "host": "mux.ystv",
        "port": 2000,
        "labels": {
          "input": [
            {
              "num": 0,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 1,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 2,
              "label": "Camera 1",
              "enabled": true
            },
            {
              "num": 3,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 4,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 5,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 6,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 7,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 8,
              "label": "Camera 2",
              "enabled": true
            },
            {
              "num": 9,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 10,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 11,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 12,
              "label": "Unused",
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
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 16,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 17,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 18,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 19,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 20,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 21,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 22,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 23,
              "label": "Camera 3",
              "enabled": true
            },
            {
              "num": 24,
              "label": "Camera 4",
              "enabled": true
            },
            {
              "num": 25,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 26,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 27,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 28,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 29,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 30,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 31,
              "label": "Unused",
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
            }
          ]
        }
      },
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
        "port": 2000
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
              "label": "Multiview Monitor",
              "enabled": true
            },
            {
              "num": 11,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 12,
              "label": "Unused",
              "enabled": true
            },
            {
              "num": 13,
              "label": "Corio",
              "enabled": true
            },
            {
              "num": 14,
              "label": "Recording",
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