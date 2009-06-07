The session stats are output to a comma-separated file
"stats.txt" in this directory.

NOTE: To specify a different stats file than "stats.txt",
use the command-line option: --statsfile
Example:
   brainworkshop.exe --statsfile fred.txt
   brainworkshop.exe --statsfile mary.txt

Each line holds the data for one session (about 60 seconds).
To be parsed properly by Brain Workshop, a particular format
must be maintained.

Example line:

2008-08-12 13:26:55,D2B,95,2,2,12,22,0,4,66,50,0,0,0,0,0,0

1. The date format is as shown: YYYY-MM-DD HH:MM:SS

2. The mode string can be any of the following:
	D#B - dual #-back
	T#B - triple #-back
	DL#B - dual letter #-back
	TL#B - triple letter #-back
	QL#B - quad letter #-back

3. The percentage score from 0-100.

4. The mode number:
	2 = D#B - dual #-back
	3 = T#B - triple #-back
	4 = DL#B - dual letter #-back
	5 = TL#B - triple letter #-back
	6 = QL#B - quad letter #-back

5. The n-back number. for example, 2 = 2-Back

6. Number of quarter-seconds per trial.
	 8 = 2 seconds
	12 = 3 seconds
	etc.

7. Number of trials in the session.

8. 0 = Standard mode, 1 = Training mode.

9. Session number, the number followed by # in game

10. The next seven numbers are percentage scores for
    each of the seven input categories.
    a. Position
    b. Audio
    c. Color
    d. Vis & N-Vis
    e. Vis & N-Audio
    f. Audio & N-Vis
    g. Arithmetic
	h. Image

Each column is delimited by the comma character: ,

If there's an error loading the stats file, please make
sure each line conforms to the above format.

