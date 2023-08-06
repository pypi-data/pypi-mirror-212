Data Dictionary For Python Imas Model
=====================================

This Python script converts an IDS  dictionary to a Python class.

Prerequisites
=============

To use this script, you need to have Python **3.10** or later installed. You can download Python from https://www.python.org/downloads/.

Installation
============

To install the necessary packages, run the following command:

.. code-block:: console

   python -m pip install idspy_dictionaries

Usage
=====

To load the desired IDS :

.. code-block:: python

   from idspy_dictionaries import ids_gyrokinetics # or any other available IDS
   new_ids = ids_gyrokinetics.Gyrokinetics()

FAQ
===

**Q:** What is the minimum required version of Python to run this script?  
**A:** The minimum required version of Python is 3.10.


**Q:** Can I load all the dictionaries at once?  
**A:** For performances reasons, it's not possible right now

**Q:** Can I add new members to the dataclasses?  
**A:** By default it's not possible to be sure that the dataclasses follow the IMAS conventions. 
