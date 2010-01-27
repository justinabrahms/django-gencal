Gencal Template Tag
===================

The General Idea
----------------

The :class:`ListingCalendar` object is inherited from Python's
:class:`calendar.HTMLCalendar`. The general idea here is to wrap
`HTMLCalendar` in order to pass a list of items. From that list, we'll
gather date objects to plot on the calendar.

Template Tag
------------

.. automodule:: gencal.templatetags.gencal
   :members: gencal

Where the magic happens
-----------------------

.. autoclass:: gencal.templatetags.gencal.ListCalendar
   :members:
   :undoc-members:
