Eidolon Savegame Editor
=======================

Early in my playing of Eidolon, I somehow missed my chance to find the
fishing pole and continually had trouble finding enough food to survive
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

+---------+----------------------------------------------------------------------------------------------------------------------------+
| OS      | Path                                                                                                                       |
+=========+============================================================================================================================+
| OSX     | ``~/Library/Application Support/Steam/SteamApps/common/Eidolon/EIDOLON.app/Contents/Resources/Engine/Config/SaveData.bin`` |
+---------+----------------------------------------------------------------------------------------------------------------------------+
| Windows | ``C:\UDK\EIDOLON\Binaries\Win32\SaveData.bin``                                                                             |
+---------+----------------------------------------------------------------------------------------------------------------------------+

Commands
--------

``reset_hunger``
~~~~~~~~~~~~~~~~

Resets your hunger to zero.

``add_items ITEM COUNT``
~~~~~~~~~~~~~~~~~~~~~~~~

Adds items to your inventory.

Options for ``ITEM`` include:

* ``Mushrooms``
* ``Tinder``

*or* any other item in your inventory; use the key ``_items`` in
``show_properties`` to see what's in your inventory currently.

Note: If the item name you enter is not something that exists in
Eidolon, it will be ignored by the game, but will stay in your
savegame file forever.

``show_properties``
~~~~~~~~~~~~~~~~~~~

Enumerates properties found in the savegame file.


Disclaimer
----------

This may destroy your savegame!  Make a backup if you don't trust this script.

