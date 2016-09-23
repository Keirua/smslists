# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class Language(object):
	def __init__(self, for_sale, wanted, jobs, announcements, rides, emergency, commentary):
		self.for_sale = for_sale
		self.wanted = wanted
		self.jobs = jobs
		self.announcements = announcements
		self.rides = rides
		self.emergency = emergency
		self.commentary = commentary

French = Language(for_sale="À vendre", wanted = "Demande de", jobs = "Emploi", announcements = "Annonces", rides = 'covoiturage', emergency = "d'Urgence", commentary= 'Commentaire')
English = Language(for_sale = "For sale", wanted = "Wanted", jobs = "Jobs", announcements = "Announcements", rides = "Rides", emergency = "Emergency", commentary = 'Commentary')
Spanish = Language(for_sale = "Se vende", wanted = "Se busca", jobs = "Trabajo", announcements = "Anuncios", rides = "Viajes", emergency = "Emergencia", commentary = "Comentarios")

LANGUAGES = {'French':French, 'English':English, 'Spanish':Spanish}


