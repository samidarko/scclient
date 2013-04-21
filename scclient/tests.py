'''
Created on 8 oct. 2012

@author: Sami Darko
'''
import unittest, datetime
from client import Semiocoder
from xml.dom.minidom import Document
from xml.etree import cElementTree

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
        self.assertTrue(isinstance(job1,Document), "setJob() not an XML Document ?")
        ejob1 = cElementTree.fromstring(job1.toxml())
        
        job2 = self.con.setJob('job unit test 2', self.extension_id, self.encoder_id, '-a -b -b 2', 'desc job 2')
        self.assertTrue(isinstance(job2,Document), "setJob() not an XML Document ?")
        ejob2 = cElementTree.fromstring(job2.toxml())

        self.job1_id = ejob1.find('./id').text
        self.job2_id = ejob2.find('./id').text
        self.assertTrue(self.job1_id.isdigit(), 'job1 id is not a digit')
        self.assertTrue(self.job2_id.isdigit(), 'job2 id is not a digit')
        
        self.assertEqual(ejob1.find('./description').text, 'desc job 1')
        self.assertEqual(ejob1.find('./options').text, '-x -z -w 1')
        self.assertEqual(ejob1.find('./owner').text, self.usr)        
        self.assertEqual(ejob1.find('./name').text, 'job unit test 1')
        self.assertEqual(ejob1.find('./extension/id').text, self.extension_id)
        self.assertEqual(ejob1.find('./encoder/id').text, self.encoder_id)
        
        self.assertEqual(ejob2.find('./description').text, 'desc job 2')
        self.assertEqual(ejob2.find('./options').text, '-a -b -b 2')
        self.assertEqual(ejob2.find('./owner').text, self.usr)    
        self.assertEqual(ejob2.find('./name').text, 'job unit test 2')
        self.assertEqual(ejob2.find('./extension/id').text, self.extension_id)
        self.assertEqual(ejob2.find('./encoder/id').text, self.encoder_id)
        
        # test getJobDetail d'un job
        job1 = self.con.getJobDetail(self.job1_id)
        self.assertTrue(isinstance(job1,Document), 'Job1 is not XML result')
        ejob1 = cElementTree.fromstring(job1.toxml())

        self.assertEqual(ejob1.find('./id').text, self.job1_id)
        self.assertEqual(ejob1.find('./description').text, 'desc job 1')
        self.assertEqual(ejob1.find('./options').text, '-x -z -w 1')
        self.assertEqual(ejob1.find('./owner').text, self.usr)        
        self.assertEqual(ejob1.find('./name').text, 'job unit test 1')
        self.assertEqual(ejob1.find('./extension/id').text, self.extension_id)
        self.assertEqual(ejob1.find('./encoder/id').text, self.encoder_id)
        
        # test joblists
        joblist = self.con.setJoblist('joblist unit test', [self.job1_id, self.job2_id, ], 'desc joblist unitest')
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        ejoblist = cElementTree.fromstring(joblist.toxml())
        
        self.joblist_id = ejoblist.find('./id').text
        self.assertEqual(ejoblist.find('./owner').text, self.usr)
        self.assertEqual(ejoblist.find('./name').text, 'joblist unit test')
        self.assertEqual(ejoblist.find('./description').text, 'desc joblist unitest')
        # TODO: tester tag job

        joblist = self.con.getJoblistDetail(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        ejoblist = cElementTree.fromstring(joblist.toxml())
        
        self.assertEqual(ejoblist.find('./id').text, self.joblist_id)
        self.assertEqual(ejoblist.find('./owner').text, self.usr)
        self.assertEqual(ejoblist.find('./name').text, 'joblist unit test')
        self.assertEqual(ejoblist.find('./description').text, 'desc joblist unitest')
        
        # TODO: tester tag job
        joblist = self.con.editJoblist(self.joblist_id, 'joblist unit test modified', [self.job1_id, ], 'desc joblist unitest  modified')
        self.assertTrue(isinstance(joblist, Document), 'Joblist is not XML result')
        ejoblist = cElementTree.fromstring(joblist.toxml())
        
        self.assertEqual(ejoblist.find('./id').text, self.joblist_id)
        self.assertEqual(ejoblist.find('./owner').text, self.usr)
        self.assertEqual(ejoblist.find('./name').text, 'joblist unit test modified')
        self.assertEqual(ejoblist.find('./description').text, 'desc joblist unitest  modified')
        
        
        # test edit
        self.con.editJob(self.job1_id, 'job unit test 1 modified', self.extension_id, self.encoder_id, '-d -e -f 3', 'desc job 1 modified')
        job1 = self.con.getJobDetail(self.job1_id)
        self.assertTrue(isinstance(job1,Document), 'Job1 is not XML result')
        ejob1 = cElementTree.fromstring(job1.toxml())
        
        self.assertEqual(ejob1.find('./id').text, self.job1_id)
        self.assertEqual(ejob1.find('./description').text, 'desc job 1 modified')
        self.assertEqual(ejob1.find('./options').text, '-d -e -f 3')
        self.assertEqual(ejob1.find('./owner').text, self.usr)        
        self.assertEqual(ejob1.find('./name').text, 'job unit test 1 modified')
        self.assertEqual(ejob1.find('./extension/id').text, self.extension_id)
        self.assertEqual(ejob1.find('./encoder/id').text, self.encoder_id)
        

        schedule = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
        task = self.con.setTask(self.joblist_id, schedule, 'video_1.mkv', True)
        self.assertTrue(isinstance(task, Document), 'Task is not XML result ?')
        etask = cElementTree.fromstring(task.toxml())
        
        self.task_id = etask.find('./id').text

        #self.assertEqual(task.getElementsByTagName('schedule')[0].firstChild.nodeValue, schedule)
        self.assertEqual(etask.find('./state').text, 'W')
        self.assertEqual(etask.find('./owner').text, self.usr)
        self.assertEqual(etask.find('./source_file').text, 'video_1.mkv')
        self.assertEqual(etask.find('./notify').text, 'True')
        self.assertEqual(etask.find('./joblist/name').text, 'joblist unit test modified')
        
        
        task = self.con.getTaskDetail(self.task_id)
        self.assertTrue(isinstance(task, Document), 'Task is not XML result ?')
        etask = cElementTree.fromstring(task.toxml())
        
        self.assertEqual(etask.find('./id').text, self.task_id)
        self.assertEqual(etask.find('./state').text, 'W')
        self.assertEqual(etask.find('./owner').text, self.usr)
        self.assertEqual(etask.find('./source_file').text, 'video_1.mkv')
        self.assertEqual(etask.find('./notify').text, 'True')
        self.assertEqual(etask.find('./joblist/name').text, 'joblist unit test modified')
        
        task = self.con.editTask(self.task_id, self.joblist_id, schedule, 'video_1.mkv', False)
        self.assertTrue(isinstance(task, Document), 'Task is not XML result ?')
        etask = cElementTree.fromstring(task.toxml())
        
        self.assertEqual(etask.find('./state').text, 'W')
        self.assertEqual(etask.find('./owner').text, self.usr)
        # FIX: bug when file is submitted again ==> 2 files, etc
        # self.assertEqual(task.getElementsByTagName('source_file')[0].firstChild.nodeValue, 'video_1.mkv')
        self.assertEqual(etask.find('./notify').text, 'False')
        self.assertEqual(etask.find('./joblist/name').text, 'joblist unit test modified')
        
        # TODO: test des erreurs
        
        # test delete
        task = self.con.deleteTask(self.task_id)
        self.assertTrue(isinstance(task, Document), 'Task not an XML result ?')
        etask = cElementTree.fromstring(task.toxml())
        self.assertEqual(etask.find('./success').text, 'Task deleted')
        
        task = self.con.deleteTask(self.task_id)
        self.assertTrue(isinstance(task, Document), 'Task not an XML result ?')
        etask = cElementTree.fromstring(task.toxml())
        self.assertEqual(etask.find('./error').text, 'Task does not exist')
        
        job = self.con.deleteJob(self.job1_id)
        self.assertTrue(isinstance(job, Document), 'Job not an XML result ?')
        ejob = cElementTree.fromstring(job.toxml())
        self.assertEqual(ejob.find('./success').text, 'Job deleted')
        
        job = self.con.deleteJob(self.job1_id)
        self.assertTrue(isinstance(job, Document), 'Job not an XML result ?')
        ejob = cElementTree.fromstring(job.toxml())
        self.assertEqual(ejob.find('./error').text, 'Job does not exist')
        
        joblist = self.con.deleteJoblist(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist not an XML result ?')
        ejoblist = cElementTree.fromstring(joblist.toxml())
        self.assertEqual(ejoblist.find('./success').text, 'Joblist deleted')
        
        joblist = self.con.deleteJoblist(self.joblist_id)
        self.assertTrue(isinstance(joblist, Document), 'Joblist not an XML result ?')
        ejoblist = cElementTree.fromstring(joblist.toxml())
        self.assertEqual(ejoblist.find('./error').text, 'Joblist does not exist')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()