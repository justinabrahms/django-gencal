import datetime
import calendar
from django.utils.datastructures import SortedDict
from calendar import HTMLCalendar, Calendar
from django.template import register

@register.simple_tag
def gencal(obj_list, year=None, month=None):
    today = datetime.date.today()
    if not year:
        year = today.year
    if not month:
        month = today.month
    return ''.join(ListCalendar(obj_list).formatmonth(year, month))

class ListCalendar(HTMLCalendar):
    """
    This is a calendar object which accepts a ``list`` argument and a
    ``date_field`` keyword argument.. This class will return an HTML
    calendar with links on the days that are present in the list,
    using ``date_field`` as the lookup.
    """

    def __init__(self, cal_items, year=None, month=None, *args, **kwargs):
        today = datetime.date.today()

        if year == None:
            year = today.year
        self.year = year

        if not month:
            month = today.month
        self.month = month

        self.date_field = kwargs.pop('date_field', 'date')

        super(ListCalendar, self).__init__(*args, **kwargs)

        cal_arr = self.monthdatescalendar(year, month)
        month_dict = SortedDict()
        for week in cal_arr:
            for date in week:
                month_dict[date] = []

        for item in cal_items:
            if isinstance(item, dict):
                possible_date = item.get(self.date_field)
            else:
                possible_date = getattr(item, self.date_field)
            if possible_date:
                month_dict[possible_date].append(item)
        self.month_dict = month_dict

    def parse(self):
        """
        Iterates self.cal_items adding one item for each day.
        """

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.

        day is a full date object, rather than just a number like in
        core.
        """
        link = self.get_link(day)
        if link:
            # return link
            return '<td><a href="%s">%d</a></td>' % (self.get_link(day),  day.day)
        return '<td>%d</td>' % (day.day)

    def get_link(self, dt):
        """
        A subclassable function which accepts a date/datetime and
        should return a url to give for that date on a calendar.
        """
        return None

    def monthdates2calendar(self, year, month):
        """
        Function returns a list containing a list of tuples
        (representing a week), the tuples represent a
        ``datetime.date`` for the given day and the weekday associated
        with it.

        This is something that ought to be implemented in core. We
        have monthdatescalendar, monthdayscalendar,
        monthdays2calendar, but no monthdates2calendar.
        """
        return [[(dt, dt.weekday()) for dt in week] for week in self.monthdatescalendar(year, month)]

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.

        Overridden so weeks will use monthdates2calendar, so we have
        access to full date objects, rather than numbers.
        """
        v = []
        a = v.append
 
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdates2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return v
