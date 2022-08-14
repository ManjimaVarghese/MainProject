from dbconnect import connection
from flask import Flask, redirect,request,session, url_for
from flask.templating import render_template
import time


# from pip._vendor.requests.packages.urllib3.util.connection import select
from builtins import len
import hashlib
import os
# import boto
# import boto.s3
# import sys
# from boto.s3.key import Key


from fileinput import filename
import array
from flask.helpers import make_response, send_file


app=Flask(__name__)
app.secret_key="hai"
@app.route('/')
@app.route('/login')
def main():
    return render_template('login.html')

staticpath = "G:\deduplication_project\deduplication_project\\static\\"


@app.route('/log')
def lg():
    session.clear()
    return redirect(url_for('main'))
@app.route('/regi')
def rg():
    return render_template('registration.html')
@app.route('/frg',methods=['POST'])
def registr():
    c=request.form['name']
    e=request.form['email']
    f=request.form['radio']
    g=request.form['date']
    h=request.form['address']
    i=request.form['mobile']
    j=request.form['password']
    l=request.form['select']
    photo=request.files['image']
    exten = time.strftime("%Y%m%d-%H%M%S")
    photo.save(staticpath +"\\photos\\" +exten+ ".jpg")
    path = "/static/photos/" +exten+ ".jpg"
    qry="insert into registration(name,image,email,gender,date_of_birth,address,mob,password,category,type)value('"+c+"','"+path+"','"+e+"','"+f+"','"+g+"','"+h+"','"+i+"','"+j+"','"+l+"','user')"
    #print(qry)
    cu,cn= connection()
    cu.execute(qry)
    cn.commit()
    return render_template('login.html')             
@app.route('/get',methods=['POST'])
def check():
    a=request.form['name']
    b=request.form['pass']
    cu,cn=connection()
    qry="select * from registration where email='"+a+"' and password='"+b+"'"
    cm=cu.execute(qry)
    res=cu.fetchone()
    # type=session['type']
    if res is not None:
        session['uid']=str(res[0])
        session['type']=str(res[10])
        type=session['type']
        if type=='admin':
            return admin()
        elif type=='provider':
            return provider()
        elif type=='user':
            return render_template('userhome.html')
    else:
        return "<script>alert('Invalid username or password');window.location='/'</script>"
    
    
@app.route('/view_profile')
def view_profile():
    uid=session['uid']
    cu,cn=connection()
    qry="select * from registration where id='"+str(uid)+"'"
    print(qry)
    cm=cu.execute(qry)
    res=cu.fetchone()
    return render_template('viewuser.html', data = res)

@app.route('/edit_profile')
def edit_profile():
    uid = session['uid']
    cu,cn = connection()
    qry = "select * from registration where id = '"+str(uid)+"'"
    print(qry)
    cm = cu.execute(qry)
    res = cu.fetchone()
    return render_template('edit_profile.html', data = res)


@app.route('/edit_post', methods=['POST'])
def edit_post():
    uid = session['uid']
    name = request.form['name']
    email = request.form['email']
    gender = request.form['radio']
    date = request.form['date']
    address = request.form['address']
    mob = request.form['mobile']
    cat = request.form['select']
    photo = request.files['image']
    photo.save(staticpath +"\\photos\\" + ".jpg")
    path = "/static/photos/" + ".jpg"
    
    cu,cn = connection()
    qry = "update registration set name = '"+name+"',image = '"+path+"',email = '"+email+"',gender = '"+gender+"',date_of_birth = '"+date+"',address = '"+address+"',mob = '"+mob+"',category = '"+cat+"' where id = '"+str(uid)+"'"
    print(qry)
    cm = cu.execute(qry)
    res = cn.commit()
    return view_profile()



@app.route('/uplod')
def up():
    return render_template('fileupload.html')


