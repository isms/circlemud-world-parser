CircleMUD World Parser
======================

This repo contains code for parsing [CircleMUD](http://www.circlemud.org/) world files (and therefore, in many cases older [DikuMUD](https://en.wikipedia.org/wiki/DikuMUD)). The flat files are parsed into simple Python data structures. From there, they can be output to JSON (the default command line functionality).

What is a world file?
---------------------

MUDs are text-based games made up primarily of interconnected rooms, non-player characters, objects (like weapons, armor, food), and other players.

![](https://upload.wikimedia.org/wikipedia/en/2/27/JediMUD_screenshot.png)

All of the rooms, items, and everything else that made up the game were persisted in simple textfiles. The specification for these file formats is described in "[The CircleMUD Builder's Manual](http://www.circlemud.org/cdp/building/building.html)" by Jeremy Elson, the creator of CircleMUD.

Here are the different types of files in CircleMUD v3.1:

| File extension | Description                                                 |
|----------------|-------------------------------------------------------------|
| `wld`          | Rooms                                                       |
| `mob`          | Mobiles (also known as "mobs" or NPCs)                      |
| `obj`          | Objects                                                     |
| `shp`          | Shops                                                       |
| `zon`          | Zone files (what to load where, how often to refresh, etc.) |

The problem
-----------

CircleMUD world files are in a custom format that, in the original codebase, were parsed directly into memory by [db.c](https://github.com/Yuffster/CircleMUD/blob/master/src/db.c).

This is inconvenient if you want to inspect these entries or use them in other games. Because the values are not annotated and because many of the interesting features are compressed into [bitvectors](https://en.wikipedia.org/wiki/Bit_array), there are many lookups that need to be done to understand even the simplest item or room.

For example, here is a single entry for an item in `lib/world/obj/30.obj` within the stock [CircleMUD world files](https://github.com/Yuffster/CircleMUD/tree/master/lib/world):

```
#3005
key dull metal~
a key of dull metal~
A key made of a dull metal is lying on the ground here.~
~
18 cdq 16385
3005 0 0 0
1 0 0
```

In the past, others have parsed these files to [XML](http://inventwithpython.com/blog/2012/03/19/circlemud-data-in-xml-format-for-your-text-adventure-game/), but the XML had some validity issues, certain file types weren't converted, and the original source code wasn't published.

Here's the same item as above in our new JSON file:

```json
{
    "affects": [], 
    "aliases": [
      "key", 
      "dull", 
      "metal"
    ], 
    "cost": 0, 
    "effects": [
      {
        "note": "NORENT", 
        "value": 4
      }, 
      {
        "note": "NODONATE", 
        "value": 8
      }, 
      {
        "note": "NOSELL", 
        "value": 65536
      }
    ], 
    "extra_descs": [], 
    "id": 3005, 
    "long_desc": "A key made of a dull metal is lying on the ground here.", 
    "rent": 0, 
    "short_desc": "a key of dull metal", 
    "type": {
      "note": "KEY", 
      "value": 18
    }, 
    "values": [
      3005, 
      0, 
      0, 
      0
    ], 
    "wear": [
      {
        "note": "WEAR_TAKE", 
        "value": 1
      }, 
      {
        "note": "WEAR_HOLD", 
        "value": 16384
      }
    ], 
    "weight": 1
}
```

Usage
-----

Before using this, make sure the requirements are installed:

    pip install -r requirements.txt

Let's say we want to convert the objects in `lib/world/obj/30.obj` to JSON. Using this package, you can run

    python parse.py 30.obj > obj/30.json
    
or

    python parse.py --dest obj/30.json 30.obj
    
which are equivalent. The input file will be recognized as CircleMUD object file and parsed appropriately. The same will be true of any of the accepted file formats. Any parsing errors will be logged to `stderr` but will not cause the script to exit and will not be transferred via pipes or written to output files. For example:

```
$ python parse.py world/obj/0.obj > 0.obj.json
2015-08-23 01:22:37,159 - __main__ - ERROR - Error parsing:

	0
	bug~
	a bug~
	This object is BAD!  If you see it, there must be a bug in the game.  Please
	report it immediately using the BUG command.~
	~
	13 0 0
	0 0 0 0
	0 0 0
	
	Traceback (most recent call last):
	  File "circlemud-world-parser/utils.py", line 89, in parse_from_string
	    d = parse_function(text)
	  File "circlemud-world-parser/object.py", line 62, in parse_object
	    weight, cost, rent = [int(v) for v in fields[7].split()]
	ValueError: too many values to unpack
	
$ head 0.obj.json
[
  {
    "affects": [], 
    "aliases": [
      "wings"
    ], 
    ...
```

Tests can be run with `make test`, and all of the stock CircleMUD files in `world/` can be converted to JSON in the `output/` directory with `make all`.

If you want to check out the JSON for all of the stock CircleMUD world files, it's in the [`output` folder](https://github.com/isms/circlemud-world-parser/tree/master/output) of this repo.

Other notes
-----------

You may want to convert all of the files in the CircleMUD world folder (typically found at `lib/world/`).

A bash script, `convert_all.sh` is also included which will parse all recognized files to JSON in a folder called `output/` while maintaining the same folder structure. Given a folder like this:

    world
    ├── mob
    ├── obj
    ├── shp
    ├── wld
    └── zon

You can run the following command:

    ./convert_all.sh world/

And you will end up with this:

    output
    ├── mob
    ├── obj
    ├── shp
    ├── wld
    └── zon

The new folders will have JSON files instead of `.obj`, `.mob`, `.wld` and so forth.