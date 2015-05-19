uu.task: UPIQ Task Management Add-on for Plone
==============================================

This repository serves as a place for development of a task managment add-on.

Copyright
---------

All content within this repository, unless otherwise noted elsewhere, is
Copyright 2015, University of Utah.  

Original works in this package are licensed under the GNU General Public
License v. 2.0. All original images, documentation, style-sheets, and 
JavaScript assets are additionally licensed under an MIT-style license.

See ``doc/COPYING.txt``

Contributors
------------

* `Sean Upton <https://github.com/seanupton>` (UPIQ, University of Utah Health Sciences)
* `Alex Clark <http://aclark.net/>` (ACLARK.NET, LLC)

Comparison
----------

Compare existing add-ons.

+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
| **Add-ons**                          |  **Description**                      |  **Pros**                             |  **Cons**                             |
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       |                                       |                                       |
|                                      |                                       |                                       |                                       |
| collective.project_                  | Project management add-on whose       |                                       |                                       |
|                                      | Dexterity content types can behave    | N/A                                   | N/A                                   |
|                                      | like a collective.task_ task. E.g.    |                                       |                                       |
|                                      | "project", "client", "iteration".     |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      | The "task" content                    |                                       |                                       |
|                                      | type included with                    |                                       |                                       |
|                                      | `collective.project`_ cannot be used  |                                       |                                       |
|                                      | when collective.task_ has been        |                                       |                                       |
|                                      | installed first, due to conflicting   |                                       |                                       |
|                                      | "task" types.                         |                                       |                                       |
|                                      |                                       |                                       |                                       |
|                                      | Curiously, no obvious warning or error|                                       |                                       |
|                                      | occurs on                             |                                       |                                       |
|                                      | installation of collective.project_   |                                       |                                       |
|                                      |                                       |                                       |                                       |
+--------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+
|                                      |                                       | It exists!                            | Supports "placeful" tasking.          |
|                                      |                                       |                                       |                                       |
| collective.task_                     | Supports "placeful" tasking. A task is+---------------------------------------+---------------------------------------+
|                                      | a folder that can contain other       | Allows assignment of task to group,   | No date widget.                       |
|                                      | (presumably dependent) tasks.         | user and "enquirer".                  |                                       |
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

.. _`collective.project`: https://github.com/collective/collective.project
.. _`collective.task`: https://github.com/collective/collective.task