@app.route('/upl_new', methods=['POST'])
def upl_new():

    from  datetime import datetime

    filename=datetime.now().strftime("%Y%m%d%H%M%S")
    cu, cn = connection()
    ud = session['uid']
    f = request.files['filename']
    # print(type(f))
    filedir = '/static/fileupload/' + f.filename  # uploadfile folderinserted

    p = "G:\\deduplication_project\\deduplication_project\\static\\fileupload\\"+filename+f.filename

    f.save(p)

    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

    connectionstring = "DefaultEndpointsProtocol=https;AccountName=sample123lik;AccountKey=jLw4XvM5sS7SWou3mVBqWOYyCSrrcHin4AqXWkScaLAAC+lu/Dh/i623g0l566udVavZ0sRSndtk+AStx9AUmA==;EndpointSuffix=core.windows.net"

    import uuid

    blob_service_client = BlobServiceClient.from_connection_string(connectionstring)

    containername = str(uuid.uuid4())

    # container_client=blob_service_client.create_container(containername)

    blob_client = blob_service_client.get_blob_client(container="sample", blob=filename+f.filename)

    with open(p, "rb") as h:
        k = blob_client.upload_blob(h)
        print(k)

    cu,cn=connection()

    hash="j"

    qry = "insert into upload(filename,uid,hashvalue,date) values('" +filename+f.filename + "','" + ud + "','" + hash + "',CURDATE())"
    # print(qry)
    cu.execute(qry)
    cn.commit()

    return "<script>alert('File uploaded successfully');window.location='/uplod'</script>"




@app.route("/downloadfileazure/<filename>")
def downloadfileazure(filename):
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

    connectionstring = "DefaultEndpointsProtocol=https;AccountName=sample123lik;AccountKey=jLw4XvM5sS7SWou3mVBqWOYyCSrrcHin4AqXWkScaLAAC+lu/Dh/i623g0l566udVavZ0sRSndtk+AStx9AUmA==;EndpointSuffix=core.windows.net"

    import uuid

    blob_service_client = BlobServiceClient.from_connection_string(connectionstring)

    containername = str(uuid.uuid4())

    # container_client=blob_service_client.create_container(containername)

    blob_client = blob_service_client.get_container_client(container="sample")

    with open("G:\\deduplication_project\\deduplication_project\\static\\"+filename, "wb") as h:
        k = blob_client.download_blob(filename).readall()
        h.write(k)

        print(k)

    return send_file("G:\\deduplication_project\\deduplication_project\\static\\"+filename,as_attachment=True)
@app.route('/upl',methods=['POST'])
def fileup():
   
    cu,cn=connection()
    ud=session['uid']
    f = request.files['filename']
    #print(type(f))
    filedir='/static/fileupload/'+f.filename#uploadfile folderinserted


    p="G:\\deduplication_project\\deduplication_project\\static\\fileupload\\"
    f.save(p+f.filename)
    # f.save(filedir)
    #print(f.filename)
    import mmap
   
    m=mmap.mmap( f.fileno(),0,access=mmap.ACCESS_READ)
    ba=bytearray(m)
    ba=bytearray(f.read())
    length=len(ba)
   # print(length)
    for c in ba:
        print(c)
        
    blocksize=8096
    totalblock=int(len(ba)/blocksize)
    #print(totalblock)
    
    
    
    
    remainblock=length-(blocksize*totalblock)
    #print(remainblock)
    
    
    
    lastindx=0;
    #f.filename=ffd
    hash='hex_dig'
    qry="insert into upload(filename,uid,hashvalue,date) values('"+f.filename+"','"+ud+"','"+hash+"',CURDATE())"     
   # print(qry)
    cu.execute(qry)
    cn.commit()
      
    qry="select max(fileid) from upload"
    #print(qry)
    cm=cu.execute(qry)
    res=cu.fetchone() 
    fileid= str(res[0])
    session['fileid']=str(res[0])
    
    
    
    #print(fileid)
    
    
    ids=0
    
    for i in range(totalblock):
        
      #  print(i*blocksize)
       # print(((i+1)*blocksize)-1)
       
        b=[]
        for h in range(8096):
            b.insert(h,ba[(i*blocksize)+h] )
            
        #print(b)
        
        
        
        #type(b)
        #print(type(b))
        q= bytes(b)
        
        #print(q)
        s=hashlib.sha1(q)
        hex_dig = s.hexdigest()
        
        
        qry="select blockid from hashblock where hashvalue='"+hex_dig+"'"
#         print(qry)
        cm=cu.execute(qry)
        res=cu.fetchone() 
        
        if res is not None:
            blkid=str(res[0])
            qry="insert into block(fileid,blockid,indux) values('"+fileid+"','"+blkid+"','"+str(ids)+"') "
