Python script that compiles a formatted JSON file to a Danmakufu shot definition script.

## Usage ##

```
python shotcompile.py [input] [output]
```

Takes an optional input and output argument, defaulted to `shots.json` and `shots.dnh`.

## Format ##

File must be valid JSON, although comments are stripped so those are fine.

**shot_image**: String containing the same path to the file you'd usually put in. (e.g. `"./etama01.png"`)

**delay_rect**: Array containing the same rect you'd usually put in. (e.g. `[2,478,34,510]`)

**delay_color**: Array containing the same color as usual. (e.g. `[128,128,128]`)

**colors**: Object containing the colors present in the shot sheet. Keys can be arbitrary strings and values are arrays containing that color. (e.g. `"red": [255,0,0]`)

**shots**: Array of objects containing the main shot data. Each object represents a group of one shot type and assumes the group of shots only differ in where their rects are positioned.


#### Shot Groups ####

The format for each shot group object is as follows:

**origin**: An array containing the starting `(x,y)` position for the group of shots. (e.g. `[0,0]`)

**size**: An array containing the width and height of the shots. (e.g. `[12,12]`)

**off**: An array containing the `(x,y)` offset between the rects of each shot. (e.g. `[16,0]`)

**colors**: An array of strings corresponding to each individual shot's color. Only colors defined in the "global" `colors` object are recognized. The length of this array determines how many shots are defined. (e.g. `["red","green","blue"]`)

**animation** (optional): An array of size 4, where the first two elements are the `(x,y)` offset between the rects of each animation frame, the third element is the number of frames in the animation, and the fourth is the duration of each frame. The `off` key can be omitted if this key is present (for single animated shots). (e.g. `[16,0,5,4]`)

**collision** (optional): If set to a number, is the radius of each shot's hitbox. If set to an array of size 3, the elements are the radius and `(x,y)` offset of the hitbox. If set to an array of these arrays, multiple hitboxes are given. (e.g. `8`, `[8,0,-2]`, `[[4,0,-2],[4,0,2]]`)

**fixed_angle** (optional): Set to `true` if the shot graphic remains fixed, `false` if it rotates according to movement angle.

**angular_velocity** (optional): If set to a number, is the number of degrees the graphic rotates per frame. If set to an array of size 2, the velocity is randomized between the two numbers (i.e. `[-4,4] -> rand(-4,4)`).

**render** (optional): A string describing the blend type used for the shot group. Valid types are `"ALPHA"`,`"ADD"`,`"ADD_RGB"`,`"ADD_ARGB"`,`"MULTIPLY"`, `"SUBTRACT"`, `"INV_DESTRGB"`.

**delay_rect** (optional): Array containing the rect for the delay graphic, overriding the global one.

**delay_color** (optional): Array containing the color for the delay graphic, overriding the global one.

**delay_render** (optional): A string describing the blend type used for the delay graphic. Valid types are as above.



### Example ###

See [shots.json](shots.json) for a more complete sample file that makes use of most options.

```json
{
	"shot_image": "./etama01.png",
	"delay_rect": [2,478,34,510],
	"shots": [
		{
			"origin": [4,4],
			"size": [8,8],
			"off": [10,0],
			"collision": 4,
			"colors": ["red","yellow","green","blue"]
		},
		{
			"origin": [4,14],
			"size": [8,8],
			"off": [10,0],
			"collision": 4,
			"fixed_angle": true,
			"colors": ["red","yellow","green","blue"]
		}
	],
	"colors": {
		"red": [255,0,0],
		"yellow": [255,255,0],
		"green": [0,255,0],
		"blue": [0,0,255]
	}
}
```