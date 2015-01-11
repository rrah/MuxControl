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
        "enabled": "False",
        "type": "Mux",
        "host": "mux.ystv",
        "port": "2000",
        "labels": {
          "input": [
            {
              "num": "1",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "2",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "3",
              "label": "Camera 1",
              "enabled": "True"
            },
            {
              "num": "4",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "5",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "6",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "7",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "8",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "9",
              "label": "Camera 2",
              "enabled": "True"
            },
            {
              "num": "10",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "11",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "12",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "13",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "14",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "15",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "16",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "17",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "18",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "19",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "20",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "21",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "22",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "23",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "24",
              "label": "Camera 3",
              "enabled": "True"
            },
            {
              "num": "25",
              "label": "Camera 4",
              "enabled": "True"
            },
            {
              "num": "26",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "27",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "28",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "29",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "30",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "31",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "32",
              "label": "Unused",
              "enabled": "False"
            }
          ],
          "output": [
            {
              "num": "1",
              "label": "DaVE 1",
              "enabled": "True"
            },
            {
              "num": "2",
              "label": "DaVE 2",
              "enabled": "True"
            },
            {
              "num": "3",
              "label": "DaVE 3",
              "enabled": "True"
            },
            {
              "num": "4",
              "label": "DaVE 4",
              "enabled": "True"
            }
          ]
        }
      },
      "trans": {
        "enabled": "False",
        "type": "Transmission Light",
        "host": "trans.ystv",
        "port": "2000"
      },
      "tarantula": {
        "enabled": "False",
        "type": "Tarantula",
        "host": "tarantula.ystv",
        "port": "9815"
      },
      "hub": {
        "enabled": true,
        "type": "Videohub",
        "host": "192.168.1.1",
        "port": "9990",
        "labels": {
          "input": [
            {
              "num": 0,
              "label": "Patch 81",
              "enabled": "True"
            },
            {
              "num": 1,
              "label": "Patch 82",
              "enabled": "True"
            },
            {
              "num": 2,
              "label": "Patch 83",
              "enabled": "True"
            },
            {
              "num": 3,
              "label": "Patch 91",
              "enabled": "True"
            },
            {
              "num": 4,
              "label": "Patch 92",
              "enabled": "True"
            },
            {
              "num": 5,
              "label": "Patch 93",
              "enabled": "True"
            },
            {
              "num": 6,
              "label": "Strmre",
              "enabled": "True"
            },
            {
              "num": 7,
              "label": "Vidsrv",
              "enabled": "True"
            },
            {
              "num": 8,
              "label": "Program",
              "enabled": "True"
            },
            {
              "num": 9,
              "label": "Preview",
              "enabled": "True"
            },
            {
              "num": 10,
              "label": "Multiview",
              "enabled": "True"
            },
            {
              "num": 11,
              "label": "Aux 1",
              "enabled": "True"
            },
            {
              "num": 12,
              "label": "Aux 2",
              "enabled": "True"
            },
            {
              "num": 13,
              "label": "Aux 3",
              "enabled": "True"
            },
            {
              "num": 14,
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": 15,
              "label": "PiVT",
              "enabled": "True"
            }
          ],
          "output": [
            {
              "num": "1",
              "label": "ATEM Input 1",
              "enabled": "True"
            },
            {
              "num": "2",
              "label": "ATEM Input 2",
              "enabled": "True"
            },
            {
              "num": "3",
              "label": "ATEM Input 3",
              "enabled": "True"
            },
            {
              "num": "4",
              "label": "ATEM Input 4",
              "enabled": "True"
            },
            {
              "num": "5",
              "label": "ATEM Monitor 1",
              "enabled": "True"
            },
            {
              "num": "6",
              "label": "ATEM Monitor 2",
              "enabled": "True"
            },
            {
              "num": "7",
              "label": "ATEM Monitor 3",
              "enabled": "True"
            },
            {
              "num": "8",
              "label": "ATEM Monitor 4",
              "enabled": "True"
            },
            {
              "num": "9",
              "label": "Program Monitor",
              "enabled": "True"
            },
            {
              "num": "10",
              "label": "Program Monitor 2",
              "enabled": "True"
            },
            {
              "num": "11",
              "label": "Vidsrv",
              "enabled": "True"
            },
            {
              "num": "12",
              "label": "Vision Mixer",
              "enabled": "True"
            },
            {
              "num": "13",
              "label": "Graphics Monitor",
              "enabled": "True"
            },
            {
              "num": "14",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "15",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "16",
              "label": "Stream",
              "enabled": "True"
            }
          ]
        }
      },
      "tally": {
        "enabled": "False",
        "type": "Tally",
        "host": "tally.ystv",
        "port": "2000"
      },
      "vik": {
        "enabled": "False",
        "type": "V1616",
        "host": "192.168.1.2",
        "port": "2001",
        "labels": {
          "input": [
            {
              "num": "1",
              "label": "Cam 1",
              "enabled": "True"
            },
            {
              "num": "2",
              "label": "Cam 2",
              "enabled": "True"
            },
            {
              "num": "3",
              "label": "Cam 3",
              "enabled": "True"
            },
            {
              "num": "4",
              "label": "Cam 4",
              "enabled": "True"
            },
            {
              "num": "5",
              "label": "Cam 5",
              "enabled": "True"
            },
            {
              "num": "6",
              "label": "Cam 6",
              "enabled": "True"
            },
            {
              "num": "7",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "8",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "9",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "10",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "11",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "12",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "13",
              "label": "Multiview",
              "enabled": "True"
            },
            {
              "num": "14",
              "label": "Preview",
              "enabled": "True"
            },
            {
              "num": "15",
              "label": "Program",
              "enabled": "True"
            },
            {
              "num": "16",
              "label": "GFX",
              "enabled": "True"
            }
          ],
          "output": [
            {
              "num": "1",
              "label": "DaVE 1",
              "enabled": "True"
            },
            {
              "num": "2",
              "label": "DaVE 2",
              "enabled": "True"
            },
            {
              "num": "3",
              "label": "DaVE 3",
              "enabled": "True"
            },
            {
              "num": "4",
              "label": "DaVE 4",
              "enabled": "True"
            },
            {
              "num": "5",
              "label": "Multi 1",
              "enabled": "True"
            },
            {
              "num": "6",
              "label": "Multi 2",
              "enabled": "True"
            },
            {
              "num": "7",
              "label": "Multi 3",
              "enabled": "True"
            },
            {
              "num": "8",
              "label": "Multi 4",
              "enabled": "True"
            },
            {
              "num": "9",
              "label": "Program Monitor",
              "enabled": "True"
            },
            {
              "num": "10",
              "label": "Program Monitor 2",
              "enabled": "True"
            },
            {
              "num": "11",
              "label": "Multiview Monitor",
              "enabled": "True"
            },
            {
              "num": "12",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "13",
              "label": "Unused",
              "enabled": "False"
            },
            {
              "num": "14",
              "label": "Corio",
              "enabled": "True"
            },
            {
              "num": "15",
              "label": "Recording",
              "enabled": "True"
            },
            {
              "num": "16",
              "label": "Stream",
              "enabled": "True"
            }
          ]
        }
      },
      "casparcg": {
        "enabled": "False",
        "type": "CasparCG",
        "host": "192.168.1.3",
        "port": "5250"
      }
    },
    "panels": {
      "getstarted": {
        "enabled": "False",
        "label": "Get Started"
      },
      "directorpanel": {
        "enabled": "False",
        "label": "Director Panel"
      },
      "hub": {
        "enabled": "True",
        "label": "Hub Control"
      },
      "mux": {
        "enabled": "False",
        "label": "Mux Control"
      },
      "trans": {
        "enabled": "False",
        "label": "Transmission Light"
      },
      "tarantula": {
        "enabled": "True",
        "label": "Tarantula Control"
      },
      "vik": {
        "enabled": "True",
        "label": "V1616 Control"
      },
      "caspar": {
        "enabled": "False",
        "label": "Graphics"
      }
    }
}
"""