#             print(qry)
            cu.execute(qry)
            cn.commit()
            ids=ids+1
        else:
            qry="insert into hashblock(hashvalue) values('"+hex_dig+"')"
 #           print(qry)
            cu.execute(qry)
            cn.commit()
            
            
            #qry="insert into upload(filename,uid,hashvalue,date) values('"+str(ffd)+"','"+ud+"','"+hex_dig+"',CURDATE())"     
            #print(qry)
            #cu.execute(qry)
            #cn.commit()
      
            
            
            qry="select max(blockid) from hashblock"
            
            
            
            
            
 #           print(qry)
            cm=cu.execute(qry)
            res=cu.fetchone() 
            blockid= str(res[0])
            
            
            f=open("C:\\aa\\"+blockid+".txt","wb");
            f.write(bytearray(b))
            f.close()
            
        
            
            
            
            
            
            qry="insert into block(fileid,blockid,indux) values('"+fileid+"','"+blockid+"','"+str(ids)+"') "
#            print(qry)
            
            
            
            
            cu.execute(qry)
            cn.commit()
            ids=ids+1
            
            
        
        
        
        
        
        #print(hex_dig)
        
        
    
    lastindx=totalblock*blocksize
    if remainblock>=0:
        #print("hai hello")
        ss=bytearray(remainblock)
        for i in range(remainblock):
            
            ss.insert(i,ba[lastindx+i])
            
            
        q= bytes(ss)
        
        #print(q)
        s=hashlib.sha1(q)
        hex_dig = s.hexdigest()
        qry="select blockid from hashblock where hashvalue='"+hex_dig+"'"
 #       print(qry)
        cm=cu.execute(qry)
        res=cu.fetchone() 
            
            
            
        if res is not None:
            blkid=str(res[0])
            qry="insert into block(fileid,blockid,indux) values('"+fileid+"','"+blkid+"','"+str(ids)+"') "
  #          print(qry)
            cu.execute(qry)
            cn.commit()
            ids=ids+1
        else:
            qry="insert into hashblock(hashvalue) values('"+hex_dig+"')"
   #         print(qry)
            cu.execute(qry)
            cn.commit()
            
            
            qry="select max(blockid) from hashblock"
#            print(qry)
            cm=cu.execute(qry)
            res=cu.fetchone() 
            blockid= str(res[0])
            
            x="C:\\aa\\"+blockid+".txt"
            f=open("C:\\aa\\"+blockid+".txt","wb");
            f.write(bytearray(ss))
            f.close()
                
                
            qry="insert into block(fileid,blockid,indux) values('"+fileid+"','"+blockid+"','"+str(ids)+"') "
#            print(qry)


            import boto3

            sessionmk = boto3.Session(
                aws_access_key_id='AKIA23KD6ZZB376VCBAB',
                aws_secret_access_key='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',
            )
            s3 = sessionmk.resource('s3')
            s3.meta.client.upload_file(Filename=x, Bucket='testabcdcrypto', Key=str(blockid))
            
            
            
            
            cu.execute(qry)
            cn.commit()
            ids=ids+1
     

    return "<script>alert('FIle uploaded successfully');window.location='/uplod'</script>"


@app.route("/sample")
def sample():
    return render_template("sample.html")


@app.route('/userdownload')
def userdownload():
    return render_template('viewupload.html')
@app.route('/download/<id>')
def down(id):
    cu,cn=connection()
    qry="select  filename from upload where fileid='"+id+"'"
   # print(qry)
    cm=cu.execute(qry)
    res=cu.fetchone()
    r=res[0].split('.')
    ext=r[1]
   
    
    cu,cn=connection()
    qry="select  blockid,indux from block where fileid='"+id+"'  order by indux asc"
    #print(qry)
    
            
    
    b=bytearray(10000)
    indx=0
    
    
    cm=cu.execute(qry)
    res=cu.fetchall() 
    for j in res:
        x=j[0]
        f="C:\\aa\\"+str(x)+".txt"
            
   #     print(f)
        
        
        
        y=j[1]
        
        fh=open(f,'rb')
        ba=fh.read()
        
   #     print(ba)
        
        for k in range(len(ba)):
            b.insert(indx,ba[k])
            indx=indx+1
            
            
    
    
  #  print(indx)
    
    sd=bytearray(indx)
    for i in range(indx):
    #    print(i)
        sd.insert(i,b[i])
               
  #  print(len(sd))
    
    
   # print(sd)       
    m="C:\\bb\\"+"jjj."+ext
    x=open("C:\\bb\\"+"jjj."+ext,"wb");
    x.write(bytearray(sd))
    x.close()
    
    return send_file(m,as_attachment=True)
    
    

        
    return render_template('usershare.html')
              
        
        
        
        
        
        
        
        
