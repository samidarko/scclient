# -*- coding: utf-8 -*-
"""Ce module est permet de générer un client pour les applications Semiocoder et 
de les piloter à distance via l'API qui est mise à disposition.

Ce module embarque sa propre librairie "poster", dernière en date et non modifiée

Example usage:
>>> from scclient import client
>>> con = client.Semiocoder('http://127.0.0.1:8000', verbose=True)
>>> con.login('user', 'password')
>>> con.getEncoders()
<?xml version="1.0" ?><encoders>
        <encoder>
                <outputflag/>
                <inputflag>-i</inputflag>
                <id>1</id>
                <name>ffmpeg</name>
        </encoder>
</encoders>
<xml.dom.minidom.Document instance at 0x028CD7D8>
>>>
"""

from poster import streaminghttp, encode
from HTMLParser import HTMLParser
import urllib, urllib2, cookielib
from xml.dom.minidom import parseString


class HTMLCSRFParser(HTMLParser):
    '''Parseur dedie a la recuperation du jeton Cross Site Request Forgery
    '''
    csrf = None
    
    def handle_starttag(self, tag, attrs):
        if tag == 'input' and ('name', 'csrfmiddlewaretoken') in attrs:
            for attr in attrs:
                if attr[0] == 'value':
                    self.csrf = attr[1]
                    
    def getCsrfToken(self):
        return self.csrf


class Semiocoder(object):
    '''Cette classe represente un objet Semiocoder.
    
    Elle permet d'interagir avec l'API de l'application cible en fournissant un client qui dispose d'un certain nombre de méthodes telles que login / logout.
    On retrouvra aussi toutes les méthodes necessaires à la creation/suppression modification des jobs, joblists et tasks.
    
    '''

    def __init__(self, host_url, login_url = '/accounts/login', logout_url = '/accounts/logout', api_url = '/api', verbose = False):
        """Constructeur du client
    
        :param host_url: Url de l'application Semiocoder cible
        :type host_url: Str
        :param login_url: Url de login de l'application cible
        :type object_id: Str
        :param logout_url: Url de logout de l'application cible
        :type object_id: Str
        :param api_url: Url de l'API de l'application cible
        :type object_id: Str
        :param verbose: Active le mode verbose
        :type object_id: bool
        
        :returns: objet Semiocoder
    """
        self.host_url = host_url
        self.login_url = login_url
        self.logout_url = logout_url
        self.api_url = api_url
        self.verbose = verbose
        self.csrfparser = HTMLCSRFParser()
        
        
    def computeResult(self, result):
        try:
            dom = parseString(result.read())
        except:
            return 'compute result : An error has occurred'
        if self.verbose:
            print dom.toxml()
        return dom
    
    
#============ Ensemble des méthodes de connexion ===========================
    
