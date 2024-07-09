import turtle as t


BG_COLOR = "black"
TITLE = "Space Binvaders"
PLAYER_COLOR = "lime"
ALIEN_COLOR = "white"
PLAYER_MOVE_UNITS = 10
ALIEN_MOVE_UNITS = 10
SCREEN_BUFFER = 0.9
ALIEN_MOVE_INTERVAL = 500  # in milliseconds


class SpaceBinvaders:

	def __init__(self, screen_width_ratio=0.33, screen_height_ratio=0.66):
		self.screen = self.create_screen(screen_width_ratio, screen_height_ratio)
		self.screen_width = self.screen.window_width()
		self.screen_height = self.screen.window_height()
		self.bottom_edge = -self.screen_height / 2 * SCREEN_BUFFER
		self.top_edge = self.screen_height / 2 * SCREEN_BUFFER
		self.left_edge = -self.screen_width / 2 * SCREEN_BUFFER
		self.right_edge = self.screen_width / 2 * SCREEN_BUFFER

		self.player = self.create_player()
		self.aliens = self.spawn_aliens()

		self.register_keystrokes()
		self.screen.listen()

		self.direction = 1
		self.alien_move_iters = 0


	def create_screen(self, screen_width_ratio, screen_height_ratio):
		screen = t.Screen()
		screen.setup(screen_width_ratio, screen_height_ratio)
		screen.bgcolor(BG_COLOR)
		screen.title(TITLE)

		return screen


	def create_player(self):
		# create the player turtle
		player = t.Turtle()
		player.penup()  # so it won't draw lines
		player.color(PLAYER_COLOR)
		player.shape("square")
		player.turtlesize(1, 3)  # stretch it to a rectangle
		player.setpos(0, self.bottom_edge)  # move it to the bottom of the game screen

		return player


	def spawn_aliens(self, num_aliens=8):
		left_spawn_edge = self.left_edge + 200

		# need to evenly space aliens. 1 row for now
		alien_gap = ((self.screen_width * SCREEN_BUFFER - 200) / num_aliens) - 20
		aliens = []
		for x in range(num_aliens):
			alien = SpaceBinvaders.create_alien()
			# set the alien position. start at the left side of the screen
			alien.setpos(left_spawn_edge + (alien_gap * x), self.top_edge)

			# add aliens to a list so we can move them later on
			aliens.append(alien)

		return aliens


	def move_player(self, dx):		
		# check if the player is at the window boundary
		if self.left_edge < self.player.xcor() + dx < self.right_edge:
			# moves the player without changing the heading
			self.player.setx(self.player.xcor() + dx)


	def move_aliens(self):
		if self.alien_move_iters >= 10:
			self.direction *= -1
			self.alien_move_iters = 0

		for alien in self.aliens:
			alien.setx(alien.xcor() + (ALIEN_MOVE_UNITS * self.direction))

		self.alien_move_iters += 1

		self.screen.ontimer(self.move_aliens, ALIEN_MOVE_INTERVAL)


	def register_keystrokes(self):
		self.screen.onkeypress(
			lambda: self.move_player(PLAYER_MOVE_UNITS),
					"Right"  # register right keystroke
		)
		self.screen.onkeypress(
			lambda: self.move_player(-PLAYER_MOVE_UNITS),
					"Left"  # register left keystroke
		)
		# I don't think we need up and down keystrokes?


	@staticmethod
	def create_alien():
		# create the alien turtle
		alien = t.Turtle()
		alien.speed("fast")
		alien.penup()  # won't draw lines
		alien.color(ALIEN_COLOR)
		alien.shape("triangle")
		alien.turtlesize(2, 2)
		alien.setheading(270)

		return alien