@app.route('/uplview')
def ff():
    uid=session['uid']
    cu,cn=connection()
    qry="select  fileid,filename,date from upload where uid='"+uid+"'"
   # print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall() 
    return render_template('viewupload.html',data=res)
@app.route('/delete/<id>')
def dele(id):
    qry="delete from upload where fileid='"+id+"'"
    cu,cn=connection()
    cu.execute(qry)
    cn.commit()
    return ff()

@app.route('/admcreategroup')
def admcreatgroup():
    return render_template('adm_groupadd.html')
@app.route('/addgroup',methods=['POST'])
def grpe():
    cdd=request.form['groupname']
    udf=session['uid']
    cu,cn= connection()
    qry="insert into groups(userid,name) values('"+udf+"','"+cdd+"')"  
    #print(qry)  
    cu,cn= connection()
    cu.execute(qry)
    cn.commit()
    
    qry="select max(groupid) from groups"
    cu,cn=connection()
   
    cm=cu.execute(qry)
    res=cu.fetchone()
    
    session['gid']=str(res[0])
 #   print(res[0])
    
    
    
    qry="select * from registration  where id not in (select userid from member where groupid ='"+str(res[0])+"')"
    cu,cn=connection()
   
    cm=cu.execute(qry)
    res=cu.fetchall()
  #  print(qry) 
    return render_template('adm_groupadd.html', data=res)




@app.route('/mm')
def mm():

    return render_template('changepassword.html')
@app.route('/mms',methods=['POST'])

def chng():
    chn=request.form['username']
    crnt=request.form['crntpsd']
    cu,cn=connection()
    qry="select * from registration where email='"+chn+"' and password='"+crnt+"'"
    cm=cu.execute(qry)
    re=cu.fetchone()

    if re is not None:
       
        nsd=request.form['newpsd']
        csd=request.form['cnpsd']
        if nsd==csd:
            qry="update registration set password='"+csd+"' where email='"+chn+"'"
         #   print(qry)  
            cu,cn= connection()
            cu.execute(qry)
            cn.commit()
            return render_template('login.html')
        else:
            return render_template('changepassword.html')
    
        
        return render_template('login.html')
    else:
        return render_template('changepassword.html')

@app.route('/chadmin')
def chadmin():
    return render_template('adm_changepassword.html')


@app.route('/chadm', methods=['POST'])
def chadm():
    chn = request.form['username']
    crnt = request.form['crntpsd']
    cu, cn = connection()
    qry = "select * from registration where email='" + chn + "' and password='" + crnt + "'"
    cm = cu.execute(qry)
    re = cu.fetchone()

    if re is not None:

        nsd = request.form['newpsd']
        csd = request.form['cnpsd']
        if nsd == csd:
            qry = "update registration set password='" + csd + "' where email='" + chn + "'"
            #   print(qry)
            cu, cn = connection()
            cu.execute(qry)
            cn.commit()
            return render_template('login.html')
        else:
            return render_template('adm_changepassword.html')

        return render_template('login.html')
    else:
        return render_template('changepassword.html')


@app.route('/chprovider')
def chprovider():
    return render_template('provider_changepassword.html')


@app.route('/chprov', methods=['POST'])
def chprov():
    chn = request.form['username']
    crnt = request.form['crntpsd']
    cu, cn = connection()
    qry = "select * from registration where email='" + chn + "' and password='" + crnt + "'"
    cm = cu.execute(qry)
    re = cu.fetchone()

    if re is not None:

        nsd = request.form['newpsd']
        csd = request.form['cnpsd']
        if nsd == csd:
            qry = "update registration set password='" + csd + "' where email='" + chn + "'"
            #   print(qry)
            cu, cn = connection()
            cu.execute(qry)
            cn.commit()
            return render_template('login.html')
        else:
            return render_template('provider_changepassword.html')

        return render_template('login.html')
    else:
        return render_template('provider_changepassword.html')


@app.route('/groupadd')
def gdd():
    return render_template('adm_groupadd.html')
@app.route('/addmembertogroup/<userids>')
def adm_grpadd(userids):
    cu,cn=connection()
   
    grpid=session['gid']
    #qry=""
    
    qry="insert into member(userid,groupid) values('"+str(userids)+"','"+str(grpid)+"')"
    print(qry)
    cu,cn= connection()
    cu.execute(qry)
    cn.commit()
   
    qry="select * from registration where type='user' and  id not in (select userid from member where groupid='"+grpid+"')"
    print(qry)
     
    cu,cn= connection()
   # print(qry)
    cm=cu.execute(qry)
    res1=cu.fetchall() 
    
    return render_template('adm_addgroupmember.html', data=res1)


