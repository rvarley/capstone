E-Bike Configurator
-------------------

**E-Bike Configurator is a tool for perspective E-Bike purchasers to make informed purchasing decisions**

Built With
----------

* Python 3.5
* Python 2.7
* Django 1.8
* Scrapy 1.0.3
* PostgreSQL
* JavaScript
* jQuery
* Bootstrap 3.3.6
* Sublime Text 2
* pip 7.1.2

Site Demo
---------

.. image:: e-bike-demo-1.gif

Prerequisites
-------------

* Basic Python knowledge.
* Installed [Python](https://www.python.org) and [Virtualenv](https://github.com/kennethreitz/python-guide/blob/master/docs/dev/virtualenvs.rst) in a unix-style environment. See this [guide](http://docs.python-guide.org/en/latest/starting/install/osx/) for guidance.
* Your application must use pip to resolve dependencies.

Before attempting to run the configurator, run the propel_spider.py web scraper.
This scraper uses scrapy, which at the time of this writing (21-Jan-2016) required
python 2.7.  

Set up a Python 2.7 virtural environment with packages installed as described in venv_python_2.7.txt

Start the virtual environment and run the scraper with the following command - 'scrapy runspider propel_spider.py'.  This will populate
the postgres database.

The configurator should be run in a Python 3.5 virtual environment with the following packages installed:
Set up a virtural environment with packages installed as described in venv_python_3.5.txt

Installation
------------
"Requirements files" are files containing lists of items to be installed using pip install like so:

`pip install -r requirements.txt`

A fork is a copy of a repository. Forking a repository allows you to freely experiment with changes without affecting the original project. 

On GitHub, navigate to the [https://github.com/rvarley/capstone) repository. See this [guide](https://help.github.com/articles/fork-a-repo/) for guidance to fork the repository.


Contributing
------------

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

History
-------

TODO: Write history

Credits
-------

Other support:
-------------
* User Authentication by [How to Tango with Django 1.7](http://www.tangowithdjango.com/book17/chapters/login.html)
* README.md template for this project by [zenorocha](https://gist.github.com/zenorocha/4526327)
* Bootstrap: how do I change the width of the container by [Robbie Averill](http://stackoverflow.com/questions/15884102/bootstrap-how-do-i-change-the-width-of-the-container)
* Try Django 1.8 by [Coding for Entrepreneurs](https://codingforentrepreneurs.com/projects/try-django-18/)
* Get all users in a group in Django by [digitaldreamer](http://digitaldreamer.net/blog/2010/5/10/get-all-users-group-django/)
* Django - iterate number in for loop of a template by [GergelyPolonkai](http://stackoverflow.com/questions/11481499/django-iterate-number-in-for-loop-of-a-template)
* Django {{ request.user.username }} doesn't render in template by [Tadeck](http://stackoverflow.com/questions/10158871/django-1-4-request-user-username-doesnt-render-in-template)
* Django The 'image' attribute has no file associated with it by [iMom0](http://stackoverflow.com/questions/15322391/django-the-image-attribute-has-no-file-associated-with-it)
* Getting started with Generic Class Based Views in Django by [onespacemedia](http://www.onespacemedia.com/news/2014/feb/5/getting-started-generic-class-based-views-django/)
* Changing Menu Order on Collapsed Navbar in Bootstrap 3 by [Tom Patrick](http://stackoverflow.com/questions/23875090/changing-menu-order-on-collapsed-navbar-in-bootstrap-3)
* How to make a whole row in a table clickable as a link by [Axel Fontaine](how to make a whole row in a table clickable as a link?)
* No need to use get_context_data, use {{ view.some_method }} by [Reinout van Rees](http://reinout.vanrees.org/weblog/2014/05/19/context.html)
* Django build URLs from template with integer param, the primary key [Ned Batchelder](http://stackoverflow.com/questions/11149288/django-build-urls-from-template-with-integer-param-the-primary-key)
* Django filter with list of values by [charlax](http://stackoverflow.com/questions/9304908/django-filter-with-list-of-values)
* Django sending email by [mongoose_za](http://stackoverflow.com/questions/6914687/django-sending-email)
* Django: login takes exactly 1 argument (2 given) by [Roberto Liffredo](http://stackoverflow.com/questions/14111539/django-login-takes-exactly-1-argument-2-given)
* Error: “dictionary update sequence element #0 has length 1; 2 is required” on Django by [Thane Brimhall](http://stackoverflow.com/questions/17610732/error-dictionary-update-sequence-element-0-has-length-1-2-is-required-on-dj)
* Updating User model in Django with class based UpdateView by [Ricardo Murillo](http://stackoverflow.com/questions/6181041/updating-user-model-in-django-with-class-based-updateview)

License
-------
Copyright (c) 2015 E-Bike Configurator by VarleyRansom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE

Questions
---------
For questions, please contact me on [Twitter](https://twitter.com/ransomv).
