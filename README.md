SMS Lists (beta) 747-222-1816
=============================

SMS Lists is an SMS-based classifieds system designed for communities with
limited internet access. Listings are limited to 140 characters. 
To learn more, visit WorldDev.io.

Overview
---------
SMS Lists is built on Django and PostgreSQL. While the U.S. beta uses Twilio,
the service is designed to agnositcally connect to APIs of wireless 
communication organizations worldwide.

Custom middleware associates user session data with a user's phone number.
Views are both class-based and function-based. In order to encourage
contributions, future releases will further incorporate generic views.

The launch beta is not location-aware, but future releases will utilize
geocoding APIs to allow for the segmentation of postings according to
locale.

Structure
---------
The beta includes six listing categories:

1. For sale
2. Jobs
3. Rides
4. Announcements
5. Commentary
6. Emergency

While present, Commentary and Emergency listings are currently in development
and will be activated in the future.

Listings are composed of two parts – header and listing detail. The header is
component is displayed when browsing listings and thus is limited to 40
characters. The detail component is the full listing and is limited to 140
characters.

Acknowledgements
----------------
This software wouldn't exist without the invaluable mentorship and architectural 
advice of Laszlo Marai. Laszlo's decades of experience and penchant for teaching
aided SMS Lists in growing from a primitive script to its current beta release.

I must also thank Ben Rachbach – Ben, thanks for being an incredible research
partner, patient travel companion and outstanding friend. Additionally, Andy
Rossback contributed the excellent design of both the WorldDev logo and the
layout for WorldDev.io.

I'd like to thank Jimmy Maguru and Alyosius Muwanga with the Nsamizi 
Training Institute for Social Development. Their guidance and vital
support were critical to the Ugandan research that led to SMS Lists.

Research in Haiti was facilitated by the great John Presime. John's efforts as
research partner, logistics coordinator and Kreole translator were critical to
the development of SMS Lists.

Further acknowledgements go to Pierre Noel and Samantha Hackney at the Haiti
Development Institute. Despite an extreme workload, Pierre and Samantha
made time to share a great deal of knowledge about the Haitian refugee crisis.

Finally, I need to thank the many translators and interpreters who, as both
professionals and themselves refugees, provided indispensable value and 
insight.