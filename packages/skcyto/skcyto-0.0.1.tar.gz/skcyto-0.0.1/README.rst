.. -*- mode: rst -*-

|Travis|_ |Codecov|_ |CircleCI|_ |ReadTheDocs|_

.. |Travis| image:: https://app.travis-ci.com/MSHelm/sk-cyto.svg?branch=main
.. _Travis: https://app.travis-ci.com/MSHelm/sk-cyto

.. |Codecov| image:: https://codecov.io/gh/MSHelm/sk-cyto/branch/main/graph/badge.svg?token=J4VXARST8A
.. _Codecov: https://codecov.io/gh/MSHelm/sk-cyto

.. |CircleCI| image:: https://circleci.com/gh/MSHelm/sk-cyto.svg?style=shield
.. _CircleCI: https://circleci.com/gh/MSHelm/sk-cyto/

.. |ReadTheDocs| image:: https://readthedocs.org/projects/sk-cyto/badge/?version=latest
.. _ReadTheDocs: https://sk-cyto.readthedocs.io/en/latest/?badge=latest

sk-cyto - Flow cytometry algorithms for scikit-learn
============================================================


**sk-cyto** brings flow cytometry to scikit-learn.

Flow cytometry is extremely amenable to regular machine learning algorithms. At the same time,
it requires specific data transformations, and various dedicated analysis methods have been developed.
sk-cyto allows you to combine the best of sk-learn infrastructure with dedicated cytometry analysis methods.
Use established patterns, such as ``Pipeline`` and existing ``Transformers`` together with state-of-the-art
algorithms like ``FlowSOM``.

.. _documentation: https://sk-cyto.readthedocs.io/en/latest/quick_start.html

Refer to the documentation_ for a full list of available ``Transformers`` and ``Estimators``

This package is work in progress. New features and algorithms will be implemented frequently.


Installation
============

From PyPI
.. code-block::

    pip install sk-cyto

Install from Github source code with
.. code-block::
    
    git clone git@github.com:MSHelm/sk-cyto.git
    cd sk-cyto
    pip install .

