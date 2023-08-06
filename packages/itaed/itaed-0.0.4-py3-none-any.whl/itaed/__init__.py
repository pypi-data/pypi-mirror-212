from itaed.click import Click
from itaed.tools import Tools
from itaed.exception import ExceptionCheck
from itaed.enviroments import Enviroments
click=Click()
tools=Tools()
exception=ExceptionCheck()
enviroments = Enviroments()
__all__=['click', 'tools', 'exception', 'enviroments']