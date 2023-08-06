import os,errno,hashlib,zipfile,json,shutil,datetime,pickle,requests,random,queue,ast,time,threading,csv as csvm
from .status import error,success,info,config_status as statusc
from .functions.functions import *
from requests_toolbelt import MultipartEncoder
from . import filelock
from uuid import uuid4
from flask import Flask,request,send_file
from .functions.subclass import subclass
from .operators import *
from pathlib import Path

FileLock = filelock.FileLock

class Uploader_Thread(threading.Thread):
    def __init__(self, q):
        super(Uploader_Thread, self).__init__()
        self.q = q
        self.state = True
        self.db_ob = None
        self.strem_loop_pause = 5

    def onThread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))

    def run(self):
        while self.state:
            try:
                function, args, kwargs = self.q.get(timeout=self.strem_loop_pause)
                function(*args, **kwargs)
            except queue.Empty:
                self.idle()

    def idle(self):
      #FIRST DOWNLOAD THEN UPLOAD
      #print(self.db_ob.upload_pending)
      if self.db_ob.upload_pending:
        self.db_ob.extract_data_from_log()
      
      if self.db_ob.get_last_hash_server() != self.db_ob.lhash:
        if self.db_ob.lhash == 'NA': self.db_ob.download_full()
        else:self.db_ob.download_changes()

    def Write_temp(self,data):
        pass

class server():
  def __init__(self):
    self.app = Flask('Pi7db Server')
    self.app.debug = True
    self.start_routes()

  def start_routes(self):
    @self.app.route('/')
    def index():
       return 'Pi7DB Stream Server V.0.1'
    
    @self.app.route('/download-data',methods=['POST'])
    def download_data():
      data = pickle.loads(request.get_data())
      db = pi7db(data['dbname'],data['dbpath'])
      keys = {}
      trash_ky = {}
      for line in db.reverse_readline(db.get_server_log_name()): 
         if line.startswith(data['hash']):break
         else:
          line = line.split('/')
          last_hex = line[0]
          if line[3] == 'update':
            if line[1] not in keys:keys[line[1]] = {}
            if line[1] in keys and line[2] not in keys[line[1]]:keys[line[1]][line[2]] = []
            if line[1] in keys and line[2] in keys[line[1]] and line[-1][:-1] not in keys[line[1]][line[2]]:
              keys[line[1]][line[2]].append(line[-1][:-1])
          else:
            if line[1] not in trash_ky:trash_ky[line[1]] = {}
            if line[1] in trash_ky and line[2] not in trash_ky[line[1]]:trash_ky[line[1]][line[2]] = []
            if line[1] in trash_ky and line[2] in trash_ky[line[1]] and line[-1][:-2] not in trash_ky[line[1]][line[2]]:
              trash_ky[line[1]][line[2]].append(line[-1][:-1])
      
      rdata = {}
      for x_col in keys:
       rdata[x_col] = {} 
       for x_doc in keys[x_col]:
        try:docd = db.read(x_col,x_doc)['data'][0]
        except:continue
        xdata = {}
        for x_key in keys[x_col][x_doc]:
          xdata = db.nesUpdate(xdata,db.ex_data_fr_dic(x_key[2:].split(x_key[:2]),docd,x_key[:2],dict()))
        if xdata:rdata[x_col][x_doc] = xdata
      
      return pickle.dumps({'hash':db.read('db_Stream_Config','last_change','hash')['data'],'update':rdata,'trash':trash_ky})



    @self.app.route('/upload-data',methods=['POST'])
    def upload_data():
      data = pickle.loads(request.get_data())
      db = pi7db(data['dbname'],data['dbpath'])
      db.on_server = True
      lhash = None
      if data['action'] == 'update':
        db.update(data['col'],data['doc'],data['data'],write=True)
        lhash = db.write_log(data['col'],data['doc'],data['data'],'update')
        db.write('db_Stream_Config','last_change',{'hash':lhash})
      elif data['action'] == 'trash':
        for x_col in data['data']:
          for x_doc in data['data'][x_col]:
            if x_doc == 'None':
              try:
                db.trash(x_col)
                lhash = db.write_log(x_col,"None",["None",{}],'trash')
              except:pass
              break
            for x_tr_q in data['data'][x_col][x_doc]:
               t_query = ast.literal_eval(x_tr_q)
               try:
                db.trash(x_col,x_doc,t_query[0],**t_query[1])
                lhash = db.write_log(x_col,x_doc,[t_query[0],t_query[1]],'trash')
               except:pass
      if lhash:db.write('db_Stream_Config','last_change',{'hash':lhash})
      
      return {'status':'D','hash':lhash}

    @self.app.route('/last-hash',methods=['POST'])
    def last_hash():
      data = pickle.loads(request.get_data())
      db = pi7db(data['dbname'],data['dbpath'])
      return {'hash':db.read('db_Stream_Config','last_change','hash')['data']}

    @self.app.route('/upload-full',methods=['POST'])
    def upload_full():
      dbhx = f"{uuid4().hex}.zip"
      file = request.files['file']
      file.save(dbhx)
      with zipfile.ZipFile(dbhx, 'r') as zip_ref:
         zip_ref.extractall('.')
      os.remove(dbhx)
      data = dict(request.form)
      db = pi7db(data['dbname'],data['dbpath'])
      lhash = db.write_log('Stream_test','Stream_test',{'test':'test'},'update')
      db.write('db_Stream_Config','last_change',{'hash':lhash})
      return {'status':'D','hash':lhash}
    
    @self.app.route('/download-full',methods=['POST'])
    def download_full():
      data = pickle.loads(request.get_data())
      dbpath = os.path.join(data['dbpath'],data['dbname'])
      return "Record not found", 400
      if not os.path.exists(dbpath):return "Record not found", 400
      dbhx = uuid4().hex
      if not os.path.exists('tmpDown'):os.makedirs('tmpDown')
      zf = zipfile.ZipFile(f"tmpDown/{dbhx}.zip", "w")
      db = pi7db(data['dbname'],data['dbpath'])
      for dirname, subdirs, files in os.walk(dbpath+'/'):
          zf.write(dirname)
          for filename in files:
              zf.write(os.path.join(dirname, filename))
      zf.close()
      lhash = db.write_log('Stream_test','Stream_test',{'test':'test'},'update')
      db.write('db_Stream_Config','last_change',{'hash':lhash})
      return send_file(f"{os.getcwd()}/tmpDown/{dbhx}.zip",as_attachment='true')

