''' Exceptions classes of apiv1 '''


class LayoutJsonFormatException(Exception):
    ''' Raised when the json format of layout is invalid '''

class RouteValueException(Exception):
    ''' Raised when source or destination of route is empty '''