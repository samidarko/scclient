# -*- coding: utf-8 -*-
"""Ce module est permet de générer un client pour les applications Semiocoder et 
de les piloter à distance via l'API qui est mise à disposition.

Ce module embarque sa propre librairie "poster", dernière en date et non modifiée

Example usage:
>>> from scclient import client
>>> con = client.Semiocoder('http://127.0.0.1:8000', verbose=True)
>>> con.login('user', 'password')
>>> con.getEncoders()
<?xml version="1.0" ?>
    <encoders>
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
import os, requests
from HTMLParser import HTMLParser
from xml.dom.minidom import parseString
from xml.etree import cElementTree
from datetime import datetime

# TODO: joblist --> ajouter la definition des jobs en xml ? etc
# TODO: ajouter form.error dans le xml
# TODO: clarifier les messages erreur de l'api

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

    def __init__(self, host_url, login_url = '/login', logout_url = '/logout', api_url = '/api', verbose = False):
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
        self.session = requests.Session()
        
        
    def computeResult(self, result):
        
        try:
            dom = parseString(result.encode('ascii',errors='ignore'))
        except:
            import pdb; pdb.set_trace()
            return 'XML parsing error : ' + result
        if self.verbose:
            print dom.toxml()
        return dom
    
    
#============ Ensemble des méthodes de connexion ===========================
    
# TODO: revoir les méthode de connexion
        
    def login(self, username = None, password = None):
        # TODO: ajouter un attribut is connected et tester
        response = self.session.get(self.host_url+self.login_url)
        self.csrfparser.feed(response.text)
        data = { 'username': username, 'password': password, 'csrfmiddlewaretoken': self.csrfparser.getCsrfToken(), }
        self.session.post(self.host_url+self.login_url,data=data)
        
    def logout(self):
        req = self.session.get(self.host_url+self.logout_url)

        
#============ Ensemble des méthodes get ===========================
        
    def getEncoderDetail(self, object_id):
        """Affiche le détail d'un objet Encoder
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'getencoderdetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        return self.computeResult(response.text)
        

    
    def getEncoders(self):
        """Affiche la liste des objets Encoder
        
        :returns: xml.dom.minidom.Document
        """
        response = self.session.get(self.host_url+self.api_url, params={ 'action' : 'getencoders', })
        return self.computeResult(response.text)
    
    
    def getExtensionDetail(self, object_id):
        """Affiche le détail d'un objet Extension
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'getextensiondetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        return self.computeResult(response.text)
    
    
    def getExtensions(self):
        """Affiche la liste des objets Extension
        
        :returns: xml.dom.minidom.Document
        """
        response = self.session.get(self.host_url+self.api_url, params={ 'action' : 'getextensions', })
        return self.computeResult(response.text)

    
    def getJobDetail(self, object_id):
        """Affiche le détail d'un objet Job
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'getjobdetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        return self.computeResult(response.text)
    
    
    def getJobs(self):
        """Affiche la liste des objets Job
        
        :returns: xml.dom.minidom.Document
        """
        response = self.session.get(self.host_url+self.api_url, params={ 'action' : 'getjobs', })
        return self.computeResult(response.text)
        
    
    def getJoblistDetail(self, object_id):
        """Affiche le détail d'un objet Joblist
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'getjoblistdetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        return self.computeResult(response.text)
        
    
    def getJoblists(self):
        """Affiche la liste des objets Joblist
        
        :returns: xml.dom.minidom.Document
        """
        response = self.session.get(self.host_url+self.api_url, params={ 'action' : 'getjoblists', })
        return self.computeResult(response.text)
        
        
    
    def getTaskDetail(self, object_id):
        """Affiche le détail d'un objet Task
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'gettaskdetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        return self.computeResult(response.text)
        
    
    def getTasks(self):
        """Affiche la liste des objets Task
        
        :returns: xml.dom.minidom.Document
        """
        response = self.session.get(self.host_url+self.api_url, params={ 'action' : 'gettasks', })
        return self.computeResult(response.text)
        
    
    def getHistoryDetail(self, object_id):
        """Affiche le détail d'un objet History
    
        :param object_id: Identifiant de l'objet à afficher
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'gethistorydetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        return self.computeResult(response.text)
        
    
    def getHistories(self):
        """Affiche la liste des objets History
        
        :returns: xml.dom.minidom.Document
        """
        response = self.session.get(self.host_url+self.api_url, params={ 'action' : 'gethistories', })
        return self.computeResult(response.text)
        
        
    def getFiles(self, object_id, target):
        """Télécharge le ou les fichiers associés à l'objet History
        
        :param object_id: Identifiant de l'objet History
        :type object_id: int
        :param target: Chemin du répertoire de destination des fichiers
        :type target: str
        
        :returns: xml.dom.minidom.Document
        """
        params = { 'action' : 'gethistorydetail', 'id' : str(object_id) }
        response = self.session.get(self.host_url+self.api_url, params=params)
        doc = self.computeResult(response.text)
        edoc = cElementTree.fromstring(doc.toxml())
        for path in edoc.findall('.//path'):
            filename = os.path.basename(path.text)
            with open(os.path.join(target, filename), 'wb') as f:
                data = self.session.get(self.host_url+path.text)
                for chunk in data.iter_content(chunk_size = 512 * 1024): # Reads 512KB at a time into memory
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                f.close()
    
    
    def deleteFiles(self, object_id):
        """Supprime le ou les fichiers associés à l'objet History
        
        :param object_id: Identifiant de l'objet History
        :type object_id: int
        
        :returns: xml.dom.minidom.Document
        """
        data = { 'action' : 'deletefiles', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken(), }
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)
        

#============ Ensemble des méthodes add ===========================
        
    def setJob(self, name, extension, encoder, options, description=''):
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
        data = { 'action' : 'setjob', 'name' : name, 'extension' : extension, 'encoder' : encoder, 'options' : options, 
                  'description' : description, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() }
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)
        
        
    def setJoblist(self, name, jobs, description=''):
        """Ajoute un Joblist
    
        :param name: Identifiant de l'objet à afficher
        :type name: str
        :param extension: Liste des object Id des jobs du joblist
        :type extension: list
        :param description: Description du job
        :type description: str
        
        :returns: xml.dom.minidom.Document
        """    
        data = { 'action' : 'setjoblist', 'name' : name, 'description' : description, 
                'job' : jobs, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() }
                  
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)
    
        
        
    def setTask(self, joblist, schedule, source_file, notify=False):
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
        data = {'action': 'settask', 'joblist' : joblist, 'schedule' : datetime.strptime(schedule,'%Y-%m-%d %H:%M'), 
                'notify' : notify, 'csrfmiddlewaretoken': self.csrfparser.getCsrfToken(), }
        
        files = { 'source_file': open(source_file, "rb") }
        response = self.session.post(self.host_url+self.api_url, data=data, files=files)
        return self.computeResult(response.text)
#        
#============ Ensemble des méthodes edit ===========================


    def editJob(self, object_id, name, extension, encoder, options, description=''):
        """Modifie un Job
        
        :param object_id: Object Id de l'objet à modifier
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
        data = { 'action' : 'editjob', 'id' : object_id, 'name' : name, 'extension' : extension, 'encoder' : encoder, 'options' : options, 
                  'description' : description, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() }
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)
        
        
    def editJoblist(self, object_id, name, jobs, description=''):
        """Ajoute un Joblist
        
        :param object_id: Object Id de l'objet à modifier
        :type name: int
        :param name: Identifiant de l'objet à afficher
        :type name: str
        :param extension: Liste des object Id des jobs du joblist
        :type extension: list
        :param description: Description du job
        :type description: str
        
        :returns: xml.dom.minidom.Document
        """
        data = { 'action' : 'editjoblist', 'id' : object_id, 'name' : name, 'description' : description,
                'job' : jobs,  'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() }
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)


    def editTask(self, object_id, joblist, schedule, source_file, notify=False):
        """Ajoute un Task
    
        :param object_id: Object Id de l'objet à modifier
        :type name: int
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
        # TODO: probleme lorsqu'on ajoute de nouveau une video == 2 videos
        data = {'action': 'edittask', 'id' : object_id, 'joblist' : joblist, 'schedule' : datetime.strptime(schedule,'%Y-%m-%d %H:%M'), 
                'notify' : notify, 'csrfmiddlewaretoken': self.csrfparser.getCsrfToken(), }
        
        files = { 'source_file': open(source_file, "rb") }
        response = self.session.post(self.host_url+self.api_url, data=data, files=files)
        return self.computeResult(response.text)
    

#============ Ensemble des méthodes delete ===========================

    def deleteJob(self, object_id):
        """Supprime un Job
        
        :param name: Object Id de l'objet à supprimer
        :type name: int
        
        :returns: xml.dom.minidom.Document
        """
        data = { 'action' : 'deletejob', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() } 
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)
    
    
    def deleteJoblist(self, object_id):
        """Supprime un Joblist
        
        :param name: Object Id de l'objet à supprimer
        :type name: int
        
        :returns: xml.dom.minidom.Document
        """
        data = { 'action' : 'deletejoblist', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() } 
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)
    
    
    def deleteTask(self, object_id):
        """Supprime un Task
        
        :param name: Object Id de l'objet à supprimer
        :type name: int
        
        :returns: xml.dom.minidom.Document
        """
        data = { 'action' : 'deletetask', 'id' : object_id, 'csrfmiddlewaretoken' : self.csrfparser.getCsrfToken() } 
        response = self.session.post(self.host_url+self.api_url, data=data)
        return self.computeResult(response.text)

