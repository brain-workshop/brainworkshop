Brain Workshop version 4.8 and later allows the user to add new sound 
sets, image sets, and music.  

To add a new sound set, create a subfolder under res/sounds/ with 
the name that you would like to see in the Brain Workshop sound 
selection screen.  You must have at least eight sound files in that
folder, or else Brain Workshop will (probably) crash.  If there are
more than eight files, Brain Workshop will take a random subset of
eight sound files when each session is begun using that sound set.
Sound files can be in wav, ogg, mp3, aac, mp2, ac3, or m4a format
if AVBin is present (which should be unless you're running Brain 
Workshop from the source code), but if AVBin is not present, only
wav files will be supported.  The filename for each sound file
(minus the file extension) will be used as the visual stimulus
for combination N-back modes.  All existing sound sets can be 
modified or (with the possible exception of 'letters') deleted.

To add new image sets, create a subfolder under res/sprites/ and add
at least eight image files to that folder.  The images should be 
square .png of any size (the program will scale them appropriately), 
but 256 pixels seems to be a good tradeoff between size and quality. 
The sprites are processed for the color n-back task by applying a 
colored filter, so the images should be mostly white clipart-style 
shapes with a transparent background. In order to reduce pixellation 
the edges of the shapes are slightly blended into the transparent 
background using the alpha channel.  Note that the 'colored-squares'
image set is treated specially by Brain Workshop, and is stored
in the 'misc' folder instead of the 'sprites' folder because of this.

To add new music, just drop an audio file into one of the subfolders of
res/music.  The music files can be in any format mentioned in the 
paragraph above on sound sets and can be of any length.

If you have a sound set, image set, or music file which you would like
to share and which is free of copyright restrictions, please submit it
to the authors and/or announce it on the brain-training@googlegroups.com
email list.  As long as it's a reasonable size, we'd be happy to host
it on the Brain Workshop Sourceforge website, and if we like it, we may
even want to include it in future releases of the program.
