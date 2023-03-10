from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import executor
from aiogram.dispatcher.filters.state import State, StatesGroup

import sqlalchemy as db
import sqlite3
from sqlalchemy.ext.declarative import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import time

bot = Bot(token='_______:_____________')
dp = Dispatcher(bot, storage=MemoryStorage())

engine = db.create_engine('sqlite+pysqlite:///database.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine, future=True, expire_on_commit=False)
session = Session()


class Locations(Base):
    __tablename__ = 'locations'

    LocationID = Column(Integer, name='LocationID', primary_key=True)
    LocationName = Column(Integer, name='LocationName')
    XCoord = Column(Integer)
    YCoord = Column(Integer)

    def __repr__(self):
        return f"Name: {self.LocationName}\n, " \
               f"LocationID: {self.LocationID}\n," \
               f"X:  {self.XCoord}\n," \
               f"Y:  {self.YCoord}\n,"


def put_locations_to_table():
    locations = [{'id': '0', 'name': 'City', 'x': 0, 'y': 0},
                 {'id': '0', 'name': 'Shop', 'x': 0, 'y': 0},
                 {'id': '0', 'name': 'Road', 'x': 0, 'y': 10},
                 {'id': '0', 'name': 'Dungeons', 'x': 0, 'y': 20}]
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    i = 0
    for location in locations:
        sql.execute(f"DELETE FROM locations WHERE LocationID = {i}")
        sql.execute(
            f"INSERT INTO locations (LocationID, LocationName, XCoord, YCoord) VALUES ({i}, '{location['name']}', '{location['x']}', '{location['y']}')")
        i += 1
    db.commit()


class Persons(Base):
    __tablename__ = 'persons'

    UserID = Column(Integer, name='UserId', primary_key=True)
    Nickname = Column(String)
    Level = Column(Integer)
    HP = Column(Integer)
    CurHP = Column(Integer)
    Money = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    XP = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    LocationID = Column(String)
    TgID = Column(String)


class Items(Base):
    __tablename__ = 'items'

    ItemID = Column(Integer, name='ItemID', primary_key=True)
    Name = Column(String)
    Cost = Column(Integer)
    CostToSale = Column(Integer)
    ItemType = Column(String)
    HP = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    ReqLevel = Column(Integer)

    def __repr__(self):
        return f"Name: {self.Name}," \
               f"ItemID: {self.ItemID}," \
               f"Cost: {self.Cost}," \
               f"CostToSale: {self.CostToSale}," \
               f"ItemType: {self.ItemType}," \
               f"HP: {self.HP}," \
               f"Attack: {self.Attack}," \
               f"MagicAttack: {self.MagicAttack}," \
               f"Armour: {self.Armour}," \
               f"MagicArmour: {self.MagicArmour}," \
               f"ReqLevel: {self.ReqLevel}"


def put_items_to_table():
    items_list = [(0, '??????', 100, 80, 'weapon', 10, 10, 10, 0, 0, 1),
                  (0, '??????', 200, 160, 'weapon', 20, 20, 15, 0, 0, 1),
                  (0, '???????????????????? ????????', 100, 80, 'helmet', 15, 0, 0, 15, 15, 1),
                  (0, '?????????????????????????? ????????', 200, 160, 'helmet', 20, 0, 0, 20, 15, 1),
                  (0, '???????????????????? ??????????', 100, 80, 'armor', 15, 0, 0, 15, 15, 1),
                  (0, '?????????????????????????? ??????????', 200, 160, 'armor', 20, 0, 0, 20, 15, 1),
                  (0, '???????????????????? ????????????', 100, 80, 'boots', 15, 0, 0, 15, 15, 1),
                  (0, '?????????????????????????? ????????????', 200, 160, 'boots', 20, 0, 0, 20, 15, 1),
                  (0, '???????????????????? ????????????', 100, 80, 'bracers', 15, 0, 0, 15, 15, 1),
                  (0, '?????????????????????????? ????????????', 200, 160, 'bracers', 20, 0, 0, 20, 15, 1),
                  (0, '?????????? ????????????????', 100, 80, 'potion', 50, 0, 0, 0, 0, 1),
                  (0, '?????????? ??????????????', 110, 90, 'potion', 10, 0, 50, 0, 0, 1)]
    items_dicts = []
    i = 0
    for item in items_list:
        d = {'id': i, 'name': item[1], 'cost': item[2], 'costToSale': item[3], 'itemType': item[4],
             'hp': item[5], 'attack': item[6], 'magicAttack': item[7], 'armour': item[8],
             'magicArmour': item[9], 'reqLevel': item[10]}
        items_dicts.append(d)
        i += 1
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    for item in items_dicts:
        sql.execute(f"DELETE FROM items WHERE ItemId = {item['id']}")
        sql.execute(
            f"INSERT INTO items (ItemID, Name, Cost, CostToSale, ItemType, HP, Attack, MagicAttack, Armour, MagicArmour, ReqLevel) VALUES ({item['id']}, "
            f"'{item['name']}', "
            f"'{item['cost']}', "
            f"'{item['costToSale']}', "
            f"'{item['itemType']}', "
            f"'{item['hp']}', "
            f"'{item['attack']}', "
            f"'{item['magicAttack']}', "
            f"'{item['armour']}', "
            f"'{item['magicArmour']}', "
            f"'{item['reqLevel']}')")
    db.commit()


class ItemsByPerson(Base):
    __tablename__ = 'items_by_person'

    UserID = Column(Integer, name='UserId')
    ItemID = Column(Integer, name='ItemID', primary_key=True)
    Quantity = Column(Integer)
    NowWearing = Column(Integer)

    def __repr__(self):
        text_about_wearing = ""
        if self.NowWearing == 1:
            text_about_wearing = " [????????????]"

        return f'ItemID: {self.ItemID}, {self.Quantity} ????????' + text_about_wearing


Base.metadata.create_all(engine)

put_items_to_table()
put_locations_to_table()


class Person(StatesGroup):
    UserId = State()
    Nickname = State()
    HP = State()
    Attack = State()
    MagicAttack = State()
    Armour = State()
    MagicArmour = State()
    TgID = State()


@dp.message_handler(commands=['start'], state="*")
async def start(message):
    await Person.UserId.set()
    create = KeyboardButton("?????????????? ??????????????????")
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(create)
    await message.answer("?????????? ???????????????????? ?? ????????! ???????????????? ??????????????????",
                         reply_markup=buttons)


@dp.message_handler(state=Person.UserId)
async def create(message, state):
    results = session.query(Persons).all()
    if len(results) > 0:
        await message.answer("?? ?????? ?????? ???????? ????????????????")
        await state.finish()
        return
    await message.answer("?????????????? ??????")
    await Person.next()


@dp.message_handler(state=Person.Nickname)
async def name(message, state):
    async with state.proxy() as data:
        data['Nickname'] = message.text
    await message.answer('?????????????? ???????????????????? ?????????? ???????????????? ??????????????????. (???? 10 ???? 100)')
    await Person.next()


@dp.message_handler(state=Person.HP)
async def health(message, state):
    async with state.proxy() as data:
        data['HP'] = message.text
    await message.answer('?????????????? ?????????????? ?????????? ??????????????????. (???? 10 ???? 100)')
    await Person.next()


@dp.message_handler(state=Person.Attack)
async def attack(message, state):
    async with state.proxy() as data:
        data['Attack'] = message.text
    await message.answer('?????????????? ?????????????? ???????????????????? ?????????? ??????????????????. (???? 10 ???? 100)')
    await Person.next()


@dp.message_handler(state=Person.MagicAttack)
async def magic_attack(message, state):
    async with state.proxy() as data:
        data['MagicAttack'] = message.text
    await message.answer('?????????????? ?????????????? ?????????????? ?????????? ??????????????????. (???? 10 ???? 100)')
    await Person.next()


@dp.message_handler(state=Person.Armour)
async def armour(message, state):
    async with state.proxy() as data:
        data['Armour'] = message.text
    await message.answer('?????????????? ?????????????? ???????????????????? ?????????? ??????????????????. (???? 10 ???? 100)')
    await Person.next()


@dp.message_handler(state=Person.MagicArmour)
async def magic_armour(message, state):
    async with state.proxy() as data:
        data['MagicArmour'] = message.text
        data['TgID'] = message.from_user.id

        new_track = Persons(UserID=message.from_user.id,
                            Nickname=data['Nickname'],
                            Level=1,
                            HP=data['HP'],
                            CurHP=data['HP'],
                            Money=1000,
                            Attack=data['Attack'],
                            MagicAttack=data['MagicAttack'],
                            XP=0,
                            Armour=data['Armour'],
                            MagicArmour=data['MagicArmour'],
                            LocationID=0,
                            TgID=data['TgID'])
        session.add(new_track)
        session.commit()
    await message.answer('???????????????? ????????????. ?????????????????? ?????????????? ?????????? ???????????????????? ?? /help')
    await state.finish()


@dp.message_handler(commands=['statistics'], state='*')
async def statistics(message):
    results = session.query(Persons).all()
    await message.answer(
        f'?????? ????????????????:\n'
        f'??????: {results[0].Nickname}\n'
        f'??????????????: {results[0].Level}\n'
        f'????????????????: {results[0].HP}\n'
        f'?????????????? ????????????????:{results[0].CurHP}\n'
        f'????????????: {results[0].Money}\n'
        f'??????????: {results[0].Attack}\n'
        f'???????????????????? ??????????: {results[0].MagicAttack}\n'
        f'????????: {results[0].XP}\n'
        f'??????????: {results[0].Armour}\n'
        f'???????????????????? ??????????: {results[0].MagicArmour}\n'
        f'??????????????: {results[0].LocationID}')


@dp.message_handler(commands=['help'], state='*')
async def help(message):
    await message.answer("?????????????????? ??????????????:\n"
                         "/start - ?????????????? ?????????????????? (???????????????? ???????????? ???????? ??????)\n"
                         "/statistics- ???????????????????? ????????????????????\n"
                         "/inventory - ???????????????????? ??????????????????\n"
                         "/locations - ?????????????????????????? ?? ???????????? ??????????????\n"
                         "/help - ???????????????????? ??????????????")


@dp.message_handler(commands=['locations'], state='*')
async def locations(message):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    loc = session.query(Locations)
    person = session.query(Persons).where(Persons.UserID == str(message.from_user.id)).first()
    await message.answer(f'???????? LocationID: {person.LocationID}')
    loc_now = loc.filter_by(LocationID=person.LocationID).first()
    await message.answer(f'???????? ????????????????????: {loc_now.XCoord}, {loc_now.YCoord}')
    where_can_go = []
    where_can_go_names = []
    for elem in loc:
        if (elem.XCoord - loc_now.XCoord) ** 2 + (elem.YCoord - loc_now.YCoord) ** 2 <= 100:
            where_can_go.append(elem)
            where_can_go_names.append(elem.LocationName)
    await message.answer("???? ???????????? ?????????? ?? ???????? ???? ???????? ??????????????: " + ', '.join(where_can_go_names))
    for elem in where_can_go:
        b = KeyboardButton(elem.LocationName)
        buttons.add(b)
    exit = KeyboardButton("??????????")
    buttons.add(exit)
    session.commit()

    await message.answer("???????? ???? ???????????? ???????????", reply_markup=buttons)


@dp.message_handler(lambda message: message.text == "Dungeons", state="*")
async def dungeons(message, state):
    user_id = message.from_user.id
    loc = session.query(Locations)
    person = session.query(Persons).where(Persons.UserID == user_id).first()
    loc_now = loc.filter_by(LocationID=person.LocationID).first()
    elem = loc.filter_by(LocationID=3).first()
    dist = (elem.XCoord - loc_now.XCoord) ** 2 + (elem.YCoord - loc_now.YCoord) ** 2
    if dist > 100:
        await message.answer("???? ???? ???????????? ?????????????????????????? ?? ????????????????????")
        state.finish()
        return

    t = int(dist ** 0.5)
    for i in range(t):
        await message.answer(f'???????? ??????????????????????. ???????????? {i} ????????????, ???????????????? ?????? {t - i} ????????????.')
        time.sleep(1)

    await message.answer('???? ?????????????????????????? ?? ????????????????????')

    user = session.execute(select(Persons).where(Persons.UserID == user_id)).first()
    user[0].LocationID = elem.LocationID
    session.commit()


@dp.message_handler(lambda message: message.text == "Road", state="*")
async def road(message, state):
    user_id = message.from_user.id
    loc = session.query(Locations)
    person = session.query(Persons).where(Persons.UserID == user_id).first()
    loc_now = loc.filter_by(LocationID=person.LocationID).first()
    elem = loc.filter_by(LocationID=2).first()
    dist = (elem.XCoord - loc_now.XCoord) ** 2 + (elem.YCoord - loc_now.YCoord) ** 2
    if dist > 100:
        await message.answer("???? ???? ???????????? ?????????????????????????? ???? ????????????")
        state.finish()
        return

    t = int(dist ** 0.5)
    for i in range(t):
        await message.answer(f'???????? ??????????????????????. ???????????? {i} ????????????, ???????????????? ?????? {t - i} ????????????.')
        time.sleep(1)

    await message.answer('???? ?????????????????????????? ???? ????????????')

    user = session.execute(select(Persons).where(Persons.UserID == user_id)).first()
    user[0].LocationID = elem.LocationID
    session.commit()


@dp.message_handler(lambda message: message.text == "City", state="*")
async def city(message, state):
    user_id = message.from_user.id
    loc = session.query(Locations)
    person = session.query(Persons).where(Persons.UserID == user_id).first()
    loc_now = loc.filter_by(LocationID=person.LocationID).first()
    elem = loc.filter_by(LocationID=0).first()
    dist = (elem.XCoord - loc_now.XCoord) ** 2 + (elem.YCoord - loc_now.YCoord) ** 2
    if dist > 100:
        await message.answer("???? ???? ???????????? ?????????????????????????? ?? ??????????")
        state.finish()
        return

    t = int(dist ** 0.5)
    for i in range(t):
        await message.answer(f'???????? ??????????????????????. ???????????? {i} ????????????, ???????????????? ?????? {t - i} ????????????.')
        time.sleep(1)

    await message.answer('???? ?????????????????????????? ?? ??????????')

    user = session.execute(select(Persons).where(Persons.UserID == user_id)).first()
    user[0].CurHP = user[0].HP
    user[0].LocationID = elem.LocationID
    session.commit()
    await message.answer('???????? ???????????????? ??????????????????????????')


@dp.message_handler(lambda message: message.text == "Shop", state="*")
async def shop(message, state):
    user_id = message.from_user.id
    loc = session.query(Locations)
    person = session.query(Persons).where(Persons.UserID == user_id).first()
    loc_now = loc.filter_by(LocationID=person.LocationID).first()
    elem = loc.filter_by(LocationID=1).first()
    dist = (elem.XCoord - loc_now.XCoord) ** 2 + (elem.YCoord - loc_now.YCoord) ** 2
    if dist > 100:
        await message.answer("???? ???? ???????????? ?????????????????????????? ?? ??????????????")
        state.finish()
        return
    user = session.execute(select(Persons).where(Persons.UserID == user_id)).first()
    user[0].LocationID = elem.LocationID
    session.commit()

    get = KeyboardButton("???????????????????? ????????????")
    sell = KeyboardButton("?????????????? ????????????")
    buy = KeyboardButton("???????????? ????????????")
    exit = KeyboardButton("??????????")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(get, buy, sell, exit)

    t = int(dist ** 0.5)
    for i in range(t):
        await message.answer(f'???????? ??????????????????????. ???????????? {i} ????????????, ???????????????? ?????? {t - i} ????????????.')
        time.sleep(1)

    await message.answer('???? ?????????????????????????? ?? ??????????????.', reply_markup=buttons)


@dp.message_handler(commands=['inventory'], state='*')
async def inventory(message):
    take_on_or_off = KeyboardButton("????????????/?????????? ????????????????????")
    exit = KeyboardButton("??????????")
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(take_on_or_off, exit)
    results = session.query(ItemsByPerson).where(ItemsByPerson.UserID == str(message.from_user.id))
    inv = ''
    for elem in results:
        inv += (str(elem) + '\n')
    await message.answer('??????????????????:\n' + inv, reply_markup=buttons)


class Actions(StatesGroup):
    Sell = State()
    Buy = State()
    TakeOnOrOff = State()


@dp.message_handler(lambda message: message.text == "????????????/?????????? ????????????????????", state="*")
async def take_on_or_off(message):
    await Actions.TakeOnOrOff.set()
    await message.answer("?????????????? ItemId ????????????, ?????????????? ???? ???????????? ??????????/????????????")


@dp.message_handler(lambda message: message.text == "??????????", state="*")
async def exit(message, state):
    await state.finish()
    await message.answer("?????????????????? ??????????????:\n"
                         "/start - ?????????????? ?????????????????? (???????????????? ???????????? ???????? ??????)\n"
                         "/statistics - ???????????????????? ????????????????????\n"
                         "/inventory - ???????????????????? ??????????????????\n"
                         "/locations - ?????????????????????????? ?? ???????????? ??????????????\n"
                         "/help - ???????????????????? ??????????????")


@dp.message_handler(state=Actions.TakeOnOrOff)
async def take_on_or_off(message, state):
    results = session.query(ItemsByPerson).filter_by(UserID=str(message.from_user.id)).filter_by(NowWearing=1)
    existing_types = set()

    for item in results:
        r = session.query(Items).filter_by(ItemID=item.ItemID).first().ItemType
        if r != 'potion':
            existing_types.add(r)

    text = '?? ?????? ????????????: ' + ', '.join(list(existing_types))

    await message.answer(text)

    take_on_or_off_item_id = str(message.text)
    user_id = message.from_user.id
    items = session.query(ItemsByPerson).filter_by(ItemID=take_on_or_off_item_id).filter_by(UserID=user_id)

    if items.count() < 1:
        await message.answer("???????????? ???????????????? ???????????????????? ?? ?????? ??????")
        await state.finish()
        return
    quantity = items.first().Quantity
    if quantity <= 0:
        await message.answer("???????????? ???????????????? ???????????????????? ?? ?????? ??????")
        await state.finish()
        return
    item_type = session.query(Items).filter_by(ItemID=take_on_or_off_item_id).first().ItemType

    now_wearing = items.first().NowWearing
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    if now_wearing == 0:
        if item_type in existing_types:
            await message.answer(f"???? ?????? ?????? ?????????? ?????????????? ???????????????????? ???????? {item_type}. ?????????????? ??????, ?????????? ???????????? ????????????.")
            await state.finish()
            return
        now_wearing = 1
        await message.answer(f"???????????? ?????????????? ???????????????????? {take_on_or_off_item_id} ???? ??????")
    else:
        now_wearing = 0
        await message.answer(f"???????????? ?????????????? ???????????????????? {take_on_or_off_item_id} ???? ???? ??????")
    sql.execute(f"INSERT OR REPLACE INTO items_by_person (UserID, ItemID, Quantity, NowWearing) VALUES ({user_id},"
                f" '{take_on_or_off_item_id}', '{quantity}', '{now_wearing}')")
    db.commit()
    session.commit()
    await state.finish()


@dp.message_handler(lambda message: message.text == "???????????????????? ????????????", state="*")
async def look_at(message):
    results = session.query(Items).all()
    text = '????????????:\n'
    for r in results:
        text += str(r)
        text += '\n\n'
    await message.answer(text)


@dp.message_handler(lambda message: message.text == "?????????????? ????????????", state="*")
async def get(message):
    await Actions.Sell.set()
    await message.answer("?????????????? ItemID ????????????, ?????????? ?????????????? ??????.")


UserID = Column(Integer, name='UserId', primary_key=True)
ItemID = Column(Integer, name='ItemID')
Quantity = Column(Integer)
NowWearing = Column(Integer)


@dp.message_handler(state=Actions.Sell)
async def sell(message, state):
    sell_item_id = str(message.text)
    user_id = message.from_user.id
    items = session.query(ItemsByPerson).filter_by(ItemID=sell_item_id).filter_by(UserID=user_id)

    if items.count() < 1:
        await message.answer("???????????? ???????????? ?? ?????? ??????")
        await state.finish()
        return
    quantity = items.first().Quantity - 1
    if quantity < 0:
        await message.answer("???????????? ???????????? ?? ?????? ??????")
        await state.finish()
        return
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    now_wearing = 0
    sql.execute(f"INSERT OR REPLACE INTO items_by_person (UserID, ItemID, Quantity, NowWearing) VALUES ({user_id},"
                f" '{sell_item_id}', '{quantity}', '{now_wearing}')")
    db.commit()

    items = session.query(Items).filter_by(ItemID=sell_item_id).first()
    money = items.CostToSale

    user = session.execute(
        select(Persons).where(Persons.UserID == user_id)
    ).first()
    user[0].Money += money
    session.commit()
    await message.answer("?????????? ????????????")
    await state.finish()


@dp.message_handler(lambda message: message.text == "???????????? ????????????", state="*")
async def get(message):
    await Actions.Buy.set()
    await message.answer("?????????????? ItemId ????????????, ?????????? ???????????? ??????. ItemID ???????? ?????????????? ?????????? ???????????????????? ?? ????????????????.")


@dp.message_handler(state=Actions.Buy)
async def buy(message, state):
    buy_item_id = int(message.text)
    user_id = message.from_user.id

    items = session.query(ItemsByPerson).filter_by(ItemID=buy_item_id).filter_by(UserID=user_id)
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    if items.count() < 1:
        quantity = 1
    else:
        quantity = items.first().Quantity + 1
    now_wearing = 0

    user = session.execute(
        select(Persons).where(Persons.UserID == user_id)
    ).first()
    items = session.query(Items).filter_by(ItemID=buy_item_id).first()
    money = items.Cost
    if user[0].Money - money < 0:
        await message.answer("?? ?????? ???????????????????????? ??????????")
        await state.finish()
        return
    user[0].Money -= money
    sql.execute(f"INSERT OR REPLACE INTO items_by_person (UserID, ItemID, Quantity, NowWearing) VALUES ({user_id},"
                f" '{buy_item_id}', '{quantity}', '{now_wearing}')")
    db.commit()
    session.commit()
    await message.answer("?????????? ????????????")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp)
