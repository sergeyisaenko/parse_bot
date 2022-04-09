from peewee import *
from playhouse.migrate import SqliteMigrator, migrate

db = SqliteDatabase('video.db')


class BaseModel(Model):
    class Meta:
        database = db


class Sneakers(BaseModel):
    title = CharField()
    url = TextField()
    price = DecimalField()


class SearchModel(BaseModel):
    title = CharField()
    chatid = CharField()


def find_all_cards():
    return Sneakers.select()


def find_id_search(chat_id):
    return SearchModel.select().where(SearchModel.chatid == chat_id)


def find_all_search():
    return SearchModel.select()


async def process_search_model(message):
    search_exist = True
    try:
        search = SearchModel.select().where(SearchModel.title == message.text).get()
        search.delete_instance()
        await message.answer('String search {} deleted'.format(message.text))
        return search_exist
    except DoesNotExist as de:
        search_exist = False

    if not search_exist:
        rec = SearchModel(title=message.text, chatid=message.chat.id)
        rec.save()
        await message.answer('String search {} added'.format(message.text))
    else:
        await message.answer('String search {} already exist'.format(message.text))
        return search_exist


def init_db():
    db.create_tables([Sneakers, SearchModel])
    # migrator = SqliteMigrator(db)
    # migrate(
    #      migrator.rename_table('VideoCard', 'Sneakers')
    # )