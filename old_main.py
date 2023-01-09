def main2():
	camera = Camera(63+1, 63+1)

	message_x = 1
	message_y = 5
	message_width = 20
	message_height = 40

	LIMIT_FPS = 20

	tcod.sys_set_fps(LIMIT_FPS)




	colors = {
		'dark_wall': tcod.Color(0, 0, 100),
		'dark_ground': tcod.Color(50, 50, 150),
		'light_wall': tcod.darkest_blue,
		'light_ground': tcod.desaturated_blue
	}
	player = Entity(0, 0, "@", tcod.white, 'Player', blocks=True)

	entities = [player]
	tcod.console_set_custom_font(font_file, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW)
	tcod.console_init_root(screen_width, screen_height, 'Mech Strike: Resistance', False)

	con = tcod.console_new(screen_width, screen_height)
	panel = tcod.console_new(panel_width, panel_height)
	game_map = GameMap(map_view_width * 3 , map_view_height * 3)
	game_map.make_map(map_view_width, map_view_height, player, entities)
	render = Render()
	
	#test stuff
	player.place(93, 93)
	entities.insert(0, Mech(63 + 8, 63 + 8, tcod.lighter_orange, 'Mech'))

	message_log = MessageLog(message_x, message_y, message_width, message_height)

	key = tcod.Key()
	mouse = tcod.Mouse()

	game_state = GameStates.PLAYERS_TURN

	while not tcod.console_is_window_closed():
	#game loop
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

		camera.update(player, game_map.zoomed_out)

		render.render_all(con, panel, entities, game_map, message_log, camera)


		tcod.console_flush()

		render.clear_all(con, entities, camera, game_map.zoomed_out)

		action = handle_keys(key)

		move = action.get('move')
		embark = action.get('embark')
		inventory = action.get('inventory')

		exit = action.get('exit')
		fullscreen = action.get('fullscreen')

		if move and game_state == GameStates.PLAYERS_TURN:
			dx, dy = move
			destination_x = player.x + dx
			destination_y = player.y + dy

			if not game_map.is_blocked(destination_x, destination_y):
				target = get_blocking_entities_at_location(entities, destination_x, destination_y)

				if isinstance(target, Mech) or not target:
					player.move(dx, dy)
					fov_recompute = True
				else:
					pass
			#
			print(vars(entities[0]))
			#
		if embark:
			game_map.toggle_zoom()

		if inventory:
			message_log.add_message(Message('Inventory is empty', tcod.white))
			print(message_log.messages[0].text)
		if exit:
			return True

		if fullscreen:
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
