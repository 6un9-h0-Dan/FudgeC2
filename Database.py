# SQL Alchemy stuffs
from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models import Users, ResponseLogs, Implants, ImplantLogs, Campaigns, CampaignUsers

import time, random
class Database():
    def __init__(self):
        engine = create_engine("sqlite:///fudge_2.db?check_same_thread=False")
        self.selectors = {
            "uid": Users.uid,
            "email": Users.user_email
        }
        self.Session = scoped_session(sessionmaker(bind=engine, autocommit=False))
        """:type: sqlalchemy.orm.Session""" # PyCharm type fix. Not required for execution.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Session.remove()

    def raw_query(self, sql_query_string, sqlinput=None):
        return []

    ## -- Queries from here on -- #
    def test(self, email):
        query = self.Session.query(Users).filter(Users.user_email == email)
        for x in query:
            print("-",x.password)
        # rows = self.Session.query(Users).filter(extract('day', Account.created_at) == int(now.day),extract('month', Account.created_at) == now.month).all()
        return query
    def JoinTest(self,user):
        q=self.Session.query(Campaigns.title,Users.user_email,CampaignUsers.write).filter(Users.user_email==user,CampaignUsers.uid==Users.uid).group_by(Campaigns.title).all()
        #q = self.Session.query(Campaigns,CampaignUsers).join(CampaignUsers)
        for x in q:
            print(x)


    ## -- PRIVATE METHODS -- #
    def __get_userid__(self,email):
        # -- Require further improvement i.e try:catch
        query = self.Session.query(Users.uid).filter(Users.user_email == email).first()
        if query[0] == None:
            return False
        else:
            return query[0]
        # TODO: Improve and avoid race conditions.

    def __get_campaignid__(self,campaign):
        #TODO: Improve the Try/Catch
        q = self.Session.query(Campaigns.cid).filter(Campaigns.title==campaign).one()
        if q == None:
            return False
        else:
            print(q[0])
