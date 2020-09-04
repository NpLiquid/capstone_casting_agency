import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Movie, Actor, Assignation
from auth import AuthError, requires_auth

class CastingAgencyCase(unittest.TestCase):
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "Batman Lego 7",
            "release_date": "14 July 2021"
        }

        self.wrong_new_movie = {
            "title": "Batman Lego 7",
            "release_date": ""
        }

        self.update_movie = {
            "title": "The NeverEnding Story 7",
            "release_date": "20 December 2021"
        }

        self.update_movie_2 = {
            "title": "The NeverEnding Story New Horizon",
            "release_date": "05 September 2022"
        }

        self.new_actor = {
            "name": "Morgan Freeman",
            "age": 83,
            "gender": "Male"
        }

        self.new_actor_2 = {
            "name": "Marilyn Monroe",
            "age": 36,
            "gender": "Female"
        }

        self.wrong_new_actor = {
            "name": "",
            "age": 83,
            "gender": "Male"
        }

        self.update_actor = {
            "name": "Halle Berry",
            "age": 54,
            "gender": "Female"
        }

        self.update_actor_2 = {
            "name": "Emily Blunt",
            "age": 37,
            "gender": "Female"
        }

        #----------------------------------------------------------------------------#
        # Tokens
        #----------------------------------------------------------------------------#
        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRndERQNks2TEJSMlV4bzJxMUlnVCJ9.eyJpc3MiOiJodHRwczovL2ZzZHUuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNTEzODg4YjVhYmZmMDA2ZDUxMmQzOCIsImF1ZCI6ImNhdSIsImlhdCI6MTU5OTIzMTIzNywiZXhwIjoxNTk5MjM4NDM3LCJhenAiOiJvVEpNZ0pmcXd1MFdCemxZUFhGcGVSS0ZBMEFTNTBLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.jUXiLImrEcAoWwMrnKtCz7zCNQ4kdqLegzWDkUfIiN-duIBDWHqqGH-ECGXnSc5mXl2Bv8ME1Us-HOh8kaupmPWZBIbs0fRuQ33oNJdZUONT0iY-Po9LFchhmYvBM8v56qeGSY0TTwUgQDjbcPCSmq8AcpDpC5FsU54Mmr9qTHQpVLhD1RgCcsfroOs_awh__b3No2jM36niMM5RU-iFR5gnz7Tw9xWQSaHviX9hpdFxyJ5HRJwlmq3T_37J7zOTxweXY2kkUuodeWmtPYliLt0lhlSJv0r0FEi6p4QDxPlsmB0iwOtm0ILSbdEIzGxqAUEsgFapmeo66CrN2A_DyA'
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRndERQNks2TEJSMlV4bzJxMUlnVCJ9.eyJpc3MiOiJodHRwczovL2ZzZHUuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMmZlYjQ2MDQ4ZDAwMDAzN2RiMTQzOCIsImF1ZCI6ImNhdSIsImlhdCI6MTU5OTIzMTI4NSwiZXhwIjoxNTk5MjM4NDg1LCJhenAiOiJvVEpNZ0pmcXd1MFdCemxZUFhGcGVSS0ZBMEFTNTBLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.A3qunUAYDqFPXT73aXMjtRIsnbHujPlwpohiJWr8n2ayta7SW6TrSxFRE-Nkl5DmwnLtNZJO_rjTHC3tNku-Q-f7SvvNIvXyYgzP9SbUcEAzaEvRRDd0hpGtXOIfG58lGX3IOTBLpplbiAiC4F5szncN1BW2bJZ80MvzcWAvmFQ3V5s1ry3LcBuYo9m4Uz0s3i7x_7Bo_5D9AMqdJMUPNH82BQ-3RQ_kH9UhPTOsL-iV16GfErP9DomLEjQJcCjotPd6-xoLgOUsogqLZFig23YXbKERoqcVyIpOcnk2poKhCVbUEYRHN96hXfm0KOEOMwN3_0AiwQ-eTt_ZbIdhRQ'
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRndERQNks2TEJSMlV4bzJxMUlnVCJ9.eyJpc3MiOiJodHRwczovL2ZzZHUuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMjMxN2NiMjJkMWU5MDAzZDQxOWYzMSIsImF1ZCI6ImNhdSIsImlhdCI6MTU5OTIzMTMzNSwiZXhwIjoxNTk5MjM4NTM1LCJhenAiOiJvVEpNZ0pmcXd1MFdCemxZUFhGcGVSS0ZBMEFTNTBLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ZYINncyKRObJp2oFxiEf30-97SmSkS99LkxFtv1p9CDKOOSihmwUQ8Td50EaKITyrhMcKxzRGhTAqLD0HiZiJ10OkkaNJ_cr-zhhIuTTCjLlJTowuhp_2Dos6cd_2zKU7Budq3MwYUUZ_tOX9S28f-yeOtH32BmSte9M8xGj1OJhOdfNXCSYL_F3_k-YTNybjM0TNlpMThlegiX1KnJpBE1-lsONIMa9KHlkA-BogYp_C2AX-888n3v2bUiQ61DR4aSWJKKatzGvC4PZbPzYGC2TP6mMuOxcIGEqFhCwI5NRT2n_QMcTQ-iZ293OLVzNLbwZ6A2NT5Zlk2cD8eMVJQ'

        self.expired_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRndERQNks2TEJSMlV4bzJxMUlnVCJ9.eyJpc3MiOiJodHRwczovL2ZzZHUuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMjMxN2NiMjJkMWU5MDAzZDQxOWYzMSIsImF1ZCI6ImNhdSIsImlhdCI6MTU5OTE1NDgxMywiZXhwIjoxNTk5MTYyMDEzLCJhenAiOiJvVEpNZ0pmcXd1MFdCemxZUFhGcGVSS0ZBMEFTNTBLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.LYyV6RVLNXCHxlxOw9Fj9Yyq9dhif83u63I4yQSKY9P1m_sL5TF4S2jsxx3UtnVPAvVJJjqLAsRF77xu0QFAhlIBSpZtSsHyuuXRIKrSWAgZMBZvJ3PuHmfNQpFfQ9Hetsrz1jsImDPawTqa7Ad-lqyrcmKtuL_6CAr1KVuGGDwLI1DnouzTpj6ml1XpjxFfUVaRRBwc0gCMD2O9l4539GwssMY6-rPYam7mjLBrn_PVMiHMqA_4S2cM6ImSjuQZZoa7IGYkhse68Ao5vJnOZnV_EkPGyF807YYS4WH0ERScFYmY7CFOCzh9QvrVTSJErDWRRZGs4fSzMJ31B-5pKQ'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #----------------------------------------------------------------------------#
    # Test Movie
    #----------------------------------------------------------------------------#

    # Get successful
    #--------------------------------------#
    def test_200_get_movies_casting_assistance(self):
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
    
    def test_200_get_movies_casting_director(self):
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
    
    def test_200_get_movies_executive_producer(self):
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
    
    # Get unauthorized
    #--------------------------------------#
    def test_401_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(self.expired_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Get resource not found
    #--------------------------------------#
    def test_404_get_movies(self):
        res = self.client().get('/movies/horror', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found') 
    
    # Create successful
    #--------------------------------------#
    def test_200_post_movies(self):
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
    
    # Create unauthorized
    #--------------------------------------#
    def test_401_post_movies_casting_assistant(self):
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    def test_401_post_movies_casting_director(self):
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Create unprocessable
    #--------------------------------------#
    def test_422_post_movies(self):
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)}, json=self.wrong_new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')
    
    # Delete successful
    #--------------------------------------#
    def test_200_delete_movies(self):
        res = self.client().delete('/movies/2', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 2). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
        self.assertEqual(movie, None)
    
    # Delete unauthorized
    #--------------------------------------#
    def test_401_delete_movies_casting_assistant(self):
        res = self.client().delete('/movies/3', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    def test_401_delete_movies_casting_director(self):
        res = self.client().delete('/movies/3', headers={'Authorization': "Bearer {}".format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Delete resource not found
    #--------------------------------------#
    def test_404_delete_movies(self):
        res = self.client().delete('/movies/300', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
    
    # Update successful
    #--------------------------------------#
    def test_200_patch_movies_casting_director(self):
        res = self.client().patch('/movies/1', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.update_movie)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
        self.assertEqual(movie.title, 'The NeverEnding Story 7')
    
    def test_200_patch_movies_executive_producer(self):
        res = self.client().patch('/movies/1', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)}, json=self.update_movie_2)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))
        self.assertEqual(movie.title, 'The NeverEnding Story New Horizon')
    
    # Update unauthorized
    #--------------------------------------#
    def test_401_patch_movies(self):
        res = self.client().patch('/movies/2', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)}, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Update resource not found
    #--------------------------------------#
    def test_404_patch_movies(self):
        res = self.client().patch('/movies/300', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
    

    #----------------------------------------------------------------------------#
    # Test Actor
    #----------------------------------------------------------------------------#

    # Get successful
    #--------------------------------------#
    def test_200_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
    
    def test_200_get_actors_casting_director(self):
        res = self.client().get('/actors', headers={'Authorization': "Bearer {}".format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))

    def test_200_get_actors_executive_producer(self):
        res = self.client().get('/actors', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
    
    # Get unauthorized
    #--------------------------------------#
    def test_401_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': "Bearer {}".format(self.expired_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Get resource not found
    #--------------------------------------#
    def test_404_get_actors(self):
        res = self.client().get('/actors/horror', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
    
    # Create successful
    #--------------------------------------#
    def test_200_post_actors_casting_director(self):
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
    
    def test_200_post_actors_executive_producer(self):
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)}, json=self.new_actor_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
    
    # Create unauthorized
    #--------------------------------------#
    def test_401_post_actors(self):
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Create unprocessable
    #--------------------------------------#
    def test_422_post_actors(self):
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.wrong_new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')
    
    # Delete successful
    #--------------------------------------#
    def test_200_delete_actors_casting_director(self):
        res = self.client().delete('/actors/4', headers={'Authorization': "Bearer {}".format(self.casting_director_token)})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 4). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
        self.assertEqual(actor, None)
    
    def test_200_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/2', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 2). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
        self.assertEqual(actor, None)
    
    # Delete unauthorized
    #--------------------------------------#
    def test_401_delete_actors(self):
        res = self.client().delete('/actors/3', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Delete resource not found
    #--------------------------------------#
    def test_404_delete_actors(self):
        res = self.client().delete('/actors/300', headers={'Authorization': "Bearer {}".format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
    
    # Update successful
    #--------------------------------------#
    def test_200_patch_actors_casting_director(self):
        res = self.client().patch('/actors/1', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.update_actor)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
        self.assertEqual(actor.name, 'Halle Berry')
    
    def test_200_patch_actors_executive_producer(self):
        res = self.client().patch('/actors/3', headers={'Authorization': "Bearer {}".format(self.executive_producer_token)}, json=self.update_actor_2)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 3). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(len(data['actor']))
        self.assertEqual(actor.name, 'Emily Blunt')
    
    # Update unauthorized
    #--------------------------------------#
    def test_401_patch_actors(self):
        res = self.client().patch('/actors/2', headers={'Authorization': "Bearer {}".format(self.casting_assistant_token)}, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unauthorized')
    
    # Update resource not found
    #--------------------------------------#
    def test_404_patch_actors(self):
        res = self.client().patch('/actors/300', headers={'Authorization': "Bearer {}".format(self.casting_director_token)}, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
