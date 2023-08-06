from . import db
from typing import Iterable

PK, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG = '__pk__', '__table__', '__update_by__', '__update_time__', '__del_flag__'
SYMBOLS = ['=', '>', '<']
BETWEEN, LIKE, IN = 'between', 'like', 'in'


def _get_condition_arg(k, v):
    if not isinstance(v, str):
        return "`%s`=?" % k, v
    v_lower = v.lower()
    if any([symbol in SYMBOLS for symbol in v_lower]):
        return "`%s`%s" % (k, v), None
    elif BETWEEN in v_lower or LIKE in v_lower or IN in v_lower:
        return "`%s` %s" % (k, v), None
    else:
        return "`%s`=?" % k, v


def _get_where_args(**kwargs):
    if kwargs:
        conditions, args = zip(*[_get_condition_arg(k, v) for k, v in kwargs.items()])
        args = [arg for arg in args if arg is not None]
        where = 'WHERE %s' % ' and '.join(conditions)
        return where, args
    return '', []


class Model:
    def __str__(self):
        kv = {k: v for k, v in self.__dict__.items() if not k.startswith("__")}
        return str(kv)

    def __getattr__(self, name):
        if PK == name:
            return 'id'
        elif TABLE == name:
            return self.__class__.__name__.lower()
        elif UPDATE_BY == name:
            return 'update_by'
        elif UPDATE_TIME == name:
            return 'update_time'
        else:
            return None

    def persist(self):
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        self.id = db.save(self._get_table(), **kv)
        return self.id

    def update(self):
        pk, table = self._get_pk_and_table()
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        if pk not in kv:
            raise KeyError("Not primary key.")

        update_kv = {k: v for k, v in kv.items() if k != pk}
        if update_kv:
            cols, args = zip(*update_kv.items())
            args = [*args, kv[pk]]
            update_time_col = self._get_update_time_col()
            if update_time_col is None or update_time_col in update_kv:
                sql = 'UPDATE `%s` SET %s WHERE `%s`=? limit 1' % (table, ','.join(['`%s`=?' % col for col in cols]), pk)
            else:
                sql = 'UPDATE `%s` SET %s, %s=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, ','.join(['`%s`=?' % col for col in cols]), update_time_col, pk)
            db.do_execute(sql, *args)

    def load(self):
        pk, table = self._get_pk_and_table()
        kv = self.__dict__
        _id = kv.get(pk)
        if _id is not None:
            cols, _ = zip(*kv.items())
            sql = 'SELECT %s FROM `%s` WHERE `%s`=? limit 1' % (','.join(['`%s`' % col for col in cols]), table, pk)
            self.__dict__.update(db.do_select_one(sql, _id))
            return self
        else:
            raise KeyError("Not primary key.")

    def delete(self):
        pk, table = self._get_pk_and_table()
        _id = self.__dict__.get(pk)
        if _id is None:
            raise KeyError("Not primary key.")

        sql = 'DELETE FROM `%s` WHERE `%s`=? limit 1' % (table, pk)
        return db.do_execute(sql, _id)

    def logic_delete(self, update_by: int = None):
        pk, table = self._get_pk_and_table()
        _id = self.__dict__.get(pk)
        if _id is None:
            raise KeyError("Not primary key.")

        return self.logic_delete_by_id(_id, update_by)

    @classmethod
    def insert(cls, **kwargs):
        table = cls._get_table()
        return db.insert(table, **kwargs)

    @classmethod
    def save(cls, **kwargs):
        table = cls._get_table()
        return db.save(table, **kwargs)

    @classmethod
    def find_by_id(cls, id: int, *selection):
        """
        Return one object or None if no result.
        """
        result = cls.select_by_id(id, *selection)
        return cls._dict2obj(result) if result else None

    @classmethod
    def find_by_ids(cls, ids: Iterable[int], *selection):
        """
        Return list(object) or empty list if no result.
        """
        return [cls._dict2obj(d) for d in cls.select_by_ids(ids, *selection)]

    @classmethod
    def select_by_id(cls, id: int, *selection):
        """
        Return one row(dict) or None if no result.
        """
        pk, table = cls._get_pk_and_table()
        if len(selection) == 0:
            sql = 'SELECT * FROM `%s` WHERE `%s`=? limit 1' % (table, pk)
        else:
            sql = 'SELECT %s FROM `%s` WHERE `%s`=? limit 1' % (','.join(['`%s`' % col for col in selection]), table, pk)
        return db.do_select_one(sql, id)

    @classmethod
    def select_by_ids(cls, ids: Iterable[int], *selection):
        """
        Return list(dict) or empty list if no result.
        """
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'
        pk, table = cls._get_pk_and_table()
        ids_str = ','.join(list(map(str, ids)))
        if len(selection) == 0:
            sql = 'SELECT * FROM `%s` WHERE `%s` in (%s) limit %d' % (table, pk, ids_str, ids_size)
        else:
            sql = 'SELECT %s FROM `%s` WHERE `%s` in (%s) limit %d' % (','.join(['`%s`' % col for col in selection]), table, pk, ids_str, ids_size)
        return db.do_select(sql)

    @classmethod
    def update_by_id(cls, id: int, **kwargs):
        assert kwargs, 'Must set update kv'
        pk, table = cls._get_pk_and_table()
        cols, args = zip(*kwargs.items())
        args = [*args, id]
        update_time_col = cls._get_update_time_col()
        if update_time_col is None or update_time_col in kwargs:
            sql = 'UPDATE `%s` SET %s WHERE `%s`=? limit 1' % (table, ','.join(['`%s`=?' % col for col in cols]), pk)
        else:
            sql = 'UPDATE `%s` SET %s, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, ','.join(['`%s`=?' % col for col in cols]), update_time_col, pk)
        db.do_execute(sql, *args)

    @classmethod
    def delete_by_id(cls, id: int):
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM `%s` WHERE `%s`=? limit 1' % (table, pk)
        return db.do_execute(sql, id)

    @classmethod
    def delete_by_ids(cls, ids: Iterable[int]):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM `%s` WHERE `%s` in (%s) limit %d' % (table, pk, ','.join(list(map(str, ids))), ids_size)
        return db.do_execute(sql)

    @classmethod
    def logic_delete_by_id(cls, id: int, update_by: int = None):
        pk, table = cls._get_pk_and_table()
        del_flag_col = cls._get_del_flag_col()
        update_by_col = cls._get_update_by_col()
        update_time_col = cls._get_update_time_col()

        if update_by is None or update_by_col is None:
            if update_time_col:
                sql = 'UPDATE `%s` SET `%s`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, del_flag_col, update_time_col, pk)
            else:
                sql = 'UPDATE `%s` SET `%s`=? WHERE `%s`=? limit 1' % (table, del_flag_col, pk)
            return db.do_execute(sql, 1, id)
        else:
            if update_time_col:
                sql = 'UPDATE `%s` SET `%s`=?, `%s`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s`=? limit 1' % (table, del_flag_col, update_by_col, update_time_col, pk)
            else:
                sql = 'UPDATE `%s` SET `%s`=?, `%s`=? WHERE `%s`=? limit 1' % (table, del_flag_col, update_by_col, pk)
            return db.do_execute(sql, 1, update_by, id)

    @classmethod
    def logic_delete_by_ids(cls, ids: Iterable[int], update_by: int = None):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        pk, table = cls._get_pk_and_table()
        ids_str = ','.join(list(map(str, ids)))
        del_flag_col = cls._get_del_flag_col()
        update_by_col = cls._get_update_by_col()
        update_time_col = cls._get_update_time_col()

        if update_by is None or update_by_col is None:
            if update_time_col:
                sql = 'UPDATE `%s` SET `%s`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s` in (%s) limit %d' % (table, del_flag_col, update_time_col, pk, ids_str, ids_size)
            else:
                sql = 'UPDATE `%s` SET `%s`=?, WHERE `%s` in (%s) limit %d' % (table, del_flag_col, pk, ids_str, ids_size)
            return db.execute(sql, 1)
        else:
            if update_time_col:
                sql = 'UPDATE `%s` SET `%s`=?, `%s`=?, `%s`=CURRENT_TIMESTAMP WHERE `%s` in (%s) limit %d' % (table, del_flag_col, update_by_col, update_time_col, pk, ids_str, ids_size)
            else:
                sql = 'UPDATE `%s` SET `%s`=?, `%s`=?, WHERE `%s` in (%s) limit %d' % (table, del_flag_col, update_by_col, pk, ids_str, ids_size)
            return db.do_execute(sql, 1, update_by)

    @classmethod
    def find(cls, *selection, **kwargs):
        """
        Return list(object) or empty list if no result.
        """
        pk, table = cls._get_pk_and_table()
        return [cls._dict2obj(d) for d in cls.select(*selection, **kwargs)]

    @classmethod
    def select(cls, *selection, **kwargs):
        """
        Return list(dict) or empty list if no result.
        """
        where, args = '', []
        if kwargs:
            limit = kwargs.get('limit')
            if limit:
                del kwargs['limit']
            where, args = _get_where_args(**kwargs)
        else:
            limit = 1000

        limit_str = 'limit %d' % limit if limit else ''
        pk, table = cls._get_pk_and_table()
        if len(selection) == 0:
            sql = 'SELECT * FROM `%s` %s %s' % (table, where, limit_str)
        else:
            sql = 'SELECT %s FROM `%s` %s %s' % (','.join(['`%s`' % col for col in selection]), table, where, limit_str)
        return db.do_select(sql, *args)

    @classmethod
    def _get_pk_and_table(cls):
        assert hasattr(cls, PK), "%s not set attribute '%s'" % (cls.__name__, PK)
        return cls.__pk__, cls._get_table()

    @classmethod
    def _get_table(cls):
        assert hasattr(cls, TABLE), "%s not set attribute '%s'" % (cls.__name__, TABLE)
        return cls.__table__

    @classmethod
    def _dict2obj(cls, dictionary):
        m = Model()
        m.__dict__.update(dictionary)
        m.__class__ = cls
        return m

    @classmethod
    def _get_update_by_col(cls):
        if hasattr(cls, UPDATE_BY):
            return cls.__update_by__
        return None

    @classmethod
    def _get_update_time_col(cls):
        if hasattr(cls, UPDATE_TIME):
            return cls.__update_time__
        return None

    @classmethod
    def _get_del_flag_col(cls):
        assert hasattr(cls, DEL_FLAG), "%s not set attribute '%s'" % (cls.__name__, DEL_FLAG)
        return cls.__del_flag__
