from os import listdir, system
from os.path import isfile, isdir, join, splitext, basename
import pygame
from pmlabel import *


class PMMenuItem(pygame.sprite.Sprite):
	ROM_LIST = 'rom_list'
	COMMAND = 'command'
	NAVIGATION = 'nav'
	NEXT_PAGE = 'next'
	PREV_PAGE = 'prev'

	num_roms = 0

	def __init__(self, item_opts, global_opts, type = False):
		pygame.sprite.Sprite.__init__(self)

		self.label = item_opts['label']
		self.command = item_opts['command']
		self.full_path = item_opts['full_path']
		if item_opts['icon_selected']: 
			self.icon_selected = global_opts.theme_pack + item_opts['icon_selected']
			self.pre_loaded_selected_icon = global_opts.load_image(self.icon_selected, global_opts.generic_menu_item_selected)
		else:
			self.icon_selected = False
		#self.extension = item_opts['extension']

		try:
			self.roms = item_opts['roms']
		except KeyError:
			self.roms = False
		
		try:
			if item_opts['override_menu'] and item_opts['override_menu'] == True:
				self.override_menu = True
			else:
				self.override_menu = False
		except KeyError:
			self.override_menu = False

		try:
			if item_opts['extension'] and item_opts['extension'] == True:
				self.extension = True
			else:
				self.extension = False
		except KeyError:
			self.extension = False


		if type == False:
			#if self.roms:
			#	self.type = self.ROM_LIST
			#else:
			#	self.type = self.COMMAND
			if self.override_menu:
				self.type = self.COMMAND
			else:
				self.type = self.ROM_LIST
		else:
			self.type = type

		#@TODO this code is duplicated
		screen_width = pygame.display.Info().current_w
		item_width = ((screen_width - global_opts.padding) / global_opts.num_items_per_row) - global_opts.padding

		self.image = pygame.Surface([item_width, global_opts.item_height], pygame.SRCALPHA, 32).convert_alpha()
		#self.image = image.convert_alpha()
		#self.image.fill(global_opts.item_color)

		if item_opts['icon_file']:
			icon_file_path = global_opts.theme_pack + item_opts['icon_file']
			icon = global_opts.load_image(icon_file_path, global_opts.generic_menu_item)

			# resize and center icon:
			icon_size = icon.get_size()
			avail_icon_width = item_width - global_opts.padding * 2
			avail_icon_height = global_opts.item_height - global_opts.padding * 2
			while True:
				icon_width = icon_size[0]
				icon_height = icon_size[1]
				icon_ratio = float(icon_height) / float(icon_width)
				icon_width_diff = avail_icon_width - icon_width
				icon_height_diff = avail_icon_height - icon_height
				if icon_width_diff < icon_height_diff:
					diff = icon_width_diff
					icon_size = (icon_width + diff, icon_height + diff * icon_ratio)
				else:
					diff = icon_height_diff
					icon_size = (icon_width + diff / icon_ratio, icon_height + diff)

				icon_size = (int(icon_size[0]), int(icon_size[1]))

				if icon_size[0] <= avail_icon_width and icon_size[1] <= avail_icon_height:
					break

			icon = pygame.transform.smoothscale(icon, icon_size)
			self.image.blit(icon, ((avail_icon_width - icon_size[0]) / 2 + global_opts.padding, (avail_icon_height - icon_size[1]) / 2 + global_opts.padding))

		#font = pygame.font.Font(global_opts.font_file, global_opts.font_size)
		#text = font.render(self.label, 1, (0, 0, 0))
		if global_opts.display_labels:
			label = PMLabel(self.label, global_opts.label_font, global_opts.label_font_color, global_opts.label_background_color)
			textpos = label.rect
			textpos.x = global_opts.labels_offset[0]
			textpos.y = global_opts.labels_offset[1]

			self.image.blit(label.image, textpos)

		if global_opts.display_rom_count:
			if self.type == self.ROM_LIST:
				self.update_num_roms()

			if self.type == self.ROM_LIST:
				if self.num_roms == 0:
					self.image.set_alpha(64)
				else:
					# draw rom circle
					rom_rect = (global_opts.rom_count_offset[0], global_opts.rom_count_offset[1],30,30)

					#text = font.render(str(num_roms), 1, (255, 255, 255))
					label = PMLabel(str(self.num_roms), global_opts.rom_count_font, global_opts.rom_count_font_color, global_opts.rom_count_background_color)
					textpos = label.rect

					textpos.centerx = rom_rect[0] + rom_rect[2] / 2
					textpos.centery = rom_rect[1] + rom_rect[3] / 2
					self.image.blit(label.image, textpos)

		self.rect = self.image.get_rect()
		#print self.command

		#self.sprite = pygame.image.load(opts['icon_file']).convert_alpha()

	#def draw(self, screen, item_color, pos):
	#	self.sprite = pygame.draw.rect(screen, item_color, pos)
	#	return self.sprite

	#def get_pos(self):
	#	return self.sprite.x + ',' + self.sprite.y

	def update_num_roms(self):
		if not isdir(self.roms):
			return 0

		files = [ f for f in listdir(self.roms) if isfile(join(self.roms,f)) and f != '.gitkeep'  ]

		self.num_roms = len(files)

	def get_rom_list(self):
		#@TODO - am I using the type field?
		if self.full_path == False and self.extension == False:
			return [
				{
					'title': f,
					'type': 'command',
					'command': self.command + ' \"' +  os.path.splitext(os.path.basename(f))[0] + '\"' 
				}
				for f in listdir(self.roms) if isfile(join(self.roms, f)) and f != '.gitkeep'
			]
		elif self.full_path == False and self.extension == True:
						return [
								{
										'title': f,
										'type': 'command',
										'command': self.command + ' \"' +  os.path.splitext(os.path.basename(f))[0] + os.path.splitext(os.path.basename(f))[1] + '\"'
								}
								for f in listdir(self.roms) if isfile(join(self.roms, f)) and f != '.gitkeep' 
						]



		return [
			{
				'title': f,
				'type': 'command',
				'command': self.command + ' \"' + self.roms + f +'\"' 
			}
			for f in listdir(self.roms) if isfile(join(self.roms, f)) and f != '.gitkeep' 
		]

	def run_command(self):
		print self.command
		system(self.command)
