uu.task: UPIQ Task Management Add-on for Plone
==============================================

This repository serves as a location for development of the ``uu.task`` task management add-on for Plone.

Introduction
------------

``uu.task`` provides configurable, effective task-related **email
notifications** to **assigned parties**. It provides features:

1. for project managers to configure and assign content items e.g. forms
   & events as **tasks with due dates**

#. for assigned parties to receive email notification about tasks **at specific
   times**

#. for assigned parties to communicate task status to project managers and
   **set notification preferences**

Content Types
-------------

``uu.task`` adds two new content types to your Plone site:

- **Task**
- **Task Planner**

.. image:: screenshot.png

Demo
----

A demo site is available here:

- http://uu-task-demo.herokuapp.com/

Similar Add-ons
---------------

``uu.task`` is inspired by similar add-ons. Here is a comparison of each.

+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
| **Add-ons**                          |  **Description**                      |  **Pros**                             |  **Cons**                             |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
| Products.Poi_                        | Venerable AT-based issue tracker.     | N/A                                   | N/A                                   |
|                                      | Includes workflow for issue tracker   |                                       |                                       |
|                                      | and task.                             |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
| collective.project_                  | Project management add-on whose       | N/A                                   | N/A                                   |
|                                      | Dexterity content types can behave    |                                       |                                       |
|                                      | like a collective.task_ task. E.g.    |                                       |                                       |
|                                      | "project", "client", "iteration".     |                                       |                                       |
|                                      | "Task" content                        |                                       |                                       |
|                                      | type included with                    |                                       |                                       |
|                                      | `collective.project`_ cannot be used  |                                       |                                       |
|                                      | with collective.task_                 |                                       |                                       |
|                                      | due to conflicting                    |                                       |                                       |
|                                      | "task" types.                         |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       | It exists.                            | Supports "placeful" tasking.          |
|                                      |                                       |                                       |                                       |
| collective.task_                     | Supports "placeful" tasking. A task is+---------------------------------------+---------------------------------------+
|                                      | a folder that can contain other       | Allows assignment of task to group,   | No date widget.                       |
|                                      | (presumably dependent) tasks.         | user and "enquirer".                  |                                       |
|                                      |                                       +---------------------------------------+---------------------------------------+
|                                      |                                       | Includes "task" behavior which can    | Possibly no support for assignment of |
|                                      |                                       | be used by other Dexterity content.   | `more than one principal`_.           |
|                                      |                                       +---------------------------------------+---------------------------------------+
|                                      |                                       | Can be used as a task framework       |                                       |
|                                      |                                       | by other add-ons.                     |                                       |
|                                      |                                       +---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       +---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+

.. _`Products.Poi`: https://github.com/collective/Products.Poi
.. _`collective.project`: https://github.com/collective/collective.project
.. _`collective.task`: https://github.com/collective/collective.task
.. _`more than one principal`: https://github.com/upiq/uu.task/issues/3

Developers
----------

Development environment with Nix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below instructions were only tested on Linux.

1. Install Nix_::

        % curl https://nixos.org/nix/install > bash

#. Clone ``uu.task``::

        % git clone https://github.com/upiq/uu.task

#. Enter environment::

        % cd uu.task
        uu.task/ % nix-shell

.. _Nix: https://nixos.org/nix

How to use ITaskAccessor
~~~~~~~~~~~~~~~~~~~~~~~~

::

    > from uu.task.interfaces import ITaskAccessor
    > task = ITaskAccessor(context)

    > print context.due  # raw value
    { ... }

    > print task.due     # computed value
    <datetime ...>

Testing
~~~~~~~

Developers please run ``make test`` before committing changes.

::

    $ make test
    check-manifest
    lists of files in version control and sdist match
    pyroma .
    ------------------------------
    Checking .
    Found uu.task
    ------------------------------
    Final rating: 10/10
    Your cheese is so fresh most people think it's a cream: Mascarpone
    ------------------------------
    flake8 uu/task/*.py
    flake8 uu/task/
    bin/test -s uu.task -v
    Running tests at level 1
    Running uu.task.testing.UUTaskFixture:Integration tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.426 seconds.
      Set up plone.app.testing.layers.PloneFixture in 11.991 seconds.
      Set up uu.task.testing.UUTaskFixture in 1.465 seconds.
      Set up uu.task.testing.UUTaskFixture:Integration in 0.000 seconds.
      Running:
                                                                                      
      Ran 2 tests with 0 failures and 0 errors in 0.028 seconds.
    Tearing down left over layers:
      Tear down uu.task.testing.UUTaskFixture:Integration in 0.000 seconds.
      Tear down uu.task.testing.UUTaskFixture in 0.003 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.083 seconds.
      Tear down plone.testing.z2.Startup in 0.005 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.002 seconds.
    viewdoc

Contributors
------------

* `Sean Upton <https://github.com/seanupton>` (UPIQ, University of Utah Health Sciences)
* `Alex Clark <http://aclark.net/>` (ACLARK.NET, LLC)
* `Rok Garbas <https://github.com/garbas>` (ACLARK.NET, LLC)

Copyright
---------

All content within this repository, unless otherwise noted elsewhere, is
Copyright 2015, University of Utah.  

Original works in this package are licensed under the GNU General Public
License v. 2.0. All original images, documentation, style-sheets, and 
JavaScript assets are additionally licensed under an MIT-style license.

See ``doc/COPYING.txt``