@app.route('/userhome')
def userh():
    return render_template('userhome.html')
@app.route('/userhomes')    
def az():
    return render_template('userhome.html')
@app.route('/fileupl')
def sre():
    return render_template('fileupload.html')
@app.route('/changepsd')
def kpl():
    return render_template('changepassword.html')
@app.route('/groupss')
def rkd():
    return render_template('viewgroup.html')




@app.route('/share')
def share():
    return render_template('fileupload.html')
@app.route('/shares/<fileid>')
def shr(fileid):
    cu,cn=connection()
    uid=session['uid']
    qry="select name,email,id from registration where id != '"+uid+"'"
   # print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall() 
    print(res)
    return render_template('share.html',data=res,fileid=fileid)   


@app.route('/shareinsert/<fileid>/<toid>')
def shareinsert(fileid,toid):
    dy='individual'
    qry="insert into share(file_id,to_id,type,date) values('"+str(fileid)+"','"+str(toid)+"','"+str(dy)+"',CURDATE())"
    cu,cn= connection()
    cu.execute(qry)
    cn.commit()
    return shr(fileid)
    
@app.route('/groupmember')
def gm():
    return render_template('groupmember.html')
@app.route('/grpmembe/<fileid>')
def groupmember(fileid):
    
    # qry="select max(fileid) from upload"
    # cu,cn=connection()
    #
    # cm=cu.execute(qry)
    # res2=cu.fetchone()
    # #print(res2)
    #
    #
    # fileid= str(res2[0])
    
    
    
    cu,cn=connection()  
    uids=session['uid']

    qry ="select groupid,name from groups where groupid not in (select to_id from share where file_id='"+fileid+"')"
    # qry="select groupid,name from groups  "
    #print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall() 
    #print(res)
    return render_template('groupmember.html',data=res,fileid=fileid)


@app.route('/shared/<groupid>/<fileid>')
def sharedgroups(groupid,fileid):
    
    dys='addgroups'
    
    qry="insert into share(file_id,to_id,type,date) values('"+str(fileid)+"','"+str(groupid)+"','"+dys+"',CURDATE())" 
    #print(qry)     
    
    cu,cn= connection()
    cu.execute(qry)
    cn.commit()
    qry="select groupid,name from groups where groupid not in (select to_id from share where file_id='"+fileid+"')"
    
   
    cm=cu.execute(qry)
    ress1=cu.fetchall() 
    #print(qry)
    return render_template('groupmember.html',data=ress1,fileid=fileid)

   
@app.route('/usershareview')
def view():
    cu,cn= connection()
    uid=session['uid']
    # qry="select distinct share.type,share.date,upload.filename,registration.id,registration.email,registration.name,upload.fileid from share,upload,registration where share.file_id=upload.fileid and upload.uid=registration.id and share.type='individual' and share.to_id='"+uid+"'"
    qry1="select distinct  share.type,share.date,upload.filename,registration.id,registration.email,registration.name,upload.fileid,`groups`.`name` as 'group' from share,upload,registration,member,groups where share.type='addgroups' and member.groupid=share.to_id and member.userid='"+uid+"' and upload.uid=registration.id and  member.groupid=`groups`.`groupid`  AND `share`.`file_id`=`upload`.`fileid`"
    print(qry1)


    qry3="SELECT distinct  share.type,share.date,upload.filename,registration.id,registration.email,registration.name,upload.fileid,`groups`.`name` AS 'group' FROM  groups INNER JOIN `share` ON `share`.`to_id`=`groups`.`groupid` INNER JOIN `upload` ON `upload`.`fileid`=`share`.`file_id` INNER JOIN `registration` ON `registration`.`id`=`upload`.`uid` WHERE `groups`.`groupid`   IN (SELECT `groupid` FROM `member` WHERE userid='"+uid+"')"


    # s="("+qry +") union ("+qry1+")";
    s=qry3
    print(s)
   
    cm=cu.execute(s)
    res=cu.fetchall() 
    #print(res)
    return render_template('usershare.html',data=res)




