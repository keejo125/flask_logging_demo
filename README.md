## Flask中logging的使用

logging在一个工厂模式的flask中使用的demo。实现通过flask自带的logger和自定义的logger来记录日志。

# 使用步骤
 - 安装依赖。

   ```shell
   pip3 install -r requirements.txt
   ```

 - 启动LogServer。

   ```python
   python LogServer.py
   ```

 - 启动flask

   ```python
   python manager runserver
   ```

- 使用flask的logger记录日志：
  - view模块访问：http://localhost:5000/test1
  - function模块：http://localhost:5000/test2
- 使用自定义的logger记录日志：
  - view模块访问：http://localhost:5000/module/test1
  - function模块：http://localhost:5000/module/test2
- 在`LogServer`的`console`中查看日志输出。

## 说明

- `Python`的`logging`模块

  先看下对于`logging`模块的官方介绍

  > Loggers have the following attributes and methods. Note that Loggers are never instantiated directly, but always through the module-level function `logging.getLogger(name)`. Multiple calls to [`getLogger()`](https://docs.python.org/3/library/logging.html#logging.getLogger) with the same name will always return a reference to the same Logger object.
  >
  > The `name` is potentially a period-separated hierarchical value, like `foo.bar.baz` (though it could also be just plain `foo`, for example). Loggers that are further down in the hierarchical list are children of loggers higher up in the list. For example, given a logger with a name of `foo`, loggers with names of `foo.bar`, `foo.bar.baz`, and `foo.bam` are all descendants of `foo`. The logger name hierarchy is analogous to the Python package hierarchy, and identical to it if you organise your loggers on a per-module basis using the recommended construction `logging.getLogger(__name__)`. That’s because in a module, `__name__` is the module’s name in the Python package namespace.
  >
  > https://docs.python.org/3/library/logging.html#logger-objects

  上面主要告诉我们两点，

  - 可以通过`logging.getLogger(name)`来获取一个`logger`，相同名字的`logger`，其实是同一个`logger`。
  - `logger`是通过`name`进行继承的，比如`foo.bar`就是`foo` 的子`logger`。就可以是实现我们通过配置一个`rootLogger`，然后直接使用`rootLogger.sublogger`来记录一下内容，而不需要单独再配置一遍。
  - 当使用`logging.getLogger(__name__)`时，`__name__`就是这个模块所在的`python package`的`namespace`。

- flask提供的logger

  再看下flask中的logging模块：

  > Flask uses standard Python [`logging`](https://docs.python.org/3/library/logging.html#module-logging). All Flask-related messages are logged under the `'flask'` logger namespace.[`Flask.logger`](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.logger) returns the logger named `'flask.app'`, and can be used to log messages for your application.

  > Depending on the situation, an extension may choose to log to [`app.logger`](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.logger) or its own named logger. Consult each extension’s documentation for details.

  > http://flask.pocoo.org/docs/1.0/logging/

  我们可以知道flask的logger就是一个标准的Python logging，它的命名是`flask`。我们既可以使用`app.logger`，也可以自己定义一个`logger`。

  那么如何使用`app.logger`呢？

  有两种方式：

  - 直接调用

    ```python
    logger = logging.getLogger('flask.app')
    logger.info('flask.app')
    ```

  - 使用`Flask`提供的接口

    ```python
    from flask import current_app
    current_app.logger.info('logged by current_app from main')
    ```

  这里推荐还是使用第二种，`current_app`是一个单例，可以直接引用到`app.logger`。

- 通过修改`app.logger`的`name`，可以实现子`logger`的继承么？

  答案是否定的。

  - 修改`app.logger`的`name`：

    ```python
    # app/__init__.py
    app.logger.name = 'app'
    ```

    然后在子模块中定义一个`app.module`的`logger`来记录：

    ```python
    from flask import current_app
    import logging
    
    logger = logging.getLogger('app.module')
    
    @module.route('/test', methods=['GET'])
    def test():
        logger.info('logged by app.module')
        current_app.logger.info('logged by current_app.logger')
    ```

    输出结果：

    ```shell
    2019-02-01 10:56:01,877 - Thread-2 - app - INFO - logged by current_app.logger
    ```

    只有`current_app.logger`的输出。

  - 修改`app.logger`的`name`是不是无效呢？

    我们把子模块中的`logger`的`name`修改为`flask.app.module`：

    ```python
    from flask import current_app
    import logging
    
    logger = logging.getLogger('flask.app.module')
    
    @module.route('/test', methods=['GET'])
    def test():
        logger.info('logged by flask.app.module')
        current_app.logger.info('logged by current_app.logger')
    ```

    输出结果：

    ```shell
    2019-02-01 11:00:10,944 - Thread-2 - flask.app.module - INFO - logged by flask.app.module
    2019-02-01 11:00:10,946 - Thread-2 - app - INFO - logged by current_app.logger
    ```

    两个`logger`均输出了。

  可见，通过修改`app.logger.name`可以在记录的时候显示为我们设置的名称，但实际上这个`logger`还是`flask.app`。

- `__name__`的使用

  在自定义`logger`的情况下，为了方便起见，我们可以利用`__name__`这个参数。

  前面说到：当使用`logging.getLogger(__name__)`时，`__name__`就是这个模块所在的`python package`的`namespace`。

  一般`Flask`的工厂模式结构如下：

  ```shell
  app
  ├── __init__.py
  ├── main
  │   ├── __init__.py
  │   ├── functions.py
  │   └── views.py
  └── module
      ├── __init__.py
      ├── functions.py
      └── views.py
  ```

  那么我们在先在`app.__init__`中定义`rootLogger`，然后再在`app.module.functions.py`中定义子`Logger`，均使用`logging.getLogger(__name__)`:

  ```python
  # app.__init__.py 初始化rootlogger
  rootLogger = logging.getLogger(__name__)
      rootLogger.setLevel(logging.DEBUG)
      socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
      rootLogger.addHandler(socketHandler)
      rootLogger.setLevel(logging.DEBUG)
  
  # app.module.functions.py
  import logging
  
  logger = logging.getLogger(__name__)
  
  def record_from_logging():
      logger.info('logged by logging from __name__')
  ```

  输出：

  ```shell
  2019-02-01 12:18:34,743 - MainThread - app - INFO - register root logger by __name__
  2019-02-01 12:19:24,954 - Thread-4 - app.module.functions - INFO - logged by logging from __name__
  ```

  可以发现输出的`logger.name`就是所在的文件目录，`logger`之间的继承关系与整个程序包保持一致。

## 总结

根据上面分析，那么怎么优雅的记录`logger`呢？

- 如果没有对模块进行分`logger`记录要求的话。可以直接使用在程序初始化的时候配置`app.logger`（可以自行设置`logger.name`）。参考`main`模块。

  ```python
  # app.__init__.py
  def register_logging(app):
      app.logger.name = 'app'
      # logstash_handler
      stashHandler = logstash.LogstashHandler('app.config.get('ELK_HOST')', 'app.config.get('ELK_PORT')')
      app.logger.addHandler(stashHandler)
  
      # socket_handler
      socketHandler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
      app.logger.addHandler(socketHandler)
      
  # app.module.function.py
  from flask import current_app
  
  @module.route('/test', methods=['GET'])
  def test():
      current_app.logger.info('logging someting')
      return 'logged by current_app.logger'
  ```

  输出效果：

  ```shell
  2019-02-01 13:49:28,998 - Thread-2 - app - INFO - logged by current_app from main
  2019-02-01 13:49:38,346 - Thread-3 - app - INFO - logged by current_app of functions
  ```

  __注意__: 对于`current_app.logger`的引用不能通过如下方式，会有`RuntimeError`的报错。

  ```python
  from flask import current_app
  
  logger = current_app.logger
  
  ## 异常
      raise RuntimeError(_app_ctx_err_msg)
  RuntimeError: Working outside of application context.
  
  This typically means that you attempted to use functionality that needed
  to interface with the current application object in some way. To solve
  this, set up an application context with app.app_context().  See the
  documentation for more information.
  
  ```

- 如果希望按自己的实际需求，对模块进行分`logger`记录要求的话。那么建议自己设置`logger`。参考`module`模块。

  ```python
  # app.__init__.py
  def register_logging():
      # set own root logger
      rootLogger = logging.getLogger(__name__)
      rootLogger.setLevel(logging.DEBUG)
      # socketHandler
      socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
      rootLogger.addHandler(socketHandler)
      # logstash_handler
      stashHandler = logstash.LogstashHandler('app.config.get('ELK_HOST')', 'app.config.get('ELK_PORT')')
      rootLogger.addHandler(stashHandler)
      rootLogger.setLevel(logging.DEBUG)
  
  # app.module.function.py
  import logging
  
  logger = logging.getLogger(__name__)
  
  @module.route('/test', methods=['GET'])
  def test():
      logger.info('logging someting')
      return 'logged by logging module'
  ```

  输出效果：

  ```shell
  2019-02-01 13:49:49,297 - Thread-5 - app.module.views - INFO - logged by flask.app.module
  2019-02-01 13:50:01,013 - Thread-7 - app.module.functions - INFO - logged by logging module of functions
  ```

## 注意

关于`python`中`logging`的配置可参考官网：

> https://docs.python.org/3/library/logging.config.html?highlight=logging

在配置`handler`时，经常会希望日志可以按时间分割([TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler))或者按大小分割([RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)).

但是在`flask`项目中，尤其开启多线程之后，在分割日志(`doRollover()`)时会有文件读写的异常:

```shell
WindowsError: [Error 32]
```

建议使用[SocketHandler](https://docs.python.org/3/library/logging.handlers.html#sockethandler)，将日志发送给单独的`LogServer`来进行二次处理。

一个简单的接受SocketLog的Server参考`LogServer.py`。

或者现在流行的[stashHandler](https://pypi.org/project/python-logstash/)，将日志发送给ELK来进行二次处理。



