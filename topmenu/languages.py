# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Language(object):
	def __init__(self, for_sale, wanted, jobs, announcements):
		self.for_sale = for_sale
		self.wanted = wanted
		self.jobs = jobs
		self.announcements = announcements

class French(Language):
	def __init__(for_sale, wanted, jobs, announcements):
		self.for_sale = "À vendre"
		self.wanted = "Demande de"
		self.jobs = "Emploi"
		self.announcements = "Annonces"

class English(Language):
	def __init__(for_sale, wanted, jobs, announcements):
		self.for_sale = "For sale"
		self.wanted = "Wanted"
		self.jobs = "Jobs"
		self.announcements = "Announcements"

class Spanish(Language):
	def __init__(for_sale, wanted, jobs, announcements):
		self.for_sale = "Se vende"
		self.wanted = "Se busca"
		self.jobs = "Trabajo"
		self.announcements = "Anuncios"