@app.route('/moreaddviews/<type>/<fileid>')
def moreaddview(type,fileid):
    
    if type=="addgroups":
        cu,cn= connection()
        uid=session['uid']
        
        cu,cn= connection()
        qry="select distinct groups.groupid,groups.name  from groups,share,member where share.to_id=groups.groupid and share.file_id='"+fileid+"' and member.userid='"+uid+"' and groups.groupid=member.groupid"
     #   print(qry)
        cm=cu.execute(qry)
        res=cu.fetchone() 
      #  print(res)
        return render_template('moreaddview.html',data=res)
    else:
        cu,cn= connection()
        qry="select upload.filename,upload.date,registration.email,registration.name from upload,registration where upload.uid=registration.id  and upload.fileid='"+fileid+"'"
       # print(qry)
        cm=cu.execute(qry)
        res=cu.fetchone() 
       # print(res)
        return render_template('individualviews.html',data=res)
        
    
    
@app.route('/groupmemebersview/<id>') 
def groupmemberview(id):
    cu,cn= connection()
    qry="select  registration.name,registration.email from registration,member where member.groupid='"+id+"' and registration.id=member.userid"
    #print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall() 
    #print(res)
    return render_template('viewmembers.html',data=res)


@app.route('/adm_groupmemebersview/<id>')
def adm_groupmemberview(id):

    session["cmid"]=id
    cu,cn= connection()
    qry="select  registration.name,registration.email,member.mid from registration,member where member.groupid='"+id+"' and registration.id=member.userid"
    #print(qry)5ct
    cm=cu.execute(qry)
    res=cu.fetchall()
    #print(res)
    return render_template('adm_viewmembers.html',data=res)



@app.route("/deletemember/<mid>")
def deletemember(mid):
    qry="DELETE FROM `member` WHERE mid='"+mid+"'"
    cu,cn=connection()
    cu.execute(qry)
    cn.commit()

    return adm_groupmemberview(session["cmid"])

@app.route('/groupviews')
def jiijm():
    return render_template('viewgroup.html')

@app.route('/adm_groupsview')
def adm_gr():
    cu,cn= connection()
    uid=session['uid']
    cu,cn= connection()
    qry="select  groupid,userid,name from groups where userid ='"+str(uid)+"' "
    #print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall()
    print(res)
    return render_template('adm_viewgroup.html',data=res)


@app.route('/groupsview')
def user():
    cu,cn= connection()
    uid=session['uid']
    cu,cn= connection()
    qry="SELECT  groups.*,member.groupid FROM groups INNER JOIN member ON member.groupid = groups.groupid WHERE member.userid='"+str(uid)+"'"
    #print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall() 
    print(res)
    return render_template('viewgroup.html',data=res)
    
@app.route('/adm_addmembergroup/<grpid>')
def assw(grpid):
    cu,cn= connection()
    session['gid']=grpid
    qry="select * from registration where type='user' and id not in (select userid from member where groupid='"+grpid+"')"
    #print(qry) 
    cu,cn= connection()
    #print(qry)
    cm=cu.execute(qry)
    res1=cu.fetchall()
    return render_template('adm_addgroupmember.html', data=res1)


@app.route('/adm')
def assswa():
    return render_template('index/index.html')
@app.route('/srw')
def sert():
    import  boto3
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
    conn = boto3.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)


    bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
   
    testfile = "replace this with an actual filename"
    print ('Uploading %s to Amazon S3 bucket %s' % \
    (testfile, bucket_name))
    
    k = Key(bucket)
    k.key = 'my test file'
    k.set_contents_from_filename(testfile,cb=percent_cb, num_cb=10)

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()      




@app.route('/provider')
def provider():
    return prov_home()
@app.route('/prov_home')
def prov_home():
    return render_template('providerhome.html')

@app.route('/provider_reg')
def provider_reg():
    return render_template('provider_reg.html')
@app.route('/provider_post',methods=['POST'])
def provider_post():
    c=request.form['name']
    e=request.form['email']
    f=request.form['radio']
    g=request.form['date']
    h=request.form['address']
    i=request.form['mobile']
    j=request.form['password']
    l=request.form['select']
    photo=request.files['image']
    exten = time.strftime("%Y%m%d-%H%M%S")
    photo.save(staticpath +"\\photos\\" +exten+ ".jpg")
    path = "/static/photos/" +exten+ ".jpg"
    qry="insert into registration(name,image,email,gender,date_of_birth,address,mob,password,category,type)value('"+c+"','"+path+"','"+e+"','"+f+"','"+g+"','"+h+"','"+i+"','"+j+"','"+l+"','provider')"
    #print(qry)
    cu,cn= connection()
    cu.execute(qry)
    cn.commit()
    return render_template('login.html')






