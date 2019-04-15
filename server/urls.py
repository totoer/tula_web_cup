
from handlers.client.login import Login
from handlers.client.logout import Logout
from handlers.client.oauth import OAuth
from handlers.client.image import Image
from handlers.client.image_like import ImageLike


urls = [
    (r'/api/login/?', Login,),
    (r'/api/logout/?', Logout,),
    (r'/api/oauth/?', OAuth,),
    (r'/api/?', Image,),
    (r'/api/image_like/?', ImageLike,),
]