#:-:
    ## -- PUBLIC METHODS -- #
    def Add_User(self, Username, Password, Admin=False):
        #TODO: This needs a more rebust response Try/Except.
        query = self.Session.query(Users.password, Users.uid).filter(Users.user_email==Username).all()
        for x in query:
            # print(query[0][1])
            return False
        print("::")
        users = Users(user_email=Username,password=Password,admin=Admin,last_login=time.time())
        self.Session.add(users)
        self.Session.commit()
        return True
    def Create_Campaign(self, title, email, description="Default"):
        # check user:
        uid=self.__get_userid__(email)
        if uid == False:
            return False
        campaign = Campaigns(title=title,created=time.time(),description=description)
        #c_user = CampaignUsers(cid=,uid=,read=,write=)
        self.Session.add(campaign)
        try:
            self.Session.commit() # flush check if this will work...
            #q=self.Session.query(Campaigns.cid).filter(Campaigns.title==title).one()
            #print("1",q[0])
            if self.Add_CampaignUser(title,email,True,True):
                print("Success adding a new campaign user.")
                return True
        except Exception as e:
            print(e)
            return False

        # Make campaign (check no dup name)
        # Add user to campaign users
        # commit or rollback.
    def Add_CampaignUser(self,CampaignTitle,Email,Read=True,Write=False):
        # a
        cid = self.Session.query(Campaigns.cid).filter(Campaigns.title==CampaignTitle).one()[0]
        uid = self.Session.query(Users.uid).filter(Users.user_email==Email).one()[0]
        print(cid,uid)
        query=CampaignUsers(cid=cid,uid=uid,read=Read,write=Write)
        try:
            self.Session.add(query)
            self.Session.commit()
            return True
        except Exception as e:
            print("Func:Add_CampaignUser:",e)
            return False

    def Get_CampaignInfo(self,campaign,email):
        q = self.Session.query(Campaigns).filter(Campaigns.title==campaign,Users.user_email==email).all()
        for x in q:
            print("User:",email,x.title,x.description,x.created)

    def Get_AllUserCampaigns(self,email):
        q=self.Session.query(Campaigns.cid, Campaigns.title).filter(
            Users.user_email==email,
            CampaignUsers.uid==Users.uid,
            Campaigns.cid==CampaignUsers.cid
        ).group_by(Campaigns.title).all()
        campaignList = []
        campDict = {}
        for x in q:
            campDict[x[0]]=x[1]
            #print(x)
            campaignList.append(x[0])
        return campDict
    def Get_ImplantIDFromTitle(self, CID,ImplantID, Email):
        # -- NOT COMPLETE: ENSURE 'ALL' entry returns a list of implants.
        # -- RETURN ( list:iid(int) )
        a=[]
        if ImplantID == "ALL":
            IID = self.Session.query(Implants).filter(Implants.cid == CID).all()
            for x in IID:
                print(x.iid)
                a.append(x.iid)
        else:
            IID = self.Session.query(Implants).filter(Implants.title == ImplantID).all()
            for element in IID:
                print(element.iid)
                a.append(element.iid)
        return a

    # -- Implant Content --#
    def Add_Implant(self,cid, title, url, beacon,initial_delay,comms_http,comms_dns,comms_binary, description="Implant: Blank description."):
        implant = Implants(cid=cid,title=title)
        IK= random.randint(10000,99999)
        NewImplant = Implants(cid=cid,title=title,description=description,callback_url=url,implant_key=IK,file_hash="0",filename="0",
                              beacon=beacon,
                              initial_delay=initial_delay,
                              comms_http=comms_http,
                              comms_dns=comms_dns,
                              comms_binary = comms_binary
                              )
        self.Session.add(NewImplant)
        try:
            self.Session.commit()
            q=self.Session.query(Implants).first()
            print(q)
            return True
        except Exception as e:
            print("db.Add_Implant: ",e)
            return False



        # uid = self.__get_userid__(email)
        # if uid == False:flask
        #     return False
        # campaign = Campaigns(title=title, created=time.time(), description=description)
        # # c_user = CampaignUsers(cid=,uid=,read=,write=)
        # self.Session.add(campaign)
        # try:
        #     self.Session.commit()  # flush check if this will work...
        #     # q=self.Session.query(Campaigns.cid).filter(Campaigns.title==title).one()
        #     # print("1",q[0])
        #     if self.Add_CampaignUser(title, email, True, True):
        #         print("Success adding a new campaign user.")
        #         return True
        # except Exception as e:
        #     print(e)
        #     return False



    # -- LOGIN CONTENT --#
    def Get_UserObjectLogin(self, email, password):
        # Auths a user and returns user object
        user = self.Session.query(Users).filter(Users.user_email==email, Users.password==password).first()
        if user != None:
            return user
        else:
            return False
    def Get_CampaignNameFromCID(self,cid):
        # -- Clean up --#
        name=self.Session.query(Campaigns.title).filter(Campaigns.cid==cid).first()
        #print(type(name))
        if name == None:
            return "Unknown"
        #print(name.title)
        return name.title
    def Get_UserObject(self, email):
        # Auths a user and returns user object:
        user = self.Session.query(Users).filter(Users.user_email==email).first()
        #user = Users.query.filter_by(user_email==email).first()
        #print(user.password)
        return user
    def Get_AllCampaignImplants(self, cid):
        implant= self.Session.query(Implants.iid, Implants.title, Implants.description, Implants.callback_url, Implants.implant_key).filter(Implants.cid==cid).all()
        if implant ==None:
            print("Campaign has no implants.")
        #print(implant.iid)
        return implant

    def Get_ImplantFromKey(self,IID):
        a = self.Session.query(Implants).filter(Implants.implant_key==IID).first()
        if a != None:
            return a
        else:
            return False

    def Update_ImplantLastCheckIn(self, ImplantKey):
        #IID = self.Session.query(Implants).filter(Implants.implant_key==ImplantKey).first()
        #print(IID, int(time.time()))
        #IID.last_check_in==int(time.time())

        a =self.Session.query(Implants).filter(Implants.implant_key==ImplantKey).update({"last_check_in": (int(time.time()))})
        self.Session.commit()
        #print(a.last_check_in)
        #self.Session.commit()


    def Register_ImplantCommand(self, email, iid, cmd):
        # -- Check if user and iid are allow to work -- #
        # -- Return Types:
        #       disallowed use html style errors?
        #       true false for anti enum?
        #
        uid = self.__get_userid__(email)
        result = self.Session.query(CampaignUsers, Implants).filter(CampaignUsers.uid == uid, Campaigns.cid == CampaignUsers.cid, Implants.cid == Campaigns.cid, Implants.iid ==iid).all()
        # print(result)
        if len(result) == 0:
            print("No Implant <--> User association")
            return False
        for line in result:
            if line[0].write == 0:
                return False
            elif line[0].write ==1:
                # uid
                cid=line[0].cid
                new_implant_log=ImplantLogs(cid=cid,uid=uid,time=time.time(),log_entry=cmd,iid=iid)
                self.Session.add(new_implant_log)
                try:
                    self.Session.commit()
                    q = self.Session.query(ImplantLogs).first()
                    print(q)
                    return True
                except Exception as e:
                    print("db.Register_ImplantCommand: ", e)
                    return False
            else:
                # -- Incase non 0/1 response --#
                return False

    def Register_ImplantResponse(self,UIK,Response):
        # Pull back the first record which matches the UIK, contain both the Campaign the IID is associated from the implant the UIk is associated with.
        info=self.Session.query(Implants,Campaigns).filter(Campaigns.cid==Implants.cid).filter(Implants.implant_key==UIK).first()
        iid = info[0].iid
        cid = info[1].cid
        # print("Record\ncid:    {}\niid:    {}\nentry:  {}\ntime:   {}".format(cid,iid,Response,int(time.time())))
        RL=ResponseLogs(cid=cid, iid=iid, log_entry=Response,time=int(time.time()))
        self.Session.add(RL)
        try:
            self.Session.commit()
        except Exception as E:
            print(E)



    def Get_CampaignImplantResponses(self, cid):
        a=self.Session.query(ResponseLogs).filter(ResponseLogs.cid == cid).all()
        ReturnList=[]
        for x in a:
            a = x.__dict__
            if '_sa_instance_state' in a:
                del a['_sa_instance_state']
            b = self.Session.query(Implants.title).filter(Implants.iid==a['iid']).first()
            if b != None:
                a['title']=b[0]
            ReturnList.append(a)
        return(ReturnList)

        # -- This may be a single or list: Check and convert to list implictly?


    # -- Campaign Settings Content -- #
    def Get_SettingsUsers(self, cid, user):
        # TODO: Create a list of user dicts with name, uid, and read/write to be returned to a table with radio tabs.
        # TODO: Clean up
        User = self.Session.query(Users.user_email, Users.uid).group_by(Users.user_email)
        final=[]
        for x in User:
            tmp={"user":x[0],"uid":x[1]}
            entry = self.Session.query(CampaignUsers).filter(CampaignUsers.cid ==cid, CampaignUsers.uid== x[1]).first()
            print("::")
            if entry != None:
                tmp['read'] =entry.read
                tmp['write'] = entry.write
                # print(entry.read,entry.write)
            else:
                tmp['read'] = 0
                tmp['write'] = 0
            final.append(tmp)

        x = [ i for i in final if i['user'] != user]
        return x

    def Set_UserCampaignReadWrite(self,uid, readwrite):
        # -- UID + 0 None 1 read 2 write
        return

    # -- Reusable Security Checks

    def Verify_UserCanAccessCampaign(self,Users,CID):
        # -- TODO: Reduce line count, and if,elif, and else statment to a cleaner alternative.
        User = self.__get_userid__(Users)
        print(User)
        if User == None:
            return False
        R = self.Session.query(CampaignUsers).filter(CampaignUsers.cid==CID, CampaignUsers.uid==User).first()
        if R == None:
            return False
        elif R.read==0:
            return False
        elif R.read==1:
            return True

