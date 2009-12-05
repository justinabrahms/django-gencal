This project aims to be a drop-in solution for calendaring for
any django app.

An imporant distinction here is I mean calendar (rendering calendars)
not recurring events and such. For that, check out Tony Hauber's
[django-schedule](http://github.com/thauber/django-schedule).

Example Usage:

  {% load gencal %}
  
  {% gencal my_list 2009 11 %}

or

  {% gencal my_list %} # will default to today