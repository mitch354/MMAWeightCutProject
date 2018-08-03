# CMPT-353
## MMAWeightCutProject

#### Background

In	most	combat	sports	athletes	are	separated	by	and	compete	within	weight	classes.
A	weight	class	is	a	range	of	weights	(i.e	171	lbs	– 186	lbs	for	the	middleweight	division) in
which	the	athlete	must	officially	weigh	in	at	in	order	for	the	fight	to	be	sanctioned	by	the
governing	athletic	commission of	where	the	fight	is	taking	place.	This	weigh-in	is	usually
held	the	day	before	the	contest and	is	designed	to	ensure	fair competition	since	being
significantly	bigger	than	your	opponent	is	a	huge	advantage in	combat	sports.


This	had	led	to	a	practice	called	weight	cutting.	With	weight	cutting	your	weight	is
only	actually	within	your	weight	class	when	you	officially	weigh	in.		The	days	preceding	this
are	spent	trying	to	drain	your	body	of	as	much	water	as	possible	until	you	reach	the	upper
limit	of	your	weight	class.	After	you	weigh	in	you	start	rehydrating	to	come	into	the	fight	the
next	day	as	heavy	as	possible.	This	process	can	result	in	you	being	more	than	30	lbs	heavier
than	your	weight	class	during	the	fight.


Needless	to	say	this	process	is	incredibly	dangerous.	A	prisoner’s	dilemma	situation
is	created	in	which	fighter’s	have	to	cut	large	amounts	out	of	fear	that	if	they	don’t	their
opponent	will. Weight	cutting	has	also	led	to	fighters	missing	weight,	having	to	stop	their
weight	cut	short	of	the	upper	limit	due	to	medical	concerns,	and	weighing	in	heavier	than
their	classes	limit.	 The	goal	of	this	project	is	to	explore	under	what	conditions	this	might
happen	and	what	attributes	to	look	for	in	a	fighter	that	is	likely	to	miss	weight.

#### Instructions

ETL/getFights.py & ETL/getFighters.py

Both of these can run from the command line like: python3 getFights.py
They output fights.json and fighters.json respectively. These each take 10+ minutes
to run so a copy of each is already available.

Analysis/missedWeightAge.py, Analysis/missedWeightTime.py, Analysis/weightClassifier.py

These take the produced json files as input. No parameters are needed.
python3 missedWeightAge.py
