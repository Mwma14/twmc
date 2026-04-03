from MyanmarMusic.core.bot import Hotty
from MyanmarMusic.core.dir import dirr
from MyanmarMusic.core.git import git
from MyanmarMusic.core.userbot import Userbot
from MyanmarMusic.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Hotty()
userbot = Userbot()
api = SafoneAPI()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
#Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

APP = "sasukevipmusicbot"  # connect music api key "Dont change it"
