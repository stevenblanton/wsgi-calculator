import traceback
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def how_to_use(*args):
    """ How to use calculator.py """

    html_code ="<html><body>" \
               "<h2>The Calculator supports the following operations:</h2><br>" \
               "<h4>Multiplication:</h4> /multiply/num1/num2/...<br>" \
               "<h4>Addition:</h4> /add/num1/num2/...<br>" \
               "<h4>Subtraction: </h4> /subtract/num1/num2/...<br>" \
               "<h4>Division:</h4> /divide/num1/num2/...<br>" \
               "<br>" \
               "<h4>Examples:</h4>" \
               "<br>http://localhost:8080/multiply/3/5 => 15" \
               "<br>http://localhost:8080/add/23/42/2 => 67" \
               "<br>http://localhost:8080/subtract/23/42 => -19" \
               "<br>http://localhost:8080/divide/22/11 => 2" \
               "</body></html>"

    return html_code


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0
    for arg in args:
        sum += int(arg)

    return str(sum)


def subtract(*args):
    """ Returns a STRING with the subtraction of the arguments """
    sub = int(args[0])
    for arg in args[1:]:
        sub -= int(arg)

    return str(sub)


def multiply(*args):
    """ Returns a STRING with the sum of the arguments """

    mult = 1
    for arg in args:
        mult *= int(arg)

    return str(mult)


def divide(*args):
    """ Returns a STRING with the sum of the arguments """

    div = int(args[0])
    for arg in args[1:]:
        if arg == 0:
            raise ZeroDivisionError
        div /= int(arg)

    return str(div)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'index': how_to_use
    }

    path = path.strip('/').split('/')

    if len(path) == 1:
        return funcs['index'], [0]

    print("test")
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Bad Request - Cannot divide by 0</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)

        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
