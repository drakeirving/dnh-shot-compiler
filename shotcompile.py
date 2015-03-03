import sys
import re
import json

def compile_shots(obj):
	blend_types = ['ALPHA','ADD','ADD_RGB','ADD_ARGB','MULTIPLY', 'SUBTRACT', 'INV_DESTRGB']

	s = '#UserShotData\n\n'

	if 'shot_image' in obj:
		s += 'shot_image = \"' + obj['shot_image'] + '\"\n'

	if 'delay_rect' in obj:
		s += 'delay_rect = (' + str(obj['delay_rect'])[1:-1] + ')\n'

	if 'delay_color' in obj:
		s += 'delay_color = (' + str(obj['delay_color'])[1:-1] + ')\n'

	if 'shots' in obj:
		s += '\n'
		id = 1
		for bunch in obj['shots']:
			if ('colors' in bunch and len(bunch['origin']) > 0 and
				'origin' in bunch and len(bunch['origin']) == 2 and
				'size' in bunch and len(bunch['size']) == 2 and
				('off' in bunch and len(bunch['off']) == 2) or ('animation' in bunch and len(bunch['animation']) == 3)):

				s += '// bunch\n\n'

				l = bunch['origin'][0]
				t = bunch['origin'][1]
				size = bunch['size']
				off = None
				if 'off' in bunch: off = bunch['off']
				animation = None
				if 'animation' in bunch: animation = bunch['animation']

				for i in range(len(bunch['colors'])):
					s += 'ShotData{\n'

					s += '\tid = ' + str(id) + '\n'

					if animation:
						s += '\tAnimationData{\n'
						for j in range(animation[2]):
							s += '\t\tanimation_data = (' + str([ animation[3], l+animation[0]*j, t+animation[1]*j, l+animation[0]*j + size[0], t+animation[1]*j + size[1] ])[1:-1] + ')\n'
						s += '\t}\n'
					else:
						s += '\trect = (' + str([ l, t, l + size[0], t + size[1] ])[1:-1] + ')\n'

					if 'collision' in bunch:
						s += '\tcollision = ' + str(bunch['collision']) + '\n'

					if 'fixed_angle' in bunch:
						s += '\tfixed_angle = ' + str(bunch['fixed_angle']).lower() + '\n'

					if 'angular_velocity' in bunch:
						if isinstance(bunch['angular_velocity'], list):
							s += '\tangular_velocity = rand(' + str(bunch['angular_velocity'])[1:-1] + ')\n'
						else:
							s += '\tangular_velocity = ' + str(bunch['angular_velocity']) + '\n'


					if 'render' in bunch and bunch['render'].upper() in blend_types:
						s += '\trender = ' + bunch['render'].upper() + '\n'

					if 'delay_render' in bunch and bunch['delay_render'].upper() in blend_types:
						s += '\tdelay_render = ' + bunch['delay_render'].upper() + '\n'

					if 'colors' in obj and bunch['colors'][i] in obj['colors']:
						color = bunch['colors'][i]
						s += '\tdelay_color = (' + str(obj['colors'][color])[1:-1] + ')\n'

					s += '}\n\n'

					id += 1
					if off:
						l += off[0]
						t += off[1]

	return s


try:
	f = sys.argv[1] if len(sys.argv) > 1 else 'shots.json'
	of = sys.argv[2] if len(sys.argv) > 2 else 'shots.dnh'

	inp = re.sub(r'//.*', '', open(f, 'r').read())
	out = open(of, 'w', encoding='utf8')

	s = compile_shots(json.loads(inp))
	# print(s)

	out.write(s)
	out.close()
except Exception as e:
	print('Error in ' + f + ': ' + str(type(e)) + ': ' + str(e.args[2:]))

