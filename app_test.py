import unittest
from app import search_artist_events, filter_events_by_date

class TestAppFunctions(unittest.TestCase):

    def test_search_artist_events(self):
        events = search_artist_events("Drake")
        self.assertIsNotNone(events)
        self.assertIsInstance(events, list)

    def test_filter_events_by_date(self):
        dummy_events = [
            {
                "name": "Event 1",
                "dates": {"start": {"localDate": "2023-08-13"}}
            },
            {
                "name": "Event 2",
                "dates": {"start": {"localDate": "2023-08-14"}}
            },
            # ... add more dummy events
        ]
        filtered_events = filter_events_by_date(dummy_events, 1)
        self.assertEqual(len(filtered_events), 1)

if __name__ == '__main__':
    unittest.main()
