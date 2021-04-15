from datetime import datetime

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3
FATAL = 4


class Logger():
    def __init__(self,filename=None,level=DEBUG,append=False):
        if level not in [i for i in range(0,5)]:
            raise ValueError(f"Logger: Invalid value for level {level}")
        self.filename = filename
        self.isFile = bool(filename is not None)
        self.level = level
        self.append = append
        self.levels = {
            "0" : "debug",
            "1" : "info",
            "2" : "warn",
            "3" : "error",
            "4" : "fatal"
        }
    
    def __repr__(self):
        string = f"""
Logger class with settings:
- Filename: {self.filename}
- Level: {self.levels[str(self.level)].upper()}
"""
        return string

    def __return_format(self,level,message):
        now = str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        level_str = self.levels[str(level)]
        return f"[{now}][{level_str.upper()}] - {message}"

    def __file_message(self,level,message):
        stream = None
        if self.append:
            stream = open(self.filename,"a+")
            stream.write(" ")
        else:
            stream = open(self.filename,"w+")
        stream.write(self.__return_format(level,message))

    def __print_message(self,level,message):
        print(self.__return_format(level,message))

    def __execute(self,level,message,stop=False):
        if self.level >= level:
            if self.isFile:
                self.__file_message(level,message)
            if not stop:
                self.__print_message(level,message)
            else:
                raise ValueError(self.__return_format(level,message))

    def debug(self,message):
        self.__execute(0,message)
    
    def info(self,message):
        self.__execute(1,message)
    
    def warn(self,message):
        self.__execute(2,message)
    
    def error(self,message):
        self.__execute(3,message)
    
    def fatal(self,message,stop=True):
        self.__execute(4,message,stop)
        
