from typing import Callable
from .logger_helper import logger


class ISO_code_reminder:
    """数据描述符,如未设置iso_code ,则会提示报错！
    """

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_reminder_"+name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        value = getattr(instance, self.private_name, None)
        if value is None:
            logger.warning(
                f"{instance} does not set {self.public_name}! please set it")
            raise NotImplementedError(
                f"还未设置{instance}对象的{self.public_name}值呢！")
        return value

    def __set__(self, instance, value):
        if not isinstance(value,str):
            raise TypeError(
                f"{self.public_name} must be a string, not {type(value).__name__}")

        setattr(instance, self.private_name, value)


class Input_reminder:

    def __init__(self,target_type_cls=object):
        self.target_type_cls = target_type_cls
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_reminder_"+name
    
    def __get__(self, instance, cls):
        if instance is None:
            raise self
        value = getattr(instance, self.private_name, None)
        if value is None:
            logger.warning(
                f"{instance} does not set attr :{self.public_name}! please set it")
            raise NotImplementedError(
                f"还未设置{instance}对象的{self.public_name}值呢！")
        return value
    
    def __set__(self, instance, value):
        if not isinstance(value,self.target_type_cls):
            raise TypeError(
                f"{self.public_name} must be a {self.target_type_cls.__name__}, not {type(value).__name__}")
        setattr(instance, self.private_name, value)

class Based_Data:
    """数据描述符，基于已有数据和处理函数生成新的只读属性
    """
    
    def __init__(self,based_attr_name:str,func:Callable):
        self.based_attr_name=str(based_attr_name)
        self.func=func
        
    def __set_name__(self, owner, name):
        self.public_name=name
        self.private_name="_lazypropety_"+name
    
    def __get__(self, instance, cls):
        if instance is None:
            return self
        if hasattr(instance,self.private_name):
            return getattr(instance,self.private_name)
        print("calculating...")
        based_data=getattr(instance,self.based_attr_name)
        res=self.func(based_data)
        setattr(instance,self.private_name,res)
        return res
        
    def __set__(self, instance, value):
        raise ValueError(f"{instance} attr `{self.public_name}` is read only!")

        
        
        
    
    

