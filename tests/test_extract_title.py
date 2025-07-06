import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
        dkasldkl
        dkakd
        #dasnlkdk
        # test_titelino_uno
        kldak
        ## dasjkdlasjkl;
        """
        self.assertEqual(extract_title(markdown), "test_titelino_uno")

    def test_extract_title_exception(self):
        with self.assertRaises(Exception):
            markdown = """
            dkasldkl
            dkakd
            #dasnlkdk
            #test_titelino_uno
            kldak
            ## dasjkdlasjkl;
            """
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