# TODO: revoir les méthode de connexion
        
    def login(self, username = None, password = None):
        # TODO: ajouter un attribut is connected et tester
        self.opener = streaminghttp.register_openers()
        self.opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))        
        #urllib2.install_opener(self.opener)
        #opener = poster.streaminghttp.register_openers()

        login_page = urllib2.urlopen(self.host_url+self.login_url)
        self.csrfparser.feed(login_page.read())
        params = urllib.urlencode(dict(username=username, password=password, next=self.api_url, csrfmiddlewaretoken = self.csrfparser.getCsrfToken()))
        req = urllib2.Request(self.host_url+self.login_url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        resp = urllib2.urlopen(req)
        
        
    def logout(self):
        r = urllib2.urlopen(self.host_url+self.logout_url)

        
#============ Ensemble des méthodes get ===========================
        
    def getEncoderDetail(self, object_id):
        """Affiche le détail d'un objet Encoder
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getencoderdetail&id='+str(object_id))
        return self.computeResult(r)
        

    
    def getEncoders(self):
        """Affiche la liste des objets Encoder
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getencoders')
        return self.computeResult(r)
    
    
    def getExtensionDetail(self, object_id):
        """Affiche le détail d'un objet Extension
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getextensiondetail&id='+str(object_id))
        return self.computeResult(r)
    
    def getExtensions(self):
        """Affiche la liste des objets Extension
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getextensions')
        return self.computeResult(r)
    
    
    def getJobDetail(self, object_id):
        """Affiche le détail d'un objet Job
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjobdetail&id='+str(object_id))
        return self.computeResult(r)
    
    
    def getJobs(self):
        """Affiche la liste des objets Job
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjobs')
        return self.computeResult(r)
        
    
    def getJoblistDetail(self, object_id):
        """Affiche le détail d'un objet Joblist
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjoblistdetail&id='+str(object_id))
        return self.computeResult(r)
        
    
    def getJoblists(self):
        """Affiche la liste des objets Joblist
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjoblists')
        return self.computeResult(r)
        
    
    def getTaskDetail(self, object_id):
        """Affiche le détail d'un objet Task
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gettaskdetail&id='+str(object_id))
        return self.computeResult(r)
        
    
    def getTasks(self):
        """Affiche la liste des objets Task
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gettasks')
        return self.computeResult(r)
        
    
    def getHistoryDetail(self, object_id):
        """Affiche le détail d'un objet History
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gethistorydetail&id='+str(object_id))
        return self.computeResult(r)
        
    
    def getHistories(self):
        """Affiche la liste des objets History
        
        :returns: xml.dom.minidom.Document
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gethistories')
        return self.computeResult(r)
    

#============ Ensemble des méthodes add ===========================
        
    def addJob(self, name, extension, encoder, options, description=''):
        """Ajoute un Job
    
        :param name: Identifiant de l'objet à afficher
        :type name: str
        :param extension: Object Id de l'extension à utiliser
        :type extension: int
        :param encoder: Object Id de l'encodeur à utiliser
        :type encoder: int
        :param options: Options du job passées à l'encoder
        :type options: str
        :param description: Description du job
        :type description: str
        
        :returns: xml.dom.minidom.Document
        """
        params = urllib.urlencode(dict(action='addjob', name=name, extension=extension, encoder=encoder, options=options, 
                                       description=description, csrfmiddlewaretoken=self.csrfparser.getCsrfToken()))
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)
        
        
    def addJoblist(self, name, jobs, description=''):
        """Ajoute un Joblist
    
        :param name: Identifiant de l'objet à afficher
        :type name: str
        :param extension: Liste des object Id des jobs du joblist
        :type extension: list
        :param description: Description du job
        :type description: str
        
        :returns: xml.dom.minidom.Document
        """
        data = [('action', 'addjoblist'), ('name', name), ('description', name), ('csrfmiddlewaretoken', self.csrfparser.getCsrfToken()),]
        for job in jobs:
            data.append(('job', job))
        params = urllib.urlencode(data)
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)
        
        
    def addTask(self, joblist, schedule, source_file, notify=False):
        """Ajoute un Task
    
        :param joblist: Object Id du joblist à utiliser
        :type joblist: int
        :param schedule: Liste des object Id des jobs du joblist
        :type schedule: datetime.datetime
        :param source_file: chemin vers le fichier à envoyer
        :type source_file: str
        :param notify: activation de la notification par mail
        :type notify: bool
        
        :returns: xml.dom.minidom.Document
        """
        params = {'action': 'addtask', 'joblist' : joblist, 'schedule' : schedule.strftime('%Y-%m-%d %H:%M'), 'notify' : notify, 
                  'source_file': open(source_file, "rb"), 'csrfmiddlewaretoken': self.csrfparser.getCsrfToken(), }
        
        datagen, headers = encode.multipart_encode(params)
        
        url = self.host_url+self.api_url
        request = urllib2.Request(url, datagen, headers)
        result = urllib2.urlopen(request)
        return self.computeResult(result)
        
#============ Ensemble des méthodes edit ===========================


    def editJob(self, object_id, name, extension, encoder, options, description=''):
        """Modifie un Job
        
        :param name: Object Id de l'objet à modifier
        :type name: int
        :param name: Identifiant de l'objet à afficher
        :type name: str
        :param extension: Object Id de l'extension à utiliser
        :type extension: int
        :param encoder: Object Id de l'encodeur à utiliser
        :type encoder: int
        :param options: Options du job passées à l'encoder
        :type options: str
        :param description: Description du job
        :type description: str
        
        :returns: xml.dom.minidom.Document
        """
        params = urllib.urlencode(dict(action='editjob', id=object_id, name=name, extension=extension, encoder=encoder, options=options, 
                                       description=description, csrfmiddlewaretoken=self.csrfparser.getCsrfToken()))
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)
        
        
    def editJoblist(self, object_id, name, jobs, description=''):
        """Ajoute un Joblist
        
        :param name: Object Id de l'objet à modifier
        :type name: int
        :param name: Identifiant de l'objet à afficher
        :type name: str
        :param extension: Liste des object Id des jobs du joblist
        :type extension: list
        :param description: Description du job
        :type description: str
        
        :returns: xml.dom.minidom.Document
        """
        data = [('action', 'editjoblist'), ('id', object_id), ('name', name), ('description', name), ('csrfmiddlewaretoken', self.csrfparser.getCsrfToken()),]
        for job in jobs:
            data.append(('job', job))
        params = urllib.urlencode(data)
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)

# TODO: editTask    

#============ Ensemble des méthodes delete ===========================

    def deleteJob(self, object_id):
        """Supprime un Job
        
        :param name: Object Id de l'objet à supprimer
        :type name: int
        
        :returns: xml.dom.minidom.Document
        """
        params = urllib.urlencode({ 'action' : 'deletejob', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() } )
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)
    
    
    def deleteJoblist(self, object_id):
        """Supprime un Joblist
        
        :param name: Object Id de l'objet à supprimer
        :type name: int
        
        :returns: xml.dom.minidom.Document
        """
        params = urllib.urlencode({ 'action' : 'deletejoblist', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() } )
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)
    
    def deleteTask(self, object_id):
        """Supprime un Task
        
        :param name: Object Id de l'objet à supprimer
        :type name: int
        
        :returns: xml.dom.minidom.Document
        """
        params = urllib.urlencode({ 'action' : 'deletetask', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() } )
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        result = urllib2.urlopen(req)
        return self.computeResult(result)

