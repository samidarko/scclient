'''
Created on 8 oct. 2012

@author: Sami Darko
'''
import unittest
from client import Semiocoder
from xml.dom.minidom import Document

# TODO: ajouter les tests sur Task et History

class Test(unittest.TestCase):

    usr = ''
    pwd = ''
    extension_id = None
    encoder_id = None
    job1_id = None
    job2_id = None
    joblist_id = None
    
    
    def setUp(self):
        self.con = Semiocoder('http://127.0.0.1:8000')
        self.con.login(self.usr, self.pwd)


    def tearDown(self):
        self.con.logout()

    def testClient(self):
        #def testGetEncoder(self):
        result = self.con.getEncoders()
        self.assertTrue(isinstance(result,Document), 'Not XML result')
        self.assertTrue(result.getElementsByTagName('id'), 'No Encoders set in Semiocoder')
        self.encoder_id = result.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertTrue(self.encoder_id.isdigit(), 'Encoder id is not a digit')


        #def testGetExtension(self):
        result = self.con.getExtensions()
        self.assertTrue(isinstance(result,Document), 'Not XML result')
        self.assertTrue(result.getElementsByTagName('id'), 'No Extension set in Semiocoder')
        self.extension_id = result.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertTrue(self.encoder_id.isdigit(), 'Extension id is not a digit')
        
        
        #def testAddJobs(self):
        job1 = self.con.addJob('job unit test 1', self.extension_id, self.encoder_id, '-x -z -w 1', 'desc job 1')
        job2 = self.con.addJob('job unit test 2', self.extension_id, self.encoder_id, '-a -b -b 2', 'desc job 2')
        
        self.assertTrue(isinstance(job1,Document), 'Job1 is not XML result')
        self.assertTrue(isinstance(job2,Document), 'Job2 is not XML result')
        self.job1_id = job1.getElementsByTagName('id')[0].firstChild.nodeValue
        self.job2_id = job2.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertTrue(self.job1_id.isdigit(), 'job1 id is not a digit')
        self.assertTrue(self.job2_id.isdigit(), 'job2 id is not a digit')
        
        self.assertEqual(job1.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc job 1')
        self.assertEqual(job1.getElementsByTagName('options')[0].firstChild.nodeValue, '-x -z -w 1')
        self.assertEqual(job1.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(job1.getElementsByTagName('name')[0].firstChild.nodeValue, 'job unit test 1')
        self.assertEqual(job1.getElementsByTagName('extension')[0].firstChild.nodeValue, self.extension_id)
        self.assertEqual(job1.getElementsByTagName('encoder')[0].firstChild.nodeValue, self.encoder_id)
        
        self.assertEqual(job2.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc job 2')
        self.assertEqual(job2.getElementsByTagName('options')[0].firstChild.nodeValue, '-a -b -b 2')
        self.assertEqual(job2.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(job2.getElementsByTagName('name')[0].firstChild.nodeValue, 'job unit test 2')
        self.assertEqual(job2.getElementsByTagName('extension')[0].firstChild.nodeValue, self.extension_id)
        self.assertEqual(job2.getElementsByTagName('encoder')[0].firstChild.nodeValue, self.encoder_id)

    
        #def testEditJob(self):
        job1 = self.con.getJobDetail(self.job1_id)
        self.assertTrue(isinstance(job1,Document), 'Job1 is not XML result')
        self.assertEqual(job1.getElementsByTagName('id')[0].firstChild.nodeValue, self.job1_id)
        self.assertEqual(job1.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc job 1')
        self.assertEqual(job1.getElementsByTagName('options')[0].firstChild.nodeValue, '-x -z -w 1')
        self.assertEqual(job1.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(job1.getElementsByTagName('name')[0].firstChild.nodeValue, 'job unit test 1')
        self.assertEqual(job1.getElementsByTagName('extension')[0].firstChild.nodeValue, self.extension_id)
        self.assertEqual(job1.getElementsByTagName('encoder')[0].firstChild.nodeValue, self.encoder_id)
        
        self.con.editJob(self.job1_id, 'job unit test 1 modified', self.extension_id, self.encoder_id, '-d -e -f 3', 'desc job 1 modified')
        job1 = self.con.getJobDetail(self.job1_id)
        self.assertTrue(isinstance(job1,Document), 'Job1 is not XML result')
        self.assertEqual(job1.getElementsByTagName('id')[0].firstChild.nodeValue, self.job1_id)
        self.assertEqual(job1.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc job 1 modified')
        self.assertEqual(job1.getElementsByTagName('options')[0].firstChild.nodeValue, '-d -e -f 3')
        self.assertEqual(job1.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(job1.getElementsByTagName('name')[0].firstChild.nodeValue, 'job unit test 1 modified')
        self.assertEqual(job1.getElementsByTagName('extension')[0].firstChild.nodeValue, self.extension_id)
        self.assertEqual(job1.getElementsByTagName('encoder')[0].firstChild.nodeValue, self.encoder_id)
        
        
        #def testAddJoblists(self):
        joblist = self.con.addJoblist('joblist unit test', [self.job1_id, self.job2_id, ], 'desc joblist unitest')
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        self.joblist_id = joblist.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertEqual(joblist.getElementsByTagName('id')[0].firstChild.nodeValue, self.joblist_id)
        self.assertEqual(joblist.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(joblist.getElementsByTagName('name')[0].firstChild.nodeValue, 'joblist unit test')
        self.assertEqual(joblist.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc joblist unitest')
        # TODO: tester tag job

    
        #def testEditJoblist(self):
        joblist = self.con.getJoblistDetail(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        self.joblist_id = joblist.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertEqual(joblist.getElementsByTagName('id')[0].firstChild.nodeValue, self.joblist_id)
        self.assertEqual(joblist.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(joblist.getElementsByTagName('name')[0].firstChild.nodeValue, 'joblist unit test')
        self.assertEqual(joblist.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc joblist unitest')
        # TODO: tester tag job
        joblist = self.con.editJoblist(self.joblist_id, 'joblist unit test modified', [self.job1_id, ], 'desc joblist unitest  modified')
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        self.joblist_id = joblist.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertEqual(joblist.getElementsByTagName('id')[0].firstChild.nodeValue, self.joblist_id)
        self.assertEqual(joblist.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(joblist.getElementsByTagName('name')[0].firstChild.nodeValue, 'joblist unit test modified')
        self.assertEqual(joblist.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc joblist unitest  modified')
        
        
        #def testDeleteJob(self):
        self.assertTrue(isinstance(self.con.getJobDetail(self.job1_id), Document), 'Joblist is not XML result')
        self.con.deleteJob(self.job1_id)
        self.assertTrue(self.con.getJobDetail(self.job1_id), 'compute result : An error has occurred')
        self.assertTrue(isinstance(self.con.getJobDetail(self.job2_id), Document), 'Joblist is not XML result')
        self.con.deleteJob(self.job2_id)
        self.assertTrue(self.con.getJobDetail(self.job2_id), 'compute result : An error has occurred')

        
        #def testDeleteJoblist(self):
        self.assertTrue(isinstance(self.con.getJoblistDetail(self.joblist_id), Document), 'Joblist is not XML result')
        self.con.deleteJoblist(self.joblist_id)
        self.assertTrue(self.con.getJoblistDetail(self.joblist_id), 'compute result : An error has occurred')
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()