class pi7db:
  def __init__(self,db_name,db_path=""):
   self.stream = False
   self.db_np,self.db_path,self.recover_croupt,self.db_name,self.temp_limt = os.path.join(db_path,db_name),db_path,False,db_name,120
   self.config_file,self.coll_name = os.path.join(self.db_np,db_name),None
   self.log_path = os.path.join(self.db_path,'Logs')
   if not os.path.exists(self.db_np):os.makedirs(self.db_np)
   if not os.path.exists(f"{self.config_file}"):
    self.config = {'secret-key':None,'doc_size':self.doc_size}
    writedoc(f"{self.config_file}",self.config)
   else:self.config={'secret-key':None,'doc_size':self.doc_size}
   self.doc_size=10000000
   self.recoverbackups()
  
  def recoverbackups(self):
    for x in extractbackups(f"{self.db_np}"):
      try:os.replace(x, x.replace('.backup',''))
      except:pass

  def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'recover_croupt':
          self._recover_croupt = statusc.recover_status = value
        if name == 'doc_size' and self.config:
          self.config['doc_size'] = value
        if name == 'stream' and value:
          q = queue.Queue()
          self.up_T = Uploader_Thread(q)
          self.up_T.start()
          try:
            doc = self.read('db_Stream_Config','status')['data'][0]
            self.upload_pending = doc['pending']
            self.lhash = doc['hash']
          except:
            self.upload_pending = False
            self.lhash = 'NA'
          self.up_T.db_ob = self
          if self.lhash == 'NA': 
            self.download_full()
          
          if not os.path.exists(self.log_path):os.makedirs(self.log_path)
        if name == 'strem_loop_pause':
          self.up_T.strem_loop_pause = value
  
  def close(self):
    self.up_T.state = False

  def __getattr__(self, attrname):
   if attrname == "temp":
    path=self.coll_name=os.path.join(self.db_np,attrname)
    SubClass = type(attrname,(subclass,),{'key':self.key,'config_file':self.config_file,'p_filter':self.filter,'p_sortdict':self.sortdict,'p_update':self.update,'p_trash':self.trash,'p_write':self.write,'config':self.config,'db_np':self.db_np,'db_name':self.db_name,"temp_limt":self.temp_limt})
    SubClass = SubClass()
    return SubClass
  
  def key(self,password):
   return True
   if isinstance(password,dict):
     if password['secret-key'] is None and self.config['secret-key'] is not None:raise ValueError(error.e6)
     else:key=password['secret-key']
   else:key = hashlib.md5(password.encode()).hexdigest()
   if self.config['secret-key'] is not None:
    if key != self.config['secret-key']:raise ValueError(error.e0)
   else:
     self.config['secret-key'] = key
     writedoc(self.config_file,self.config)

  def changekey(self,old_key,New_key):
   files,old_key,New_key = extractfiles(self.db_np,extract_kwargs({},self.db_name)),hashlib.md5(old_key.encode()).hexdigest(),hashlib.md5(New_key.encode()).hexdigest()
   if old_key == opendoc(self.config_file)['secret-key']:
    for x_js in files:
     writedoc(x_js,opendoc(x_js,old_key),New_key)
    writedoc(self.config_file,{'secret-key':New_key})
   else:raise ValueError(error.e1)

  def rename(self,coll_name,doc_name,new_name):
    path,new_path = os.path.join(self.db_np,coll_name,doc_name),os.path.join(self.db_np,coll_name,new_name)
    if os.path.exists(path):
      self.update(coll_name,doc_name,{"cr_dc_path":new_path})
      os.rename(path,new_path)
      return success.s5(doc_name,new_name)
    else:return error.e7(doc_name)

  def status(self):
    dic = {}
    for f in [f for f in os.scandir(self.db_np) if f.is_dir()]:
      doc = extractfiles(f.path,extract_kwargs({},self.db_name))
      dic[f.name] = {"Total_Files":len(doc),"Doc_Name":map(lambda f:f.split("/")[-1],doc)}
    return dic     
  
  def exists(self,file_name,coll_name=None,**kwargs):
    kwargs = extract_kwargs(kwargs,self.db_name)
    if coll_name is not None:data_files = extractfiles(f"{self.db_np}/{coll_name}",kwargs)
    else:data_files = extractfiles(f"{self.db_np}",extract_kwargs(kwargs,self.db_name))
    for x_file in data_files:
     if file_name == x_file.split('/')[-1]:
      if 'today' in kwargs and kwargs['today']==True:
        if datetime.date.today() == datetime.date.fromtimestamp(Path(x_file).stat().st_mtime):return True
        else:return False
      else:return True
    return False
  
  def get_server_log_name(self):
    return f'{self.log_path}/log_1Server.txt'
  
  def write_log(self,coll_name,file_name,xdata,action):
    l_hash = uuid4().hex[:14]
    server_n = 'Server' if self.on_server else ''
    with FileLock(f"{self.log_path}/log_1{server_n}.txt.lock"):
     with open(f"{self.log_path}/log_1{server_n}.txt" ,'a') as f:
      if action == 'trash':
        log = f'{l_hash}/{coll_name}/{file_name}/{action}/{xdata}\n'
      else:log = f'{l_hash}/{coll_name}/{file_name}/{action}/{self.dic_ex_key(xdata)}\n'
      f.write(log)
    self.upload_pending = True
    self.lhash = l_hash
    return l_hash


  def write(self,coll_name,fn_dict,data=None,write_log=True):
   self.key(self.config)     
   path = os.path.join(self.db_np,coll_name)
   if data is None and isinstance(fn_dict,dict) or all([isinstance(x,dict) for x in fn_dict]):
    if isinstance(fn_dict,list):return writenodoc(path,fn_dict,self.config)
    else:xn_dict={'unid':unid(),**fn_dict};return writenodoc(path,xn_dict,self.config)
   else:
    try:
     data_dict={'unid':unid(),**data}
     data_dict['cr_dc_path'] = f"{path}/{fn_dict}";create_coll(path)
     writedoc(data_dict['cr_dc_path'],data_dict,self.config['secret-key'])
     if self.stream and write_log:self.write_log(coll_name,fn_dict,data,'update')
     return success.s0(fn_dict, coll_name)
    except Exception as e:return error.e4
   
  def update(self,coll_name,file_name=None,data_arg=None,**kwargs):
   self.key(self.config)
   if "where" in kwargs:
     if isinstance(coll_name,str) and isinstance(file_name,dict):
       if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):updatebyfilter(self.filter(coll_name,*kwargs['where'])['data'],file_name,{**self.config,**kwargs,"coll_name":coll_name,"write_func":self.write})
       else:return updatebyfilter(self.filter(coll_name,kwargs['where'])['data'],file_name,{**self.config,**kwargs,"coll_name":coll_name,"write_func":self.write})
     if isinstance(coll_name,dict) and file_name is None:
      if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):updatebyfilter(self.filter(coll_name,*kwargs['where'])['data'],coll_name,{**self.config,**kwargs})
      else:return updatebyfilter(self.filter(kwargs['where'])['data'],coll_name,{**self.config,**kwargs})
   try:
    js_data=opendoc(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key'])
    if isinstance(data_arg,dict):js_data=nes_update(js_data,data_arg,**kwargs)
    else:return error.e2
    writedoc(f"{self.db_np}/{coll_name}/{file_name}",js_data,self.config['secret-key'])
    if self.stream:self.write_log(coll_name,file_name,data_arg,'update')
    return success.s1(1)
   except OSError as e:
    if isinstance(file_name,dict):
     if 'write' in kwargs and kwargs['write']==True:return self.write(coll_name,file_name)
     else:
      if e.errno == errno.ENOENT:return error.e3(None)
    elif e.errno == 2:
      if 'write' in kwargs and kwargs['write']==True:return self.write(coll_name,file_name,data_arg)
      else:return e

  def read(self,coll_name=None,file_name=None,key_name=None,**kwargs):
   self.key(self.config)
   kwargs,data_files,r_data = extract_kwargs(kwargs,self.db_name),[],{"data":[],"status":1}
   if key_name is not None:return {"data":opendoc(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key'])[key_name],"status":1}
   elif file_name is not None:
    if isinstance(file_name,str):data_files=[f"{self.db_np}/{coll_name}/{file_name}"]
    if isinstance(file_name,list):
      if isinstance(file_name[0],tuple):data_files=[f"{self.db_np}/{coll_name}/{'/'.join(x)}" for x in file_name]
      elif isinstance(file_name[0],str):data_files=[f"{self.db_np}/{coll_name}/{x}" for x in file_name]
   elif coll_name is not None:data_files = extractfiles(f"{self.db_np}/{coll_name}",kwargs)
   else:data_files = extractfiles(f"{self.db_np}",kwargs)
   for x_file in data_files[kwargs['f_a']:kwargs['l_a']]:
     o_data = opendoc(x_file,self.config['secret-key'])
     if isinstance(o_data,list):r_data['data'].extend(o_data)
     else:r_data['data'].append(o_data)
   return r_data
    
  def trash(self,coll_name=None,file_name=None,key_name=None,**kwargs):
   self.key(self.config)
   if self.stream:self.write_log(coll_name,file_name,[key_name,kwargs],'trash')
   if len(kwargs):
    if 'dropkey' in kwargs:key_name=kwargs['dropkey']
    if isinstance(coll_name,str) and 'where' in kwargs:
      if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):trashbyfilter(self.filter(coll_name,*kwargs['where'])['data'],key_name,self.config)
      else:trashbyfilter(self.filter(coll_name,kwargs['where'])['data'],key_name,self.config)
      return True
    if 'where' in kwargs and coll_name is None:
      if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):trashbyfilter(self.filter(coll_name,*kwargs['where'])['data'],key_name,self.config)
      else:trashbyfilter(self.filter(kwargs['where'])['data'],key_name,self.config)
      return True
   if key_name is not None and isinstance(key_name,set) or isinstance(key_name,dict):
     tr_data = opendoc(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key'])
     writedoc(f"{self.db_np}/{coll_name}/{file_name}",nes_trash(tr_data,key_name),self.config['secret-key'])
     return success.s2(key_name,file_name)
   elif file_name is not None and isinstance(file_name,str):
     os.remove(f"{self.db_np}/{coll_name}/{file_name}")
     return success.s3(file_name)
   elif coll_name is not None:
     if isinstance(coll_name,str):coll_name = [coll_name]
     if 'IGNORE' in kwargs:
       if isinstance(kwargs['IGNORE'],str):kwargs['IGNORE'] = [kwargs['IGNORE']]
       for x in coll_name:
        for x_file in extractfiles(f"{self.db_np}/{x}",kwargs):os.remove(x_file)
     else:
      for x in coll_name:shutil.rmtree(f"{self.db_np}/{x}", ignore_errors=False, onerror=None)
      return success.s4(",".join(coll_name))
   elif coll_name is None and 'IGNORE_COLLECTION' in kwargs:
      collections = list(self.status().keys())
      if isinstance(kwargs['IGNORE_COLLECTION'],str):kwargs['IGNORE_COLLECTION'] = [kwargs['IGNORE_COLLECTION']]
      for x in kwargs['IGNORE_COLLECTION']:collections.remove(x)
      for x in collections:shutil.rmtree(f"{self.db_np}/{x}", ignore_errors=False, onerror=None)
      return success.s4(",".join(collections))
  
  def dic_ex_key(self,dic, key="", rc=0):
    keys = list(dic.keys())
    if rc == 0 and len(keys) > 1:
      return f'#={"#=".join(keys)}'
    elif len(keys) == 1 and isinstance(dic[keys[0]], dict):
      return self.dic_ex_key(dic[keys[0]], f"{key}{keys[0]}_=", rc + 1)
    else:
      if key == "":return '_=' + keys[0]
      else: return '_=' + key[:-2]

  def ex_data_fr_dic(self,keys, data, typ, rdata):
    if typ == '#=':
      rdata = {}
      for x in keys:
        if x in data: rdata[x] = data[x]
      return rdata
    elif typ == '_=':
      x = keys[0]
      if x in data:
        if x not in rdata: rdata[x] = {}
        if not keys[1:]:
          rdata[x] = data[x]
        else:
          if self.ex_data_fr_dic(keys[1:], data[x], typ, rdata[x]) is None:
            return None
      else:
        return None
    return rdata
  
  def nesUpdate(self,d1, d2):
    for x in d1:
      if x in d2 and isinstance(d1[x],dict) and isinstance(d2[x],dict): self.nesUpdate(d1[x], d2[x])
      else: d2[x] = d1[x]
    return d2
  
  def remove_logs(self,last_hex):
    with FileLock(f"{self.log_path}/log_1.txt.lock"):
      with open(f"{self.log_path}/log_1.txt" ,'r') as filedata:
        inputFilelines = filedata.readlines()
    nowwrite = False
    with FileLock(f"{self.log_path}/log_1.txt.lock"):
      with open(f"{self.log_path}/log_1.txt", 'w') as filedata:
         for textline in inputFilelines:
            if textline.startswith(last_hex):
              nowwrite = True
              continue
            if nowwrite:filedata.write(textline)

  def complete_upload(self):
    dbhx = uuid4().hex
    zf = zipfile.ZipFile(f"{dbhx}.zip", "w")
    for dirname, subdirs, files in os.walk(self.db_np+'/'):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    
    encoder = MultipartEncoder(
       fields={
        'dbpath':self.db_path,'dbname':self.db_name,
        'file': (f'{dbhx}.zip', open(f"{dbhx}.zip", 'rb'), 'application/zip')}
    )
    response = requests.post(
      f"{self.server_url}/upload-full", data=encoder, headers={'Content-Type': encoder.content_type}
    )
    self.upload_pending = False
    self.lhash = response.json()['hash']
    self.write('db_Stream_Config','status',{'pending':False,'hash':self.lhash},False)
    os.remove(f"{dbhx}.zip")
  
  def get_last_hash_server(self):
    try:
      data = {'dbpath':self.db_path,'dbname':self.db_name}
      res = requests.post(url=f"{self.server_url}/last-hash",data=pickle.dumps(data),headers={'Content-Type': 'application/octet-stream'})
      return res.json()['hash']
    except:
      raise Exception("Server Not Online!")

  def download_full(self):
    data = {'dbpath':self.db_path,'dbname':self.db_name}
    with requests.post(f"{self.server_url}/download-full",data=pickle.dumps(data), stream=True) as r:
        if r.status_code==400:
          return False
        r.raise_for_status()
        with open('stream_db_down.zip', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    with zipfile.ZipFile('stream_db_down.zip', 'r') as zip_ref:
         zip_ref.extractall('.')
    os.remove('stream_db_down.zip')
    self.lhash = self.get_last_hash_server()
    self.write('db_Stream_Config','status',{'pending':False,'hash':self.lhash},False)
  
  def download_changes(self):
    data = {'dbpath':self.db_path,'dbname':self.db_name,'hash':self.lhash}
    res = requests.post(url=f"{self.server_url}/download-data",data=pickle.dumps(data),headers={'Content-Type': 'application/octet-stream'})
    data = pickle.loads(res.content)
    for x_col in data['update']:
      for x_doc in data['update'][x_col]:
        db.update(x_col,x_doc,data['update'][x_col]['x_doc'],write=True)

    for x_col in data['trash']:
      for x_doc in data['trash'][x_col]:
            if x_doc == 'None':
              try:self.trash(x_col)
              except:pass
              break
            for x_tr_q in data['trash'][x_col][x_doc]:
               t_query = ast.literal_eval(x_tr_q)
               try:self.trash(x_col,x_doc,t_query[0],**t_query[1])
               except:pass
    self.lhash = res.json()['hash']
    self.write('db_Stream_Config','status',{'pending':False,'hash':self.lhash},False)

  def extract_data_from_log(self):
    keys = {}
    trash_ky = {}
    last_hex = ''
    with FileLock(f"{self.log_path}/log_1.txt.lock"):
     with open(f"{self.log_path}/log_1.txt" ,'r') as f:
      while True:
       line = f.readline()
       if not line:break
       line = line.split('/')
       last_hex = line[0]
       if line[3] == 'update':
         if line[1] not in keys:keys[line[1]] = {}
         if line[1] in keys and line[2] not in keys[line[1]]:keys[line[1]][line[2]] = []
         if line[1] in keys and line[2] in keys[line[1]] and line[-1][:-1] not in keys[line[1]][line[2]]:
           keys[line[1]][line[2]].append(line[-1][:-1])
       else:
         if line[1] not in trash_ky:trash_ky[line[1]] = {}
         if line[1] in trash_ky and line[2] not in trash_ky[line[1]]:trash_ky[line[1]][line[2]] = []
         if line[1] in trash_ky and line[2] in trash_ky[line[1]] and line[-1][:-2] not in trash_ky[line[1]][line[2]]:
           trash_ky[line[1]][line[2]].append(line[-1][:-1])
     
    self.upload_to_server(trash_ky,'trash')

    for x_col in keys:
      for x_doc in keys[x_col]:
        try:docd = self.read(x_col,x_doc)['data'][0]
        except:continue
        xdata = {}
        for x_key in keys[x_col][x_doc]:
          xdata = self.nesUpdate(xdata,self.ex_data_fr_dic(x_key[2:].split(x_key[:2]),docd,x_key[:2],dict()))
        self.upload_to_server(xdata,'update',x_col,x_doc)
    self.remove_logs(last_hex)
    return True
    
  def upload_to_server(self,data,action,x_col=None,x_doc=None):
    data = {'data':data,'action':action,'dbpath':self.db_path,'dbname':self.db_name,'col':x_col,'doc':x_doc,'lhash':self.lhash}
    res = requests.post(url=f"{self.server_url}/upload-data",data=pickle.dumps(data),headers={'Content-Type': 'application/octet-stream'})
    self.upload_pending = False
    self.lhash = res.json()['hash']
    self.write('db_Stream_Config','status',{'pending':False,'hash':self.lhash},False)
    
    
  def sort(self,coll_name,command_tup=None,**kwargs):
   self.key(self.config)
   un_ex_kwargs,kwargs,order = kwargs,extract_kwargs(kwargs,self.db_name),False
   if "order" in kwargs:order = kwargs['order']
   if isinstance(coll_name,set):all_data,command_tup=self.read(**un_ex_kwargs),coll_name
   else:all_data=self.read(coll_name,**un_ex_kwargs)
   r_data = {"data":all_data['data'],"status":1}
   if isinstance(command_tup,set):
    key_tup = "i"+str([[x] for x in command_tup])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(command_tup,str):r_data['data'] = sorted(r_data['data'],key = lambda i: i[command_tup],reverse=order)[kwargs['f_a']:kwargs['l_a']]
   return r_data

  def sortdict(self,dict_list,sort_key,**kwargs):
   kwargs,order,r_data = extract_kwargs(kwargs,self.db_name),False,{"data":dict_list['data'],"status":1}
   if "order" in kwargs:order = kwargs['order']
   if isinstance(sort_key,set):
    key_tup = "i"+str([[x] for x in sort_key])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'][kwargs['f_a']:kwargs['l_a']], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(sort_key,str):r_data['data'][kwargs['f_a']:kwargs['l_a']] = sorted(r_data['data'],key = lambda i: i[sort_key],reverse=order)
   return r_data
  
  def filter(self,*command_tup,**kwargs):
   self.key(self.config)
   un_ex_kwargs,kwargs,F_docs = kwargs,extract_kwargs(kwargs,self.db_name),None
   if "IGNORE" in kwargs:un_ex_kwargs["IGNORE"] = kwargs["IGNORE"]
   if len(command_tup)>=1 and isinstance(command_tup[1],list):command_tup,all_data,F_docs = list(command_tup[2:]),command_tup[0],command_tup[1]
   elif isinstance(command_tup[0],str):command_tup,all_data = list(command_tup[1:]),[command_tup[0]]
   elif 'dict' in kwargs:all_data = kwargs['dict']
   else:
     if 'IGNORE_COLLECTION' in kwargs:
      if isinstance(kwargs['IGNORE_COLLECTION'],str):kwargs['IGNORE_COLLECTION']=[kwargs['IGNORE_COLLECTION']]
     else:kwargs['IGNORE_COLLECTION']=[]
     all_data = [x for x in self.status().keys() if x not in kwargs['IGNORE_COLLECTION']]
   r_data,command_arr= {"data":[],'status':1},[]
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = no_freeze_filter(self,command,all_data,F_docs,kwargs,un_ex_kwargs)
     for x_l in data_get:
      for x in x_l:
       if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_L in no_freeze_filter(self,command_tup[0],all_data,F_docs,kwargs,un_ex_kwargs):
      for x_r in x_L:r_data['data'].append(x_r)
    return r_data
  
  def readkey(self,coll_name=None,**kwargs):
   if not 'key' in kwargs:raise KeyError("Key Is Required")
   self.key(self.config)
   r_data,kwargs = {"data":[],"status":1},extract_kwargs(kwargs,self.db_name)
   if isinstance(kwargs['key'],str):kwargs['key'] = [kwargs['key']]
   if coll_name is not None:data_files = extractfiles(f"{self.db_np}/{coll_name}",kwargs)
   else:data_files = extractfiles(f"{self.db_np}",kwargs)
   for x_file in data_files[kwargs['f_a']:kwargs['l_a']]:
     o_data = opendoc(x_file,self.config['secret-key'])
     if isinstance(o_data,list):
       for x_dict in o_data:
         dic={}
         try:
           for x in kwargs['key']:dic[x] = x_dict[x]
         except:pass
         r_data['data'].append(dic)
     else:
       dic={}
       try:
         for x in kwargs['key']:dic[x] = o_data[x]
       except:pass
       r_data['data'].append(dic)
   return r_data
  
  def reverse_readline(self,filename, buf_size=8192):
    #with FileLock(filename):
     with open(filename, 'rb') as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size)).decode(encoding='utf-8')
            remaining_size -= buf_size
            lines = buffer.split('\n')
            if segment is not None:
                if buffer[-1] != '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        if segment is not None:
            yield segment

class csv:
  def __init__(self,file_path=None):    
   self.file_path = file_path
  
  def csv_read(self,file_path=None,**kwargs):
    if file_path is not None:self.file_path = file_path
    kwargs = extract_kwargs(kwargs,"")
    def checkdigit(num):
      if "no_int" in kwargs:return num
      else:
       if num.isdigit():return int(num)
       else:
         try:return float(num)
         except:return num
    if 'csv_str' in kwargs:csvreader = csvm.reader([x for x in kwargs['csv_str'].splitlines() if x != "" or x.isspace()])
    else:
     with open(self.file_path, 'r') as csvfile:
       csvreader = csvm.reader(csvfile)
    self.fields = list(filter(lambda x: x != "", next(csvreader)))
    rows = [row for row in csvreader]
    self.rows_num = csvreader.line_num
    data = {"data":[],"status":1}
    for row in rows[kwargs['f_a']:kwargs['l_a']]:
     if any(row):
      dic,c = {},0
      for col in row[:len(self.fields)]:
         dic[self.fields[c]] = checkdigit(col)
         c+=1
      data['data'].append(dic)
    return data
  
  def csv_filter(self,*command_tup,**kwargs):
   kwargs = extract_kwargs(kwargs,self.file_path)
   if 'dict' in kwargs:all_data=kwargs.pop('dict')['data']
   else:all_data = self.csv_read(**kwargs)['data']
   r_data,command_arr= {"data":[],'status':1},[]
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = andfilter(command,all_data,kwargs)
     for x in data_get:
      if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_r in andfilter(command_tup[0],all_data,kwargs):r_data['data'].append(x_r)
    return r_data
    
  def csv_write(self,data,file_path=None,**kwargs):
    if 'write' in kwargs and kwargs['write'] is False:
      csv_str = ''
      csv_str+=','.join(list(data['data'][0].keys()))
      csv_str+=''.join([f"{','.join(map(str, x.values()))}\n" for x in data['data']])
      return csv_str
    else:
     with open(file_path, 'w', newline='') as file:
      writer = csvm.writer(file)
      writer.writerow(list(data['data'][0].keys()))
      writer.writerows([x.values() for x in data['data']])
     return {f"Sucesss! {file_path} Is Created."}
  
  def csv_sort(self,dict_data,sort_key,**kwargs):
   kwargs,order,r_data = extract_kwargs(kwargs,self.file_path),False,{"data":dict_data['data'],"status":1}
   if "order" in kwargs:order = kwargs['order']
   if isinstance(sort_key,set):
    key_tup = "i"+str([[x] for x in sort_key])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'][kwargs['f_a']:kwargs['l_a']], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(sort_key,str):r_data['data'][kwargs['f_a']:kwargs['l_a']] = sorted(r_data['data'],key = lambda i: i[sort_key],reverse=order)
   return r_data
  
  def csv_trash(self,command):
   data = self.read()
   for x in data['data']:
     if findDiff(command,x):data['data'].remove(x)
   return data

  def csv_update(self,data_arg=None,**kwargs):
   if "where" in kwargs:
    data = self.csv_read()
    for x in data['data']:
     if findDiff(command,x):x.update(data_arg)
    return data