=======
Changes
=======

3.2 (2023-06-05)
================

- Add support for Python 3.11.

- Add support for Python 3.10.


3.1 (2021-10-19)
================

- Pin to ``setuptools < 52`` to work around and incompatibility with
  ``zc.buildout`` in that version.

- Add support for Python 3.9.

- Require "view management screens" permission for the following methods
  (#20224):

    + ``.orderedbtreefolder.OrderedBTreeFolder.manage_changeOrder``
    + ``.orderedbtreefolder.OrderedBTreeFolder.getBatchObjectListing``


3.0 (2020-03-16)
================

Backwards incompatible changes
++++++++++++++++++++++++++++++

- Drop support for Python 2.

Features
++++++++

- Add support for Python 3.8.


2.0.1 (2019-11-05)
==================

- When moving an element behind the end of the list this no longer reverses
  the whole list. (#18264)


2.0 (2019-02-20)
================

Backwards incompatible changes
++++++++++++++++++++++++++++++

- Drop support for Zope 2.

Features
++++++++

- Support Zope 4.

- Add support for Python 3.6 and 3.7.

Other changes
+++++++++++++

- Flake8. (#16318)


1.5 (2017-08-10)
================

- Remove dependency on ``Globals`` (Zope 4 forward compatibility).


1.4 (2016-10-24)
================

- Fix `moveObjectsByDelta()` to be usable with unicode ids.

- `getObjectPosition()` now raises a `LookupError` if object is not found.

- Move source code to new directory 'src'.

- Update `bootstrap.py`, so it accepts a pinned version of setuptools.

- Use `py.test` as the one and only testrunner.


1.3.0 (2011-03-15)
==================

- Updated package to use `Products.BTreeFolder2` >= 2.13.3, so most
  compatibility code added in version 1.2.1 could be removed, thus requiring
  at least `Products.BTreeFolder2` version 2.13.3.

- Removed not needed dependency on `Products.CMFCore`.


1.2.1 (2011-03-07)
==================

- Methods ``objectItems``, ``objectValues``, ``keys``, ``values`` and
  ``items`` returned values unordered when package was used together with
  `Products.BTreeFolder2` >= 2.13.


1.2.0 (2011-03-03)
==================

- Updated to run on Zope 2.12+, thus requiring at least this version.


1.1.0 (2009-04-01)
==================

- Initial packaging as an egg.

- Code cleanup.