'''         


    def User_Login(Username, Password):
        # db.select([census]).where(db.and_(census.columns.state == 'California', census.columns.sex != 'M'))
        query = sqlalchemy.select([Users]).where(sqlalchemy.and_(Users.columns.user_email == Username, Users.columns.password == Password))
        #query = sqlalchemy.select([Users])
        Result = connection.execute(query)
        ResultSet=Result.fetchone()
        #print(len(ResultSet))

        if ResultSet != None:
            return "Sucessful Login: This is an admin account."
        else:
            return "Incorrect Username/Password."



    def Get_Campaign_Info():
        return
    def Add_Campaign_User( campaign, email):
        uid = __get_user_id__(email)
        if not uid:
            print("No UID found.")
            return False
        cid = __get_campaign_id(campaign)
        if not cid:
            print("No CID found.")
            return False
        query = sqlalchemy.insert(CampaignUsers).values(cid=CID, uid=uid, read=1, write=1)
        connection.execute(query)
        return True
    def Update_Campaign_User():
        return
    def Remove_Campaign_User():
        return
    def Create_Implant():
        return
    def Log_Implant():
        return
    def Log_Response():
        return
print(Add_User("admin_3","letmein", True))

User_Login("admin","letmein")

#a= input("Username: ")
#b= input("Password: ")

#print(User_Login(a,b))
#Create_Campaign("Boots Ltd.","admin")
__get_user_id__("admin")
#metadata.drop_all(engine)
'''
#db = Database()
#db.test("admin")