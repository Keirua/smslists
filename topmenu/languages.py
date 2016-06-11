# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class Language(object):
	def __init__(self, for_sale, wanted, jobs, announcements):
		self.for_sale = for_sale
		self.wanted = wanted
		self.jobs = jobs
		self.announcements = announcements

French = Language(for_sale="À vendre", wanted = "Demande de", jobs = "Emploi", announcements = "Annonces")
English = Language(for_sale = "For sale", wanted = "Wanted", jobs = "Jobs", announcements = "Announcements")
Spanish = Language(for_sale = "Se vende", wanted = "Se busca", jobs = "Trabajo", announcements = "Anuncios")

LANGUAGES = {'French':French, 'English':English, 'Spanish':Spanish}