@app.route('/prov_upload')
def prov_upload():
    return render_template('prov_fileupload.html')


@app.route('/prov_fileup', methods=['POST'])
def prov_fileup():
    cu, cn = connection()
    ud = session['uid']
    f = request.files['filename']
    # print(type(f))
    filedir = '/static/fileupload/' + f.filename  # uploadfile folderinserted

    p = "G:\\deduplication_project\\deduplication_project\\static\\fileupload\\"
    f.save(p + f.filename)
    # f.save(filedir)
    # print(f.filename)
    import mmap

    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    ba = bytearray(m)
    ba = bytearray(f.read())
    length = len(ba)
    # print(length)
    for c in ba:
        print(c)

    blocksize = 8096
    totalblock = int(len(ba) / blocksize)
    # print(totalblock)




    remainblock = length - (blocksize * totalblock)
    # print(remainblock)



    lastindx = 0;
    # f.filename=ffd
    hash = 'hex_dig'
    qry = "insert into upload(filename,uid,hashvalue,date) values('" + f.filename + "','" + ud + "','" + hash + "',CURDATE())"
    # print(qry)
    cu.execute(qry)
    cn.commit()

    qry = "select max(fileid) from upload"
    # print(qry)
    cm = cu.execute(qry)
    res = cu.fetchone()
    fileid = str(res[0])
    session['fileid'] = str(res[0])

    # print(fileid)


    ids = 0

    for i in range(totalblock):

        #  print(i*blocksize)
        # print(((i+1)*blocksize)-1)

        b = []
        for h in range(8096):
            b.insert(h, ba[(i * blocksize) + h])

        # print(b)



        # type(b)
        # print(type(b))
        q = bytes(b)

        # print(q)
        s = hashlib.sha1(q)
        hex_dig = s.hexdigest()

        qry = "select blockid from hashblock where hashvalue='" + hex_dig + "'"
        #         print(qry)
        cm = cu.execute(qry)
        res = cu.fetchone()

        if res is not None:
            blkid = str(res[0])
            qry = "insert into block(fileid,blockid,indux) values('" + fileid + "','" + blkid + "','" + str(ids) + "') "
            #             print(qry)
            cu.execute(qry)
            cn.commit()
            ids = ids + 1
        else:
            qry = "insert into hashblock(hashvalue) values('" + hex_dig + "')"
            #           print(qry)
            cu.execute(qry)
            cn.commit()

            # qry="insert into upload(filename,uid,hashvalue,date) values('"+str(ffd)+"','"+ud+"','"+hex_dig+"',CURDATE())"
            # print(qry)
            # cu.execute(qry)
            # cn.commit()



            qry = "select max(blockid) from hashblock"

            #           print(qry)
            cm = cu.execute(qry)
            res = cu.fetchone()
            blockid = str(res[0])

            f = open("C:\\aa\\" + blockid + ".txt", "wb");
            f.write(bytearray(b))
            f.close()

            import boto3

            sessioan = boto3.Session(
                aws_access_key_id='AKIA23KD6ZZB376VCBAB',
                aws_secret_access_key='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',
            )
            s3 = sessioan.resource('s3')
            s3.meta.client.upload_file(Filename="C:\\aa\\" + blockid + ".txt", Bucket='testabcdcrypto', Key=str(blockid))

            qry = "insert into block(fileid,blockid,indux) values('" + fileid + "','" + blockid + "','" + str(
                ids) + "') "
            #            print(qry)




            cu.execute(qry)
            cn.commit()
            ids = ids + 1







            # print(hex_dig)

    lastindx = totalblock * blocksize
    if remainblock >= 0:
        # print("hai hello")
        ss = bytearray(remainblock)
        for i in range(remainblock):
            ss.insert(i, ba[lastindx + i])

        q = bytes(ss)

        # print(q)
        s = hashlib.sha1(q)
        hex_dig = s.hexdigest()
        qry = "select blockid from hashblock where hashvalue='" + hex_dig + "'"
        #       print(qry)
        cm = cu.execute(qry)
        res = cu.fetchone()

        if res is not None:
            blkid = str(res[0])
            qry = "insert into block(fileid,blockid,indux) values('" + fileid + "','" + blkid + "','" + str(ids) + "') "
            #          print(qry)
            cu.execute(qry)
            cn.commit()
            ids = ids + 1
        else:
            qry = "insert into hashblock(hashvalue) values('" + hex_dig + "')"
            #         print(qry)
            cu.execute(qry)
            cn.commit()

            qry = "select max(blockid) from hashblock"
            #            print(qry)
            cm = cu.execute(qry)
            res = cu.fetchone()
            blockid = str(res[0])

            f = open("C:\\aa\\" + blockid + ".txt", "wb");
            f.write(bytearray(ss))
            f.close()

            qry = "insert into block(fileid,blockid,indux) values('" + fileid + "','" + blockid + "','" + str(
                ids) + "') "
            #            print(qry)




            cu.execute(qry)
            cn.commit()
            ids = ids + 1

    return "<script>alert('File uploaded successfully');window.location='/prov_upload'</script>"


