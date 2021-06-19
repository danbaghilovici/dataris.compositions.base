from __future__ import annotations
from typing import TYPE_CHECKING,Dict,List
import time
if TYPE_CHECKING:
    from utils.models.composition_info import DATARISCompositionInfo
    from utils.models.timed_operation import DATARISCompositionOperation

class DATARISCompositionBase():
    version='0.0.1'

    __trans={}

    __id='__DATARIS_composition_base'
    __accepts=None
    __returns=None

    @classmethod
    def getCompositionId(cls)->str:
        return cls.__id

    @classmethod
    def getTranslations(cls)->Dict:
        return cls.__trans


    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs

        self._errors:List[Exception]=[]
        self._warnings:List[any]=[]

    def _appendError(self,err:Exception):
        self._errors.append(err)

    def _appendWarning(self,err:any):
        self._warnings.append(err)

    def __call__(self, *args, **kwargs)->DATARISCompositionOperation:
        res:DATARISCompositionOperation={
            'time':0,
            'result':None,
            'name':self.getCompositionInfo(),
            'iteration':1,
            'done':False,
            'errors':[],
            'warnings':[]
        }
        start_time=0
        end_time=-1
        try:
            # if
            start_time=time.time()
            res['result']=self._handle(args[0]) if len(args) > 0 else None
            res['done']=True
        except Exception as e:
            self._appendError(e)
            res['result']=None
            res['done'] = False # todo find if this might cause problems
            raise e
        finally:
            end_time=time.time()
            res['time']=end_time-start_time
            res['errors']=self._errors
            res['warnings']=self._warnings
            return res

    def _handle(self, arg):
        raise NotImplementedError()

    def getCompositionInfo(self, *args)->DATARISCompositionInfo:
        return {'name':self.__class__,'args':self.args,'kwargs':self.kwargs}

    @staticmethod
    def createIUNCTIOCompositionFromJson(obj:Dict[any]):

        return {}

if __name__ == '__main__':
    d=DATARISCompositionBase('aa')
    d._handle(11)