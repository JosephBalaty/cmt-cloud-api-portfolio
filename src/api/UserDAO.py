
class UserDAO:

    @staticmethod
    def login(login_info):
        username = content["username"]
        password = content["password"]
        body = {
                'grant_type':'password',
                'username':username,
                'password':password,
                'client_id':p.CLIENT_ID,
                'client_secret':p.CLIENT_SECRET
            }
        headers = { 'content-type': 'application/json' }
        url = 'https://' + p.DOMAIN + '/oauth/token'
        r = requests.post(url, json=body, headers=headers)

        return r.json()

        @staticmethod
        # what is sub?
        def authenticate_user(payload):
            query = client.query(kind=USERS)
            query.add_filter('sub', '=', payload['sub'])
            user = list(query.fetch())[0]
            return user
        
        @staticmethod
        def get_users(user_id):
            query = client.query(kind=USERS)
            users = list(query.fetch())
            for u in users:
                u['id'] = u.key.id
            return users