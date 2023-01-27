from enum import Enum

from components.components import Directions


class Characters(Enum):
	SMILEY = chr(0x263A)
	FILLED_SMILEY = chr(0x263B)
	HEART = chr(0x2665)
	DIAMOND = chr(0x2666)

	BULLET = chr(0x2022)

	RIGHT_POINTING_TRIANGLE = chr(0x25BA)
	LEFT_POINTING_TRIANGLE =chr(0x25C4)
	UP_POINTING_TRIANGLE = chr(0x25B2)
	DOWN_POINTING_TRIANGLE = chr(0x25BC)

	LOWER_HALF_BLOCK = chr(0x2584)
	LEFT_HALF_BLOCK = chr(0x258C)
	RIGHT_HALF_BLOCK = chr(0x2590)
	UPPER_HALF_BLOCK = chr(0x2580)
	RECTANGLE = chr(0x25AC)


	LIGHT_SHADE = chr(0x2591)
	MEDIUM_SHADE = chr(0x2592)


CHARACTER_MAPPINGS = {
    "triangles": [
        Characters.UP_POINTING_TRIANGLE.value,
        Characters.RIGHT_POINTING_TRIANGLE.value,
        Characters.DOWN_POINTING_TRIANGLE.value,
        Characters.LEFT_POINTING_TRIANGLE.value,
    ],

    "bars": [
        Characters.LOWER_HALF_BLOCK.value,
        Characters.LEFT_HALF_BLOCK.value,
        Characters.UPPER_HALF_BLOCK.value,
        Characters.RIGHT_HALF_BLOCK.value,
    ]
}