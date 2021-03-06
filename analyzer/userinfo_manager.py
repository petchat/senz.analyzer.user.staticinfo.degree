import leancloud
from analyzer import staticinfo_exceptions
from config import token_config
import re

__author__ = 'Jayvee'
USER_INFO_DATABASE_APP_ID = "pin72fr1iaxb7sus6newp250a4pl2n5i36032ubrck4bej81"
USER_INFO_DATABASE_APP_KEY = "qs4o5iiywp86eznvok4tmhul360jczk7y67qj0ywbcq35iia"


def push_userinfo(userId, applist, staticInfo, timestamp, userRawdataId):
    leancloud.init(USER_INFO_DATABASE_APP_ID, USER_INFO_DATABASE_APP_KEY)
    try:
        if not isinstance(staticInfo, dict):
            raise staticinfo_exceptions.MsgException('staticInfo should be a dict')
        if not re.compile('1\d{12}').match(str(timestamp)):
            raise staticinfo_exceptions.MsgException('timestamp is not formatted')
        UserInfoLog = leancloud.Object.extend('UserInfoLog')
        uil = UserInfoLog()
        user_query = leancloud.Query(leancloud.User)
        # userquery.equal_to('id', userId)
        user_obj = user_query.get(userId)

        uil.set('user', user_obj)
        uil.set('applist', applist)
        uil.set('staticInfo', staticInfo)
        uil.set('timestamp', timestamp)
        uil.set('userRawdataId', userRawdataId)
        uil.save()
    except Exception, e:
        raise staticinfo_exceptions.MsgException('[%s]fail to push userId=%s, staticinfo=%s, timestamp=%s, detail=%s'
                                        % ('push_userinfo', userId, staticInfo, timestamp, str(e)))


def query_latest_userinfo(userId):
    leancloud.init(USER_INFO_DATABASE_APP_ID, USER_INFO_DATABASE_APP_KEY)
    try:
        UserInfoLog = leancloud.Object.extend('UserInfoLog')
        info_query = leancloud.Query(UserInfoLog)
        user_query = leancloud.Query(leancloud.User)
        user_obj = user_query.get(userId)
        info_query.equal_to('user', user_obj)
        info_query.descending('timestamp')
        latest_userinfo = info_query.first()
        return latest_userinfo
    except leancloud.LeanCloudError, lce:
        if lce.code == 101:
            return None
        else:
            raise staticinfo_exceptions.MsgException('[%s]fail to query latest info. userId=%s, detail=%s'
                                            % ('query_latest_userinfo', userId, lce))


def query_userinfo_list(userId):
    leancloud.init(USER_INFO_DATABASE_APP_ID, USER_INFO_DATABASE_APP_KEY)
    try:
        UserInfoLog = leancloud.Object.extend('UserInfoLog')
        info_query = leancloud.Query(UserInfoLog)
        user_query = leancloud.Query(leancloud.User)
        user_obj = user_query.get(userId)
        info_query.equal_to('user', user_obj)
        info_query.descending('timestamp')
        query_result = info_query.find()
        userinfo_list = []
        for userinfo in query_result:
            userinfo_list.append(
                {'timestamp': userinfo.attributes['timestamp'],
                 'staticInfo': userinfo.attributes['staticInfo'],
                 'userRawdataId': userinfo.attributes['userRawdataId'],
                 'applist': userinfo.attributes['applist']})
        return userinfo_list
    except leancloud.LeanCloudError, lce:
        raise staticinfo_exceptions.MsgException('[%s]fail to query userinfo. userId=%s, LeanCloudError detail=%s'
                                        % ('query_userinfo_list', userId, lce))


if __name__ == '__main__':
    push_userinfo('55a0c4d3e4b06d11d320a160',
                  {"sport-fitness": 0.14017973131826397, "consumption-5000to10000": 0.12907750356282785,
                   "business_news": 0.06019292654288461, "consumption-5000down": 0.10113896734527256,
                   "current_news": 0.19523741203679054, "consumption-20000up": 0.15569978883230456,
                   "indoorsman": 0.17960441041762185, "health": 0.12191351265656468,
                   "consumption-10000to20000": 0.2356820553240806, "social": 0.20201845583545766,
                   "online_shopping": 0.17904598788548037}, 1427642632501)
    print query_latest_userinfo('55a0c4d3e4b06d11d320a160')
    print query_userinfo_list('55a0c4d3e4b06d11d320a160')
