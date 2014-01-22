from os import listdir, system
from os.path import isfile, isdir, join, splitext, basename
import pygame
from pmlabel import *


class PMMenuItem(pygame.sprite.Sprite):
	num_roms = 0

	def __init__(self, item_opts, global_opts):
		pygame.sprite.Sprite.__init__(self)

		self.label = item_opts['label']
		self.command = item_opts['command']
		self.roms = item_opts['roms']
		self.full_path = item_opts['full_path']

		#@TODO this code is duplicated
		screen_width = pygame.display.Info().current_w
		item_width = ((screen_width - global_opts.padding) / global_opts.num_items_per_row) - global_opts.padding

		self.image = pygame.Surface([item_width, global_opts.item_height])
		self.image.fill(global_opts.item_color)

		icon_file_path = global_opts.icon_pack_path + item_opts['icon_file']
		icon = pygame.image.load(icon_file_path).convert_alpha()

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

		icon = pygame.transform.scale(icon, icon_size)
		self.image.blit(icon, ((avail_icon_width - icon_size[0]) / 2 + global_opts.padding, (avail_icon_height - icon_size[1]) / 2 + global_opts.padding))

		#font = pygame.font.Font(global_opts.font_file, global_opts.font_size)
		#text = font.render(self.label, 1, (0, 0, 0))
		label = PMLabel(self.label, global_opts.font, global_opts.text_color, global_opts.item_color)
		textpos = label.rect
		textpos.x = global_opts.padding
		textpos.y = global_opts.item_height - textpos.height - global_opts.padding

		self.image.blit(label.image, textpos)

		

		self.update_num_roms()

		if self.num_roms == 0:
			self.image.set_alpha(64)
		else:
			# draw rom circle
			rom_rect = (item_width - global_opts.padding - 30, global_opts.item_height - global_opts.padding - 30, 30, 30)
			pygame.draw.rect(self.image, global_opts.rom_dot_color, rom_rect)

			#text = font.render(str(num_roms), 1, (255, 255, 255))
			label = PMLabel(str(self.num_roms), global_opts.font, global_opts.text_highlight_color, global_opts.rom_dot_color)
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

		files = [ f for f in listdir(self.roms) if isfile(join(self.roms,f)) ]

		self.num_roms = len(files)

	def get_rom_list(self):
		#@TODO - am I using the type field?
		if self.full_path == False:
			return [
				{
					'title': f,
					'type': 'command',
					'command': self.command + " " +  os.path.splitext(os.path.basename(f))[0] 
				}
				for f in listdir(self.roms) if isfile(join(self.roms, f))
			]


		return [
			{
				'title': f,
				'type': 'command',
				'command': self.command + ' \'' + self.roms + f +'\'' 
			}
			for f in listdir(self.roms) if isfile(join(self.roms, f))
		]

	def run_command(self):
		print self.command
		system(self.command)