import datetime
import calendar
from django.db.models import get_model
from django.template import Node, Library, TemplateSyntaxError, Variable, Context
from django.template.loader import get_template
from collections import defaultdict

register = Library()

class SimpleGencalNode(Node):
    """
    {% simple_gencal for Base.Model on date_field in DateObject with 'template' %}

    e.g.:
    
    {% simple_gencal for event.Event on day in date with gencal/gencal.html %}
    
    where:
    event is an application and Event is a model in that app and
    day is a field in Event and
    date is a Context variable containing the date to render on and
    gencal/gencal.html is a template to use to render a calendar.
    """
    def __init__(self, model, field, date_obj, template):
        self.field, self.date_obj, self.template = field, Variable(date_obj), template
        # See:
        #   http://www.b-list.org/weblog/2007/nov/03/working-models/
        # for explanation of this jiggery-pokery.
        model_list = model.split('.')
        assert(len(model_list) == 2)
        app_label, model_name = model_list
        self.model = get_model(app_label, model_name)
        assert (self.model != None)

    def render(self, context):
        self.date_obj = self.date_obj.resolve(context)
        self.field = str(self.field)
        year, month = getattr(self.date_obj, 'year'), getattr(self.date_obj, 'month')
        year_key, month_key = ("%s__year" % self.field), ("%s__month" % self.field)
        event_set = self.model._default_manager.filter( **{ year_key:year } ).filter( **{ month_key:month })

        cal_items = [{ 'day':getattr(event, self.field), 'title':event.__unicode__(), 'url':event.get_absolute_url(), 'class':'' } for event in event_set]

        d = gencal(self.date_obj, cal_items)
        template = get_template(self.template)
        return template.render(Context(d))

@register.tag(name='simple_gencal')
def simple_gencal(parser, token):
    """
    The proper way to call simple_gencal is::
    
        {% simple_gencal for Base.Model on date_field in DateObject with 'my/template.html' %}
    
    Base.Model is the model you'd like to pull from
    date_field is the date or datetime field in the aforementioned model
    DateObject is the date / datetime obj of the month to render (Defaults to current)
    'my/template.html' is the template to render (Defaults to gencal/gencal.html)

    """
    bits = token.contents.split()
    if len(bits) > 9:
        raise TemplateSyntaxError, "simple_gencal takes a maximum of 8 arguments"
    try:
        if (bits[5] == 'in'):
            pass
    except IndexError:
        # This means it wasn't passed in, so assign the defaults.
        # Need to investigate *args and **args b/c what if 
        # they want to define a template but not the month to render?
        pass
        
    # FIXME: Need to add checks in for simple_gencal to make sure people are using the correct arguments and such
    return SimpleGencalNode(bits[2], bits[4], bits[6], bits[8])

@register.inclusion_tag('gencal/gencal.html') # TODO: Make this generic
def gencal(date = datetime.datetime.today(), cal_items=[]):
    """
    This will generate a calendar. It expects the year & month (in datetime format)
    and a list of dicts in the following format:

    cal_items = [{ 'day':datetime(2008,1,30), 'title':"Concert at Huckelberries", 'class':"concert",    'url':'/foo/2' },
                 { 'day':datetime(2008,2,4),  'title':"BBQ at Mom\'s house",      'class':"restaurant", 'url':'/restaurants/9' }]

    A listing of variables and their meanings:

    * day is the datetime of the day you'd like to reference
    * title is the text of the event that will be rendered
    * url is the url to the object you'd like to reference, it isn't necessary. If you don't wish to pass in a url, just pass it as None
    * class is a non-necessary field that will apply class="your_entry" to the list item

    My suggested urls.py file is:
    *Note: Its important to name your year/month url gencal or the backwards/forwards links won't work*;

    ::

        urlpatterns = patterns('',
            url(r'^(?P<year>\d{4})/(?P<month>\d+)/$', 'online_department.schedule.views.index', name='gencal'),
            (r'^$', 'online_department.schedule.views.index'),
        )

    The CSS I use to make it look good is:

    ::

        <style type="text/css">
        table.cal_month_calendar caption { text-align: center; text-size: 15px; background: none;}
        table.cal_month_calendar table { width: 455px;}
        table.cal_month_calendar th,td { width: 65px;}
        table.cal_month_calendar th { text-align: center; }
        table.cal_month_calendar td { height: 65px; position: relative;}
        table.cal_month_calendar td.cal_not_in_month { background-color: #ccc;}
        table.cal_month_calendar div.table_cell_contents { position: relative; height: 65px; width: 65px;}
        table.cal_month_calendar div.month_num { position: absolute; top: 1px; left: 1px; }
        table.cal_month_calendar ul.event_list { list-style-type: none; padding: 15px 0 0 0; margin: 0;}
        table.cal_month_calendar { border-collapse: collapse; }
        table.cal_month_calendar th { color: white; background: black;}
        table.cal_month_calendar td, th { border: 1px solid black; }
        </style>

    """
    # Set the values pulled in from urls.py to integers from strings
    year, month = date.year, date.month
    
    # account for previous month in case of Jan
    lastmonth, nextmonth = month - 1, month + 1
    lastyear, nextyear = year, year
    if lastmonth == 0:
        lastmonth = 12
        lastyear -= 1
    elif nextmonth == 13:
        nextmonth = 1
        nextyear += 1

    prev_date = datetime.date(lastyear, lastmonth, 1)
    next_date = datetime.date(nextyear, nextmonth, 1)

    month_range = calendar.monthrange(year, month)
    first_day_of_month = datetime.date(year, month, 1)
    last_day_of_month = datetime.date(year, month, month_range[1])
    num_days_last_month = calendar.monthrange(year, lastmonth)[1]

    # first day of calendar is:
    #
    # first day of the month with days counted back (timedelta)
    # until Sunday which is day-of-week_num plus one (for the
    # 0 offset)
    #

    first_day_of_calendar = first_day_of_month - datetime.timedelta(first_day_of_month.weekday())

    # last day of calendar is:
    #
    # the last day of the month with days added on (timedelta)
    # until saturday[5] (the last day of our calendar)
    #

    last_day_of_calendar = last_day_of_month + datetime.timedelta(12 - last_day_of_month.weekday())

    events_by_day = defaultdict(list)
    for event in cal_items:
        d = event['day']
        d = datetime.date(d.year, d.month, d.day)
        events_by_day[d].append({'title':event['title'], 'url':event['url'], 'class':event['class'], 'timestamp':event['day'] })

    month_cal = []
    week = []
    week_headers = [header for header in calendar.weekheader(2).split(' ')]
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        cal_day = {'day': day, 'event': events_by_day[day], 'in_month': (day.month == month)}
        week.append(cal_day)        # Add the current day to the week
        if day.weekday() == 6:      # When Sunday comes, add the week to the calendar
            month_cal.append(week)
            week = []               # Reset the week
        day += datetime.timedelta(1)        # set day to next day (in datetime object)

    return {'month_cal': month_cal, 'headers': week_headers, 'date':date, 'prev_date':prev_date, 'next_date':next_date }
