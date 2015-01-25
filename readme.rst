Eidolon Savegame Editor
=======================

Early in my playing of Eidolon, I somehow missed my chance to find the
fishing pole, and continually had trouble finding enough food to survive
as a result.  This is the tool I wrote to avoid having to trek all
the way across the world to find that fishing pole.

Install
-------

From any environment where pip is available::

    pip install eidolon-savegame-editor

Or, from a clone of this repository::

    pip install -e .

Use
---

::

    eidolon_savegame_editor /path/to/savegame COMMAND

But where's my savegame?
------------------------

OSX: ``~/Library/Application Support/Steam/SteamApps/common/Eidolon/EIDOLON.app/Contents/Resources/Engine/Config/SaveData.bin``

Commands
--------

``reset_hunger``
~~~~~~~~~~~~~~~~

Resets your hunger to zero.

``show_properties``
~~~~~~~~~~~~~~~~~~~

Enumerates properties found in the savegame file.


Disclaimer
----------

This may destroy your savegame!  Make a backup if you don't trust this script.

