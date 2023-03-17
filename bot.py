#from instapy import InstaPy
#from instapy import smart_run


#path ="C:\Program Files (x86)\geckodriver.exe"
#session = InstaPy(username='bodrov_magazine', password='bodrovAdmin1997A+', geckodriver_path= path, want_check_browser=False, headless_browser=False)
#session.login()
#session.like_by_tags(["НИЖНИЙНОВГОРОД","ФОТОГРАФНИЖНИЙНОВГОРОД"], amount=5)
#session.set_do_follow()

#with smart_run(session):


from instagrapi import Client
import time
import random
import data


cl = Client()
cl.login(data.username, data.password)

class LikePost:
    def __init__(self,client):
        self.cl = client
        self.tags = ['фотографнижнийновгород','нижнийновгород']
        self.liked_medias = []
        self.elapsed_time = 0

    def wait_time(self,delay):
        time.sleep(delay)

    def get_post_id(self):
        medias = cl.hashtag_medias_recent(random.choice(self.tags), amount =1)
        media_dict = medias[0].dict()
        return str(media_dict["id"])

    def like_post(self, amount):
        for i in range(amount):
            random_post = self.get_post_id()
            if random_post in self.liked_medias:
                pass
            else:
                self.cl.media_like(media_id = random_post)
                self.liked_medias.append(random_post)
                random_delay = random.randint(20,60)
                print(f"Liked {len(self.liked_medias)} posts, time elapsed {self.elapsed_time / 60 }, now waiting for {random_delay} seconds ")
                self.wait_time(random_delay)

followers = cl.user_followers(cl.user_id)
for user_id in followers.keys():
    cl.user_follow(user_id)
    time.sleep(random.randint(20,60))
    print(f"Follow {cl.user_info(user_id)}")



start = LikePost(cl)
start.like_post(600)