@app.route('/provview')
def provview():
    uid=session['uid']
    cu,cn=connection()
    qry="select  fileid,filename,date from upload where uid='"+str(uid)+"'"
   # print(qry)
    cm=cu.execute(qry)
    res=cu.fetchall()
    return render_template('prov_viewupload.html',data=res)


@app.route('/del/<id>')
def delt(id):
    qry="delete from upload where fileid='"+id+"'"
    cu,cn=connection()
    cu.execute(qry)
    cn.commit()
    return redirect(url_for('provview'))





@app.route('/prov_view_profile')
def prov_view_profile():
    uid=session['uid']
    cu,cn=connection()
    qry="select * from registration where id='"+str(uid)+"'"
    print(qry)
    cm=cu.execute(qry)
    res=cu.fetchone()
    return render_template('viewprov.html', data = res)


@app.route('/prov_edit_profile')
def prov_edit_profile():
    uid = session['uid']
    cu, cn = connection()
    qry = "select * from registration where id = '" + str(uid) + "'"
    print(qry)
    cm = cu.execute(qry)
    res = cu.fetchone()
    return render_template('prov_edit_profile.html', data=res)


@app.route('/prov_edit_post', methods=['POST'])
def prov_edit_post():
    uid = session['uid']
    name = request.form['name']
    email = request.form['email']
    gender = request.form['radio']
    date = request.form['date']
    address = request.form['address']
    mob = request.form['mobile']
    cat = request.form['select']
    photo = request.files['image']
    photo.save(staticpath + "\\photos\\" + ".jpg")
    path = "/static/photos/" + ".jpg"

    cu, cn = connection()
    qry = "update registration set name = '" + name + "',image = '" + path + "',email = '" + email + "',gender = '" + gender + "',date_of_birth = '" + date + "',address = '" + address + "',mob = '" + mob + "',category = '" + cat + "' where id = '" + str(
        uid) + "'"
    print(qry)
    cm = cu.execute(qry)
    res = cn.commit()
    return prov_view_profile()


@app.route('/admin')
def admin():
    return adm_home()


@app.route('/adm_view_profile')
def adm_view_profile():
    uid=session['uid']
    cu,cn=connection()
    qry="select * from registration where id='"+str(uid)+"'"
    print(qry)
    cm=cu.execute(qry)
    res=cu.fetchone()
    return render_template('viewadm.html', data = res)


@app.route('/adm_providers')
def adm_providers():
    cu,cn=connection()
    qry="select * from registration where type='provider'"
    cm = cu.execute(qry)
    ress1 = cu.fetchall()
    return render_template('adm_providers.html', data=ress1)

@app.route('/adm_providerssearch',methods=['post'])
def adm_providerssearch():
    s=request.form["search"]
    cu,cn=connection()
    qry="select * from registration where type='provider' and name like '%"+s+"%'"
    cm = cu.execute(qry)
    ress1 = cu.fetchall()
    return render_template('adm_providers.html', data=ress1)

@app.route('/adm_home')
def adm_home():
    return render_template('admhome.html')

@app.route('/adm_users')
def adm_users():
    cu,cn=connection()
    qry="select * from registration where type='user'"
    cm = cu.execute(qry)
    ress1 = cu.fetchall()
    return render_template('adm_users.html', data=ress1)


@app.route('/adm_uploads')
def adm_uploads():
    cu,cn=connection()
    qry="SELECT upload.*, registration.* FROM upload INNER JOIN registration ON upload.uid=registration.id where registration.type='provider'"
    cm = cu.execute(qry)
    res = cu.fetchall()
    return render_template('adm_uploads.html', data=res)



if __name__ =='__main__':
    app.run(debug=True)

