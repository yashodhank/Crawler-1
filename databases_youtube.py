import datetime, MySQLdb, emoji

class data:
    def __init__(self, configuration):
        self.connection = MySQLdb.connect(host=str(configuration['database']['host']),
                                          user=str(configuration['database']['user']),
                                          passwd=str(configuration['database']['password']),
                                          db=str(configuration['database']['db']),
                                          use_unicode=True,
                                          charset="utf8"
                                          )

        self.cursor = self.connection.cursor()
        # self.cursor.execute("drop table if exists facebook_pages")
        self.create_pages()
    pass

    def check_queue(self):
        self.cursor.execute("Select * FROM queue LIMIT 1")
        self.is_queue_empty = self.cursor.fetchone()

        return self.is_queue_empty


    def create_pages(self):
        self.cursor.execute('''create table if not exists youtube_pages(title text, id text, etag text, description text, customUrl text,
                publishedAt text, defaultLanguage text, country text, contentDetails text, viewCount text,
                commentCount text, subscriberCount text, videoCount text, keywords text, defaultTab text, analyticsAccountId text,
                featuredChannelsTitle text, time_ text)''')

        self.connection.commit()
    pass

    def check_item(self, id):
        self.cursor.execute("Select * from youtube_pages where id = %s", (id, ))
        check = self.cursor.fetchone()
        return check
    pass


    def insert_into(self, params):
        import json

        list_to_insert =[]

        if params['snippet']['title'].find("'") == -1:
            list_to_insert.append(params['snippet']['title'])
        else:
            name = params['snippet']['title'].replace("'", "''")
            list_to_insert.append(name)

        list_to_insert.append(params['id'])
        list_to_insert.append(params['etag'])

        if 'description' in params['snippet'].keys():
            list_to_insert.append(params['snippet']['description'])
        else:
            list_to_insert.append(None)

        if 'customUrl' in params['snippet'].keys():
            list_to_insert.append(params['snippet']['customUrl'])
        else:
            list_to_insert.append(None)

        if 'publishedAt' in params['snippet'].keys():
            list_to_insert.append(params['snippet']['publishedAt'])
        else:
            list_to_insert.append(None)

        if 'defaultLanguage' in params['snippet'].keys():
            list_to_insert.append(params['snippet']['defaultLanguage'])
        else:
            list_to_insert.append(None)

        if 'country' in params['snippet'].keys():
            list_to_insert.append(params['snippet']['country'])
        else:
            list_to_insert.append(None)

        if 'contentDetails' in params.keys():
            contentDetails=json.dumps(params['contentDetails'])
            list_to_insert.append(contentDetails)
        else:
            list_to_insert.append(None)

        if 'viewCount' in params['statistics'].keys():
            list_to_insert.append(params['statistics']['viewCount'])
        else:
            list_to_insert.append(None)

        if 'commentCount' in params['statistics'].keys():
            list_to_insert.append(params['statistics']['commentCount'])
        else:
            list_to_insert.append(None)

        if 'subscriberCount' in params['statistics'].keys():
            list_to_insert.append(params['statistics']['subscriberCount'])
        else:
            list_to_insert.append(None)

        if 'videoCount' in params['statistics'].keys():
            list_to_insert.append(params['statistics']['videoCount'])
        else:
            list_to_insert.append(None)

        if 'keywords' in params['brandingSettings']['channel'].keys():
            list_to_insert.append(params['brandingSettings']['channel']['keywords'])
        else:
            list_to_insert.append(None)

        if 'defaultTab' in params['brandingSettings']['channel'].keys():
            list_to_insert.append(params['brandingSettings']['channel']['defaultTab'])
        else:
            list_to_insert.append(None)

        if 'trackingAnalyticsAccountId' in params['brandingSettings']['channel'].keys():
            list_to_insert.append(params['brandingSettings']['channel']['trackingAnalyticsAccountId'])
        else:
            list_to_insert.append(None)

        if 'featuredChannelsTitle' in params['brandingSettings']['channel'].keys():
            list_to_insert.append(params['brandingSettings']['channel']['featuredChannelsTitle'])
        else:
            list_to_insert.append(None)


        time = str(datetime.datetime.now())
        list_to_insert.append(time)

        for i in range(0,len(list_to_insert)):
            if list_to_insert[i] is not None:
                emotic = emoji.demojize(list_to_insert[i])
                list_to_insert[i] = list_to_insert[i].replace(list_to_insert[i],emotic)
                list_to_insert[i] = self.encode_to_string(list_to_insert[i])
                pass
            else:
                pass

        self.cursor.execute(self.make_query(list_to_insert,'youtube_pages'))
        self.connection.commit()
    pass

    def encode_to_string(self, element):
        '''encoding unicode variable and replacing encounter special sign'''

        element = element.replace("\"", " ")
        element = element.replace("\\", " ")
        return element.encode("utf-8", "ignore")

    pass

    def make_query(self, list, db_name):
        '''creating a query to mysql db using list object'''

        que = "INSERT INTO %s VALUES" % db_name
        query = que + "(%s)" % ','.join(['\"{}\"'] * len(list))
        query = query.format(*list)
        # print query
        return query

    pass