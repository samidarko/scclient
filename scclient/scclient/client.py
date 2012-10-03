import poster
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
    
        
    def login(self, username = None, password = None):
        # TODO: ajouter un attribut is connected et tester
        self.opener = poster.streaminghttp.register_openers()
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

        
    def getEncoderDetail(self, object_id):
        """Affichages des détails d'un objet job
    
        :param request: Paramètres de la requête HTTP
        :type request: HttpRequest
        :param object_id: Identifiant de l'objet job à afficher
        :type object_id: int
        
        :returns: HttpResponse
        """
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getencoderdetail&id='+str(object_id))
        return self.computeResult(r)
        

    
    def getEncoders(self):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getencoders')
        return self.computeResult(r)
    
    
    def getExtensionDetail(self, object_id):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getextensiondetail&id='+str(object_id))
        return self.computeResult(r)
    
    def getExtensions(self):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getextensions')
        return self.computeResult(r)
    
    
    def getJobDetail(self, object_id):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjobdetail&id='+str(object_id))
        return self.computeResult(r)
    
    
    def getJobs(self):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjobs')
        return self.computeResult(r)
        
    
    def getJoblistDetail(self, object_id):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjoblistdetail&id='+str(object_id))
        return self.computeResult(r)
        
    
    def getJoblists(self):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=getjoblists')
        return self.computeResult(r)
        
    
    def getTaskDetail(self, object_id):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gettaskdetail&id='+str(object_id))
        return self.computeResult(r)
        
    
    def getTasks(self):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gettasks')
        return self.computeResult(r)
        
    
    def getHistoryDetail(self, object_id):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gethistorydetail&id='+str(object_id))
        return self.computeResult(r)
        
    
    def getHistories(self):
        r = urllib2.urlopen(self.host_url+self.api_url+'?action=gethistories')
        return self.computeResult(r)
    
        
    def setJob(self, name, extension, encoder, options, description):
        params = urllib.urlencode(dict(action='setjob', name=name, extension=extension, encoder=encoder, options=options, 
                                       description=description, csrfmiddlewaretoken=self.csrfparser.getCsrfToken()))
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        resp = urllib2.urlopen(req)
        
        
    def setJoblist(self, name, description, jobs):
        
        data = [('action', 'setjoblist'), ('name', name), ('description', name), ('csrfmiddlewaretoken', self.csrfparser.getCsrfToken()),]
        for job in jobs:
            data.append(('job', job))
        params = urllib.urlencode(data)
        url = self.host_url+self.api_url
        req = urllib2.Request(url, data=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
        resp = urllib2.urlopen(req)
        
        
    def setTask(self, joblist, schedule, source_file, notify=False):
        
        params = {'action': 'settask', 'joblist' : joblist, 'schedule' : schedule.strftime('%Y-%m-%d %H:%M'), 'notify' : notify, 
                  'source_file': open(source_file, "rb"), 'csrfmiddlewaretoken': self.csrfparser.getCsrfToken(), }
        
        datagen, headers = poster.encode.multipart_encode(params)
        
        url = self.host_url+self.api_url
        request = urllib2.Request(url, datagen, headers)
        result = urllib2.urlopen(request)
        
        
        
        