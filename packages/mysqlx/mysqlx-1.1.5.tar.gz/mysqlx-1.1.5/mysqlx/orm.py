from . import db
from typing import Iterable
from datetime import datetime

PK, TABLE, UPDATE_TIME = '__pk__', '__table__', 'update_time'


class Model:

    def __init__(self, id: int = None, create_by: int = None, create_time: datetime = None, update_time: datetime = None, update_by: int = None,
                 del_flag: int = None):
        self.id = id
        self.create_by = create_by
        self.create_time = create_time
        self.update_by = update_by
        self.update_by = update_time
        self.del_flag = del_flag

    def __str__(self):
        kv = {k: v for k, v in self.__dict__.items() if k not in (PK, TABLE)}
        return str(kv)

    def __getattr__(self, name):
        if PK == name:
            return 'id'
        elif TABLE == name:
            return self.__class__.__name__.lower()
        else:
            return None

    def persist(self):
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        self.id = db.save(self.__table__, **kv)
        return self.id

    def update(self):
        pk = self.__pk__
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        if pk in kv:
            update_kv = {k: v for k, v in kv.items() if k != pk}
            cols, args = zip(*update_kv.items())
            args = [*args, kv[pk]]
            if UPDATE_TIME in update_kv:
                sql = 'UPDATE `%s` SET %s WHERE `%s`=? limit 1' % (self.__table__, ','.join(['`%s`=?' % col for col in cols]), pk)
            else:
                sql = 'UPDATE `%s` SET %s, %s=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (self.__table__, ','.join(['`%s`=?' % col for col in cols]), UPDATE_TIME, pk)
            db.do_execute(sql, *args)
        else:
            raise KeyError("Not primary key.")

    def load(self):
        pk = self.__pk__
        kv = self.__dict__
        _id = kv.get(pk)
        if _id is not None:
            cols, _ = zip(*kv.items())
            sql = 'SELECT %s FROM `%s` WHERE `%s`=? limit 1' % (','.join(['`%s`' % col for col in cols]), self.__table__, pk)
            self.__dict__.update(db.do_select_one(sql, _id))
            return self
        else:
            raise KeyError("Not primary key.")

    def delete(self):
        pk = self.__pk__
        _id = self.__dict__.get(pk)
        if _id is not None:
            sql = 'DELETE FROM `%s` WHERE `%s`=? limit 1' % (self.__table__, pk)
            return db.do_execute(sql, _id)
        else:
            raise KeyError("Not primary key.")

    def logic_delete(self, update_by: int = None):
        pk = self.__pk__
        _id = self.__dict__.get(pk)
        if _id is not None:
            if update_by is None:
                sql = 'UPDATE `%s` SET `del_flag`=1, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (self.__table__, UPDATE_TIME, pk)
                return db.do_execute(sql, _id)
            else:
                sql = 'UPDATE `%s` SET `del_flag`=1, `update_by`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (self.__table__, UPDATE_TIME, pk)
                return db.do_execute(sql, update_by, _id)
        else:
            raise KeyError("Not primary key.")

    @classmethod
    def insert(cls, **kwargs):
        table = Model._get_table(cls)
        return db.insert(table, **kwargs)

    @classmethod
    def save(cls, **kwargs):
        table = Model._get_table(cls)
        return db.save(table, **kwargs)

    @classmethod
    def find_by_id(cls, id: int, *selection):
        pk, table = Model._get_pk_and_table(cls)
        if len(selection) == 0:
            sql = 'SELECT * FROM `%s` WHERE `%s`=? limit 1' % (table, pk)
        else:
            sql = 'SELECT %s FROM `%s` WHERE `%s`=? limit 1' % (','.join(['`%s`' % col for col in selection]), table, pk)
        result = db.do_select_one(sql, id)
        return Model.dict2obj(result, cls, pk, table) if result else None

    @classmethod
    def find_by_ids(cls, ids: Iterable[int], *selection):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'
        pk, table = Model._get_pk_and_table(cls)
        ids_str = ','.join(list(map(str, ids)))
        if len(selection) == 0:
            sql = 'SELECT * FROM `%s` WHERE `%s` in (%s) limit %d' % (table, pk, ids_str, ids_size)
        else:
            sql = 'SELECT %s FROM `%s` WHERE `%s` in (%s) limit %d' % (','.join(['`%s`' % col for col in selection]), table, pk, ids_str, ids_size)
        return [Model.dict2obj(d, cls, pk, table) for d in db.do_select(sql)]

    @classmethod
    def update_by_id(cls, id: int, **kwargs):
        pk, table = Model._get_pk_and_table(cls)
        cols, args = zip(*kwargs.items())
        args = [*args, id]
        if UPDATE_TIME in kwargs:
            sql = 'UPDATE `%s` SET %s WHERE `%s`=? limit 1' % (table, ','.join(['`%s`=?' % col for col in cols]), UPDATE_TIME, pk)
        else:
            sql = 'UPDATE `%s` SET %s, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, ','.join(['`%s`=?' % col for col in cols]), UPDATE_TIME, pk)
        db.do_execute(sql, *args)

    @classmethod
    def delete_by_id(cls, id: int):
        pk, table = Model._get_pk_and_table(cls)
        sql = 'DELETE FROM `%s` WHERE `%s`=? limit 1' % (table, pk)
        return db.do_execute(sql, id)

    @classmethod
    def delete_by_ids(cls, ids: Iterable[int]):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'
        pk, table = Model._get_pk_and_table(cls)
        sql = 'DELETE FROM `%s` WHERE `%s` in (%s) limit %d' % (table, pk, ','.join(list(map(str, ids))), ids_size)
        return db.do_execute(sql)

    @classmethod
    def logic_delete_by_id(cls, id: int, update_by: int = None):
        pk, table = Model._get_pk_and_table(cls)
        if update_by is None:
            sql = 'UPDATE `%s` SET `del_flag`=1, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, UPDATE_TIME, pk)
            return db.do_execute(sql, id)
        else:
            sql = 'UPDATE `%s` SET `del_flag`=1, `update_by`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, UPDATE_TIME, pk)
            return db.do_execute(sql, update_by, id)

    @classmethod
    def logic_delete_by_ids(cls, ids: Iterable[int], update_by: int = None):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'
        pk, table = Model._get_pk_and_table(cls)
        ids_str = ','.join(list(map(str, ids)))
        if update_by is None:
            sql = 'UPDATE `%s` SET `del_flag`=1, `%s`=CURRENT_TIMESTAMP WHERE `%s` in (%s) limit %d' % (table, UPDATE_TIME, pk, ids_str, ids_size)
            return db.execute(sql)
        else:
            sql = 'UPDATE `%s` SET `del_flag`=1, `update_by`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s` in (%s) limit %d' % (table, UPDATE_TIME, pk, ids_str, ids_size)
            return db.do_execute(sql, update_by)

    @classmethod
    def find_all(cls, *selection, limit=100):
        pk, table = Model._get_pk_and_table(cls)
        if len(selection) == 0:
            sql = 'SELECT * FROM `%s` limit %d' % (table, limit)
        else:
            sql = 'SELECT %s FROM `%s` limit %d' % (','.join(['`%s`' % col for col in selection]), table, limit)
        return [Model.dict2obj(d, cls, pk, table) for d in db.do_select(sql)]

    @staticmethod
    def _get_pk_and_table(cls):
        pk = Model._get_pk(cls)
        table = Model._get_table(cls)
        return pk, table

    @staticmethod
    def _get_pk(cls):
        pk = cls.__dict__.get(PK)
        return pk if pk else 'id'

    @staticmethod
    def _get_table(cls):
        table = cls.__dict__.get(TABLE)
        return table if table else cls.__name__.lower()

    @staticmethod
    def dict2obj(dictionary, cls, pk, table):
        m = Model()
        m.__dict__.update(dictionary)
        m.__class__ = cls
        if cls.__dict__.get(PK) is not None:
            m.__pk__ = pk
        if cls.__dict__.get(TABLE) is not None:
            m. __table__ = table
        return m
