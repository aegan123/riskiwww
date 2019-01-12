#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riskiwww.settings")
import django
django.setup()
from eventsignup.models import EventType
#
etype=EventType(event_type='custom')
etype.save()
etype=EventType(event_type='muutapahtuma')
etype.save()
etype=EventType(event_type='ekskursio')
etype.save()
etype=EventType(event_type='vuosijuhlat')
etype.save()
etype=EventType(event_type='sitz')
etype.save()
etype=EventType(event_type='sitsit')
etype.save()
#
etypes=EventType.objects.all()
if etypes:
	print('Luoti onnistui.')
	for field in etypes:
		print(field)
else:
	print('Ei onnistunut.')
