# FFX_EBP_Model_Replacer
A simple command line tool to swap out models in the script (ebp) files of FFX/FFX-2.

Arguments are below:

-p --path: Path to ebp file or folder containing ebp files.
-s --search: Model number to search. Can be declared multiple times if wanting to search and replace multiple models.
-r --replace: Model number that is replacing. Can be declared multiple times. Number of times this argument is used must match the -s argument.
-b --batch: Indicates that -p is a directory.
-o --overwrite: Overwrite original file(s). Will create a new file if argument is not specified.
-d --delete: Delete file(s) if no matches are found. Useful for only keeping edited scripts.

The below example would replace all instances of Tidus' model in the game scripts with Yuna's as well as replace all instances of Auron in the game scripts with Young Auron, while overwriting the original files and deleting any files that do not return any matches:

Ebp_Model_Replace.exe -p "D:\SteamLibrary\steamapps\common\FINAL FANTASY FFX&FFX-2 HD Remaster\data\ffxmods\ffx_ps2\ffx\master\jppc\event\obj" -d -b -o -s 1 -r 2 -s 3 -r 45

When putting in the numbers of models from other folders, instead of using their Hex representation, type in their group folder and then their folder number. For example, Kinoc is 0x211B (folder #283 in the NPC Folder) in hex, which would be model number 8475. Instead of having to do that, you instead type 2283.

As an example, the below would swap any instances of Seymour with his child self:

Ebp_Model_Replace.exe -p "D:\SteamLibrary\steamapps\common\FINAL FANTASY FFX&FFX-2 HD Remaster\data\ffxmods\ffx_ps2\ffx\master\jppc\event\obj" -d -b -o -s 8 -r 2272
