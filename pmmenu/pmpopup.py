import os
import pygame
import subprocess
import string
from os import system
from pmcontrols import *
from pmutil import *

class PMPopup(pygame.sprite.Sprite):

	def __init__(self, scene_type, cfg, list = None):
		pygame.sprite.Sprite.__init__(self)
		
		self.cfg = cfg
		self.scene_type = scene_type
		
		
		self.hover = 0
		self.selected = False
		self.menu_open = False
		
		self.screen = None
		self.effect = None
		
		self.menu_work = WorkFunctions(self.cfg)
		self.list = self.build_menu(self.scene_type)
		self.item_height = self.list[0]['value'].rect.h
		self.update_menu()

		self.rect = self.menu.get_rect()
	
	#MENU FUNCTIONS
	def hover_next(self):
		self.hover += 1
		if self.hover > (len(self.list)-1): self.hover = 0
		self.update_menu()
		
	def hover_prev(self):
		self.hover -= 1
		if self.hover < 0: self.hover = len(self.list)-1
		self.update_menu()
	
	def set_selected(self):
		self.selected = not self.selected
		self.update_menu()
		
		
	def build_menu(self, scene_type):
		if scene_type == "main":
			self.volume = {
			"title": PMPopitem("Volume:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(self.menu_work.get_sound_volume(), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Volume:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(self.menu_work.get_sound_volume(), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.volume_up,
			"next": self.menu_work.volume_down
			}
			
			self.theme = {
			"title": PMPopitem("Theme:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(self.menu_work.theme_list[self.menu_work.theme_count], self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Theme:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(self.menu_work.theme_list[self.menu_work.theme_count], self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.theme_prev,
			"next": self.menu_work.theme_next
			}
			
			self.cursor = {
			"title": PMPopitem("Show Cursor:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.cursor_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Show Cursor:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.cursor_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.cursor_swap,
			"next": self.menu_work.cursor_swap
			}
			
			self.transitions = {
			"title": PMPopitem("Scene FX:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.scene_trans_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Scene FX:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.scene_trans_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.transition_swap,
			"next": self.menu_work.transition_swap
			}

			self.show_ip = {
			"title": PMPopitem("Show IP:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.ip_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Show IP:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.ip_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.ip_swap,
			"next": self.menu_work.ip_swap
			}
			
			self.show_update = {
			"title": PMPopitem("Show Update:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.update_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Show Update:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.update_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.update_swap,
			"next": self.menu_work.update_swap
			}
			
			self.sort_alphanum = {
			"title": PMPopitem("Sort ABC:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.sort_abc_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Sort ABC:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.sort_abc_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.sort_abc_swap,
			"next": self.menu_work.sort_abc_swap
			}
			
			self.roms_first = {
			"title": PMPopitem("Show roms 1st:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.roms_first_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Show roms 1st:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.roms_first_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.roms_first_swap,
			"next": self.menu_work.roms_first_swap
			}
			
			self.hide_items_without_roms = {
			"title": PMPopitem("Hide Empty Emu:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.hide_items_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Hide Empty Emu:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.hide_items_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.hide_items_swap,
			"next": self.menu_work.hide_items_swap
			}
			
			self.quit_to_console = {
			"title": PMPopitem("Allow PiPlay Quit:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.quit_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Allow PiPlay Quit:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.quit_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.quit_swap,
			"next": self.menu_work.quit_swap
			}
			
			self.scraper_clones = {
			"title": PMPopitem("Scrape Clones:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.scraper_clones_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Scrape Clones:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.scraper_clones_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.scraper_clones_swap,
			"next": self.menu_work.scraper_clones_swap
			}
			
			self.scraper_overwrite_image = {
			"title": PMPopitem("Overwrite Images:", self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"value": PMPopitem(str(self.menu_work.scraper_overwrite_bool), self.cfg.popup_font, self.cfg.popup_menu_font_color),
			"title_selected": PMPopitem("Overwrite Images:", self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"value_selected": PMPopitem(str(self.menu_work.scraper_overwrite_bool), self.cfg.popup_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.scraper_overwrite_swap,
			"next": self.menu_work.scraper_overwrite_swap
			}
			

			
			popup = [self.volume, self.theme, self.cursor, self.transitions, self.show_ip, self.show_update, self.sort_alphanum,
						self.roms_first, self.hide_items_without_roms, self.quit_to_console, self.scraper_clones, self.scraper_overwrite_image]
			
			return popup
			#self.themes = PMPopitem(get_theme(), cfg.popup_font, cfg.popup_menu_font_color)
			
		elif scene_type == "romlist":
			
			self.selected = True
			
			self.letter = {
			"value": PMPopitem(self.menu_work.abc_list[self.menu_work.abc_count], self.cfg.popup_rom_letter_font, self.cfg.popup_menu_font_color),
			"value_selected": PMPopitem(self.menu_work.abc_list[self.menu_work.abc_count], self.cfg.popup_rom_letter_font, self.cfg.popup_menu_font_selected_color),
			"prev": self.menu_work.abc_prev,
			"next": self.menu_work.abc_next,
			}
			
			popup = [self.letter]
			
			return popup
	
	def update_menu(self):
		if self.scene_type == 'main':
		
			self.item_width = max(self.list, key=lambda x: x['title'].rect.w)['title'].rect.w + max(self.list, key=lambda x: x['value'].rect.w)['value'].rect.w + 40
			text_rect = pygame.Rect(0,0, self.item_width, (self.item_height * len(self.list)) + 20)
			self.menu = pygame.Surface([text_rect.w, text_rect.h], pygame.SRCALPHA, 32).convert_alpha()
			self.menu.fill(self.cfg.popup_menu_background_color, text_rect)
			
			y = 10
			x = 10
			for index, item in enumerate(self.list):
				if index == self.hover:
					self.menu.blit(item['title_selected'].image, (x,y))
				else:
					self.menu.blit(item['title'].image, (x,y))
				if self.selected and index == self.hover:
					self.menu.blit(item['value_selected'].image, (text_rect.w - item['value'].rect.w - x, y))
				else:
					self.menu.blit(item['value'].image, (text_rect.w - item['value'].rect.w - x, y))
					
				y += item['title'].rect.height
				
		elif self.scene_type == 'romlist':
			
			text_rect = pygame.Rect(0,0, int(self.item_height * 1.5), int(self.item_height * 1.5))
			self.menu = pygame.Surface([text_rect.w, text_rect.h], pygame.SRCALPHA, 32).convert_alpha()
			self.menu.fill(self.cfg.popup_menu_background_color, text_rect)
			
			
			y = 0
			for index, item in enumerate(self.list):
				self.menu.blit(item['value'].image, ((text_rect.w - item['value'].rect.w)/2, (text_rect.h - item['value'].rect.h)/2))
					
				y += item['value'].rect.height
			
	def handle_events(self, action, screen, effect):
		self.screen = screen
		self.effect = effect
		
		if action == 'LEFT':
			self.cfg.menu_navigation_sound.play()
			if not self.selected: self.hover_prev()
			else:
				self.list[self.hover]['prev']()
				self.list = self.build_menu(self.scene_type)
				self.update_menu()
			self.draw_menu()
		elif action == 'RIGHT':
			self.cfg.menu_navigation_sound.play()
			if not self.selected: self.hover_next()
			else: 
				self.list[self.hover]['next']()
				self.list = self.build_menu(self.scene_type)
				self.update_menu()
			self.draw_menu()
		elif action == 'UP':
			self.cfg.menu_navigation_sound.play()
			if not self.selected: self.hover_prev()
			else:
				self.list[self.hover]['prev']()
				self.list = self.build_menu(self.scene_type)
				self.update_menu()
			self.draw_menu()
		elif action == 'DOWN':
			self.cfg.menu_navigation_sound.play()
			if not self.selected: self.hover_next()
			else: 
				self.list[self.hover]['next']()
				self.list = self.build_menu(self.scene_type)
				self.update_menu()
			self.draw_menu()
		elif action == 'MENU':
			if self.selected and self.scene_type != 'romlist':
				action = 'SELECT'
			else:
				self.cfg.menu_back_sound.play()
				self.menu_open = False
				self.screen.blit(self.cfg.fade_image,(0,0))
				self.on_exit_actions()
				
		elif action == 'BACK':
				self.cfg.menu_back_sound.play()
				self.menu_open = False
				self.screen.blit(self.cfg.fade_image,(0,0))
				self.on_exit_actions()
		
		if action == 'SELECT':
			if self.scene_type != 'romlist':
				self.cfg.menu_select_sound.play()
				self.selected = not self.selected
				self.update_menu()
				self.draw_menu()
				
			
				
	def on_exit_actions(self):
		config_path = '/home/pi/pimame/pimame-menu/config.yaml'
		requires_restart = False
		
		#THEME
		if self.menu_work.theme_list[self.menu_work.theme_count] != self.cfg.theme_name:
			PMUtil.replace(config_path, 'theme_pack: "' + self.cfg.theme_name, 'theme_pack: "' + self.menu_work.theme_list[self.menu_work.theme_count])
			requires_restart = True
		
		#CURSOR
		if self.cfg.show_cursor != self.menu_work.cursor_bool:
			pygame.mouse.set_visible(self.menu_work.cursor_bool)
			PMUtil.replace(config_path, '', str(self.menu_work.cursor_bool), 'show_cursor:')
		
		#SCENE TRANSITIONS
		if self.cfg.use_scene_transitions != self.menu_work.scene_trans_bool:
			self.cfg.use_scene_transitions = self.menu_work.scene_trans_bool
			PMUtil.replace(config_path, '', str(self.menu_work.scene_trans_bool), 'use_scene_transitions:')
		
		#IP
		if self.cfg.show_ip != self.menu_work.ip_bool:
			self.cfg.show_ip = self.menu_work.ip_bool
			PMUtil.replace(config_path, '', str(self.menu_work.ip_bool), 'show_ip:')
		
		#SHOW UPDATE
		if self.cfg.show_update != self.menu_work.update_bool:
			self.cfg.show_update = self.menu_work.update_bool
			PMUtil.replace(config_path, '', str(self.menu_work.update_bool), 'show_update:')
		
		#SORT EMU BY ALPHANUM
		if self.cfg.sort_items_alphanum != self.menu_work.sort_abc_bool:
			self.cfg.sort_items_alphanum = self.menu_work.sort_abc_bool
			PMUtil.replace(config_path, '', str(self.menu_work.sort_abc_bool), 'sort_items_alphanum:')
			requires_restart = True
		
		#SORT EMU WITH ROMS FIRST
		if self.cfg.sort_items_with_roms_first != self.menu_work.roms_first_bool:
			self.cfg.sort_items_with_roms_first = self.menu_work.roms_first_bool
			PMUtil.replace(config_path, '', str(self.menu_work.roms_first_bool), 'sort_items_with_roms_first:')
			requires_restart = True
		
		#HIDE ITEMS WITHOUT ROMS
		if self.cfg.hide_items_without_roms != self.menu_work.hide_items_bool:
			self.cfg.hide_items_without_roms = self.menu_work.hide_items_bool
			PMUtil.replace(config_path, '', str(self.menu_work.hide_items_bool), 'hide_items_without_roms:')
			requires_restart = True
		
		#ALLOW QUIT TO CONSOLE
		if self.cfg.allow_quit_to_console != self.menu_work.quit_bool:
			self.cfg.allow_quit_to_console = self.menu_work.quit_bool
			PMUtil.replace(config_path, '', str(self.menu_work.quit_bool), 'allow_quit_to_console:')
		
		#SCRAPER SHOW CLONES
		if self.cfg.show_clones != self.menu_work.scraper_clones_bool:
			self.cfg.show_clones = self.menu_work.scraper_clones_bool
			PMUtil.replace(config_path, '', str(self.menu_work.scraper_clones_bool), 'show_clones:')
		
		#SCRAPER OVERWRITE IMAGES
		if self.cfg.overwrite_images != self.menu_work.scraper_overwrite_bool:
			self.cfg.overwrite_images = self.menu_work.scraper_overwrite_bool
			PMUtil.replace(config_path, '', str(self.menu_work.scraper_overwrite_bool), 'overwrite_images:')
			
		if requires_restart: 
			system('clear')
			PMUtil.run_command_and_continue('echo Changing settings and restarting PiPlay')
		
	def draw_menu(self):
		self.screen.blit(self.effect,(0,0))
		self.screen.blit(self.menu, ((pygame.display.Info().current_w - self.rect.w)/2, (pygame.display.Info().current_h - self.rect.h)/2))
		

		
class WorkFunctions():
	def __init__(self, cfg):
		
		#mainscene
		self.cfg = cfg
		self.theme_count = 0
		self.theme_list = self.get_themes()
		self.cursor_bool = self.cfg.show_cursor
		self.scene_trans_bool = self.cfg.use_scene_transitions
		self.ip_bool = self.cfg.show_ip
		self.update_bool = self.cfg.show_update
		self.sort_abc_bool = self.cfg.sort_items_alphanum
		self.roms_first_bool = self.cfg.sort_items_with_roms_first
		self.hide_items_bool = self.cfg.hide_items_without_roms
		self.quit_bool = self.cfg.allow_quit_to_console
		self.scraper_clones_bool = self.cfg.show_clones
		self.scraper_overwrite_bool = self.cfg.overwrite_images
		
		#romlist
		self.abc_count = 0
		self.abc_list = map(chr, range(65, 91))
		
	
		#MENU ITEM FUNCTIONS
	def get_sound_volume(self):
		try: 
			volume = subprocess.check_output("amixer -c 0 get PCM | awk '/dB/ {print $4}'", shell=True)
			return volume.split("]")[0].split("[")[1]
		except:
			return "Not available"
			
	def volume_up(self):
		system("/usr/bin/amixer -q -c 0 sset PCM 3dB+ unmute nocap")
		
	def volume_down(self):
		system("/usr/bin/amixer -q -c 0 sset PCM 3dB- unmute nocap")
		
	def get_themes(self):
		a = [x for x in os.walk('/home/pi/pimame/pimame-menu/themes/').next()[1] if os.path.isfile('/home/pi/pimame/pimame-menu/themes/' + x + '/theme.yaml') and x != self.cfg.theme_name]
		a.insert(0, self.cfg.theme_name)
		return a
			
	def theme_prev(self):
		self.theme_count -= 1
		if self.theme_count < 0: self.theme_count = len(self.theme_list) - 1
		
	def theme_next(self):
		self.theme_count += 1
		if self.theme_count >= len(self.theme_list): self.theme_count = 0
		
	def cursor_swap(self):
		self.cursor_bool = not self.cursor_bool
		return self.cursor_bool
	
	def transition_swap(self):
		self.scene_trans_bool = not self.scene_trans_bool
		return self.scene_trans_bool
		
	def ip_swap(self):
		self.ip_bool = not self.ip_bool
		return self.ip_bool
		
	def update_swap(self):
		self.update_bool = not self.update_bool
		return self.update_bool
		
	def sort_abc_swap(self):
		self.sort_abc_bool = not self.sort_abc_bool
		return self.sort_abc_bool
		
	def roms_first_swap(self):
		self.roms_first_bool = not self.roms_first_bool
		return self.roms_first_bool
		
	def hide_items_swap(self):
		self.hide_items_bool = not self.hide_items_bool
		return self.hide_items_bool
		
	def quit_swap(self):
		self.quit_bool = not self.quit_bool
		return self.quit_bool
		
	def scraper_clones_swap(self):
		self.scraper_clones_bool = not self.scraper_clones_bool
		return self.scraper_clones_bool
		
	def scraper_overwrite_swap(self):
		self.scraper_overwrite_bool = not self.scraper_overwrite_bool
		return self.scraper_overwrite_bool
		
	#ROMLIST FUNCTIONS
	def abc_prev(self):
		self.abc_count -= 1
		if self.abc_count < 0: self.abc_count = len(self.abc_list) - 1
		
	def abc_next(self):
		self.abc_count += 1
		if self.abc_count >= len(self.abc_list): self.abc_count = 0
	
	
	def abc_find(self, list):
        #list = ['alpha','bravo','charlie','delta','echo','foxtrot','golf','hotel','india',
                #'juliet','kilo','lima','mike','november','oscar','papa','Quebec','romeo',
                #'sierra','tango','uniform','victor','whiskey','x-ray','yankee','zulu']

        #abc_list = map(chr, range(65,91))
		for index, i in enumerate(list):
			if ord(i['title'][0].upper()) >= ord(self.abc_list[self.abc_count]):
				return index
		return 0

		
class PMPopitem(pygame.sprite.Sprite):
	def __init__(self, label_text, font, color_fg, font_bold = False):
		pygame.sprite.Sprite.__init__(self)
		
		self.text = label_text
		self.color_fg = color_fg
		self.font = font
		
		#pygame faux bold font
		font.set_bold(font_bold)
		text = font.render(label_text, 1, color_fg).convert_alpha()
		text_rect = text.get_rect()
		if label_text == '': text_rect.w = 0
		self.image = pygame.Surface([text_rect.w, text_rect.h], pygame.SRCALPHA, 32).convert_alpha()
		self.image.blit(text, text_rect)

		
		self.rect = self.image.get_rect()