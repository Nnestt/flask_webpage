import unittest
from flask import Flask
from app import app, most_job_us, most_job_sg, most_seeked_us, most_seeked_sg, sg_top_skills, sg_top_skills_cat, sg_se_skills, sg_is_skills, us_top_skills, us_top_skills_cat, us_se_skills, us_is_skills
from functions import explodeSkill, getTopXSkill
import pandas as pd

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls): #set up the test client
        cls.app = app.test_client()
        cls.app.testing = True

# test the functions to ensure it returns HTML containing a <div> element ========================================

    def test_most_job_us(self):
        result = most_job_us()
        self.assertIn('<div', result)

    def test_most_job_sg(self):
        result = most_job_sg()
        self.assertIn('<div', result)

    def test_most_seeked_us(self):
        result = most_seeked_us()
        self.assertIn('<div', result)

    def test_most_seeked_sg(self):
        result = most_seeked_sg()
        self.assertIn('<div', result)

    def test_sg_top_skills(self):
        df = pd.read_csv('data\\processed_sg.csv')
        df_exploded = explodeSkill(df)
        top_20_skills_sg = getTopXSkill(df_exploded, 20)
        result = sg_top_skills(top_20_skills_sg)
        self.assertIn('<div', result)

    def test_sg_top_skills_cat(self):
        df = pd.read_csv('data\\processed_sg.csv')
        df_exploded = explodeSkill(df)
        top_20_skills_sg = getTopXSkill(df_exploded, 20)
        result = sg_top_skills_cat(top_20_skills_sg)
        self.assertIn('<div', result)

    def test_sg_se_skills(self):
        result = sg_se_skills()
        self.assertIn('<div', result)

    def test_sg_is_skills(self):
        result = sg_is_skills()
        self.assertIn('<div', result)

    def test_us_top_skills(self):
        df = pd.read_csv('data\\processed_us.csv')
        df_exploded = explodeSkill(df)
        top_20_skills_us = getTopXSkill(df_exploded, 20)
        result = us_top_skills(top_20_skills_us)
        self.assertIn('<div', result)

    def test_us_top_skills_cat(self):
        df = pd.read_csv('data\\processed_us.csv')
        df_exploded = explodeSkill(df)
        top_20_skills_us = getTopXSkill(df_exploded, 20)
        result = us_top_skills_cat(top_20_skills_us)
        self.assertIn('<div', result)

    def test_us_se_skills(self):
        result = us_se_skills()
        self.assertIn('<div', result)

    def test_us_is_skills(self):
        result = us_is_skills()
        self.assertIn('<div', result)

    def test_home_route(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div', result.data)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApp)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(f"All {result.testsRun} test cases passed.")
        print("Success")
    else:
        print(f"{result.testsRun - len(result.failures) - len(result.errors)} out of {result.testsRun} test cases passed.")