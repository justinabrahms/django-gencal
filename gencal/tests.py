from templatetags.gencal import ListCalendar
import unittest
import datetime

class GencalBasicTest(unittest.TestCase):
    def setUp(self):
        obj_list = [{'date':datetime.date.today()},
                    {'date':datetime.date.today() + datetime.timedelta(days=1)},
                    {'date':datetime.date.today() + datetime.timedelta(days=2)}]

        def get_link(self, dt):
            if self.month_dict[dt] != []:
                return "/home/"
            return None
        ListCalendar.get_link = get_link
        
        self.list_cal = ListCalendar(obj_list)

    def test_it(self):
        today = datetime.date.today()
        calendar = ''.join(self.list_cal.formatmonth(today.year, today.month))
        self.assertEqual(3, calendar.count("/home/"))
        


if __name__ == "__main__":
    unittest.main()
