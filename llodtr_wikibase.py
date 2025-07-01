from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes.string import String
from wikibaseintegrator.datatypes.externalid import ExternalID
from wikibaseintegrator.datatypes.item import Item
from wikibaseintegrator.datatypes.property import Property
from wikibaseintegrator.datatypes.lexeme import Lexeme
from wikibaseintegrator.datatypes.sense import Sense as SenseClaim
from wikibaseintegrator.datatypes.monolingualtext import MonolingualText
from wikibaseintegrator.datatypes.time import Time
from wikibaseintegrator.datatypes.globecoordinate import GlobeCoordinate
from wikibaseintegrator.datatypes.url import URL
from wikibaseintegrator.models import Reference, References, Form, Sense
from wikibaseintegrator.models.qualifiers import Qualifiers
from wikibaseintegrator.models.claims import Claims
from wikibaseintegrator import wbi_helpers
from wikibaseintegrator.wbi_enums import ActionIfExists, WikibaseSnakType

from wikibaseintegrator.wbi_config import config as wbi_config

import llodtr_config_private

wbi_config['BACKOFF_MAX_TRIES'] = 5
wbi_config['BACKOFF_MAX_VALUE'] = 3600
wbi_config['USER_AGENT'] = "bot based on wikibaseintegrator"
wbi_config['PROPERTY_CONSTRAINT_PID'] = None # 'P2302'
wbi_config['DISTINCT_VALUES_CONSTRAINT_QID'] = None # 'Q21502410'
wbi_config['COORDINATE_GLOBE_QID'] = 'http://www.wikidata.org/entity/Q2'
wbi_config['CALENDAR_MODEL_QID'] = 'http://www.wikidata.org/entity/Q1985727'

wbi_config['MEDIAWIKI_API_URL'] = 'https://llod-training.wikibase.cloud/w/api.php'
wbi_config['MEDIAWIKI_INDEX_URL'] = "https://llod-training.wikibase.cloud/w/index.php"
wbi_config['MEDIAWIKI_REST_URL'] = "https://llod-training.wikibase.cloud/w/rest.php"
wbi_config['SPARQL_ENDPOINT_URL'] = "https://llod-training.wikibase.cloud/query/sparql"
wbi_config['WIKIBASE_URL'] = "https://llod-training.wikibase.cloud"
wbi_config['DEFAULT_LANGUAGE'] = 'en'
wbi_config['DEFAULT_LEXEME_LANGUAGE'] = "Q207" # This is for Lexemes. Value None raises error.

login = wbi_login.Login(user=llodtr_config_private.wb_bot_user, password=llodtr_config_private.wb_bot_pwd)
bot = WikibaseIntegrator(login=login)
print('**** Wikibase bot username and password accepted, bot is being loaded. ****')
