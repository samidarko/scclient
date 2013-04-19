'''
Created on 8 oct. 2012

@author: Sami Darko
'''
import unittest, datetime
from client import Semiocoder
from xml.dom.minidom import Document

# TODO: ajouter les tests sur Task et History

class Test(unittest.TestCase):

    usr = 'coderoot'
    pwd = 'Semiocoder01'
    extension_id = None
    encoder_id = None
    job1_id = None
    job2_id = None
    joblist_id = None
    
    
    def setUp(self):
        self.con = Semiocoder('http://127.0.0.1:8000', verbose=True)
        self.con.login(self.usr, self.pwd)


    def tearDown(self):
        self.con.logout()
        
        
    def testInit(self):
        pass
        

    def testClient(self):
        
        # test encoders
        encoder1 = self.con.getEncoders()
        self.assertTrue(isinstance(encoder1,Document), "getEncoders() not an XML Document ?")
        self.assertTrue(encoder1.getElementsByTagName('id'), 'No Encoders set in Semiocoder ?')
        self.encoder_id = encoder1.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertTrue(self.encoder_id.isdigit(), 'Encoder id is not a digit')
        encoder2 = self.con.getEncoderDetail(self.encoder_id)
        self.assertTrue(isinstance(encoder2,Document), "getEncoders() not an XML Document ?")
        self.assertEqual(encoder1, encoder1, "same but different ?")

        # test extensions
        extension1 = self.con.getExtensions()
        self.assertTrue(isinstance(extension1,Document), "getExtensions() not an XML Document ?")
        self.assertTrue(extension1.getElementsByTagName('id'), 'No Extension set in Semiocoder ?')
        self.extension_id = extension1.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertTrue(self.extension_id.isdigit(), 'Extension id is not a digit')
        extension2 = self.con.getExtensionDetail(self.extension_id)
        self.assertTrue(isinstance(extension2,Document), 'Not XML result')
        self.assertEqual(encoder1, encoder1, "same but different ?")
        
        # test creation des jobs
        job1 = self.con.setJob('job unit test 1', self.extension_id, self.encoder_id, '-x -z -w 1', 'desc job 1')
        job2 = self.con.setJob('job unit test 2', self.extension_id, self.encoder_id, '-a -b -b 2', 'desc job 2')
        self.assertTrue(isinstance(job1,Document), "setJob() not an XML Document ?")
        self.assertTrue(isinstance(job2,Document), "setJob() not an XML Document ?")
        
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
        
        # test getJobDetail d'un job
        job1 = self.con.getJobDetail(self.job1_id)
        self.assertTrue(isinstance(job1,Document), 'Job1 is not XML result')
        self.assertEqual(job1.getElementsByTagName('id')[0].firstChild.nodeValue, self.job1_id)
        self.assertEqual(job1.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc job 1')
        self.assertEqual(job1.getElementsByTagName('options')[0].firstChild.nodeValue, '-x -z -w 1')
        self.assertEqual(job1.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(job1.getElementsByTagName('name')[0].firstChild.nodeValue, 'job unit test 1')
        self.assertEqual(job1.getElementsByTagName('extension')[0].firstChild.nodeValue, self.extension_id)
        self.assertEqual(job1.getElementsByTagName('encoder')[0].firstChild.nodeValue, self.encoder_id)
        
        # test joblists
        joblist = self.con.setJoblist('joblist unit test', [self.job1_id, self.job2_id, ], 'desc joblist unitest')
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        self.joblist_id = joblist.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertEqual(joblist.getElementsByTagName('id')[0].firstChild.nodeValue, self.joblist_id)
        self.assertEqual(joblist.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(joblist.getElementsByTagName('name')[0].firstChild.nodeValue, 'joblist unit test')
        self.assertEqual(joblist.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc joblist unitest')
        # TODO: tester tag job

        joblist = self.con.getJoblistDetail(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        self.joblist_id = joblist.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertEqual(joblist.getElementsByTagName('id')[0].firstChild.nodeValue, self.joblist_id)
        self.assertEqual(joblist.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(joblist.getElementsByTagName('name')[0].firstChild.nodeValue, 'joblist unit test')
        self.assertEqual(joblist.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc joblist unitest')
        
        
        # test edit
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
        
        # TODO: tester tag job
        joblist = self.con.editJoblist(self.joblist_id, 'joblist unit test modified', [self.job1_id, ], 'desc joblist unitest  modified')
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        self.joblist_id = joblist.getElementsByTagName('id')[0].firstChild.nodeValue
        self.assertEqual(joblist.getElementsByTagName('id')[0].firstChild.nodeValue, self.joblist_id)
        self.assertEqual(joblist.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(joblist.getElementsByTagName('name')[0].firstChild.nodeValue, 'joblist unit test modified')
        self.assertEqual(joblist.getElementsByTagName('description')[0].firstChild.nodeValue, 'desc joblist unitest  modified')
        
        
        schedule = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
        task = self.con.setTask(self.joblist_id, schedule, 'video_1.mkv', True)
        self.assertTrue(isinstance(task, Document), 'Task is not XML result ?')
        self.task_id = task.getElementsByTagName('id')[0].firstChild.nodeValue

        #self.assertEqual(task.getElementsByTagName('schedule')[0].firstChild.nodeValue, schedule)
        self.assertEqual(task.getElementsByTagName('state')[0].firstChild.nodeValue, 'W')
        self.assertEqual(task.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(task.getElementsByTagName('source_file')[0].firstChild.nodeValue, 'video_1.mkv')
        self.assertEqual(task.getElementsByTagName('notify')[0].firstChild.nodeValue, 'True')
        self.assertEqual(task.getElementsByTagName('joblist')[0].firstChild.nodeValue, 'joblist unit test modified')
        
        
        task = self.con.getTaskDetail(self.task_id)
        self.assertEqual(task.getElementsByTagName('id')[0].firstChild.nodeValue, self.task_id)
        self.assertEqual(task.getElementsByTagName('state')[0].firstChild.nodeValue, 'W')
        self.assertEqual(task.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        self.assertEqual(task.getElementsByTagName('source_file')[0].firstChild.nodeValue, 'video_1.mkv')
        self.assertEqual(task.getElementsByTagName('notify')[0].firstChild.nodeValue, 'True')
        self.assertEqual(task.getElementsByTagName('joblist')[0].firstChild.nodeValue, 'joblist unit test modified')
        
        task = self.con.editTask(self.task_id, self.joblist_id, schedule, 'video_1.mkv', False)
        self.assertEqual(task.getElementsByTagName('state')[0].firstChild.nodeValue, 'W')
        self.assertEqual(task.getElementsByTagName('owner')[0].firstChild.nodeValue, self.usr)
        # self.assertEqual(task.getElementsByTagName('source_file')[0].firstChild.nodeValue, 'video_1.mkv')
        self.assertEqual(task.getElementsByTagName('notify')[0].firstChild.nodeValue, 'False')
        self.assertEqual(task.getElementsByTagName('joblist')[0].firstChild.nodeValue, 'joblist unit test modified')
        # test delete
        
        task = self.con.deleteTask(self.task_id)
        self.assertTrue(isinstance(task, Document), 'Task not an XML result ?')
        self.assertEqual(task.getElementsByTagName('success')[0].firstChild.nodeValue, 'Task deleted')
        task = self.con.deleteTask(self.task_id)
        self.assertTrue(isinstance(task, Document), 'Task not an XML result ?')
        self.assertEqual(task.getElementsByTagName('error')[0].firstChild.nodeValue, 'Task does not exist')
        
        job = self.con.deleteJob(self.job1_id)
        self.assertTrue(isinstance(job, Document), 'Job not an XML result ?')
        self.assertEqual(job.getElementsByTagName('success')[0].firstChild.nodeValue, 'Job deleted')
        job = self.con.deleteJob(self.job1_id)
        self.assertTrue(isinstance(job, Document), 'Job not an XML result ?')
        self.assertEqual(job.getElementsByTagName('error')[0].firstChild.nodeValue, 'Job does not exist')
        
        joblist = self.con.deleteJoblist(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist not an XML result ?')
        self.assertEqual(joblist.getElementsByTagName('success')[0].firstChild.nodeValue, 'Joblist deleted')
        joblist = self.con.deleteJoblist(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist not an XML result ?')
        self.assertEqual(joblist.getElementsByTagName('error')[0].firstChild.nodeValue, 'Joblist does not exist')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()