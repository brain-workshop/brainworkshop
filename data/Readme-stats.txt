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

0. The date format is as shown: YYYY-MM-DD HH:MM:SS

1. The mode string can be any of the following:
	D#B - dual #-back
	T#B - triple #-back
	DL#B - dual letter #-back
	TL#B - triple letter #-back
	QL#B - quad letter #-back

2. The percentage score from 0-100.

3. The mode number:
	2 = D#B - dual #-back
	3 = T#B - triple #-back
	4 = DL#B - dual letter #-back
	5 = TL#B - triple letter #-back
	6 = QL#B - quad letter #-back

4. The n-back number. for example, 2 = 2-Back

5. Number of 0.1 seconds per trial.
	15 = 1.5 seconds
	30 = 3 seconds
	etc.

6. Number of trials in the session.

7. 0 = Standard mode, 1 = Training mode.

8. Session number, the number followed by # in game

9-17. The next nine numbers are percentage scores for
    each of the seven input categories.
    9. Position
    10. Audio
    11. Color
    12. Vis & N-Vis
    13. Audio & N-Vis
    14. Arithmetic
    15. Image
    16. Vis & N-Audio
    17. Audio2

Each column is delimited by the comma character: ,

If there's an error loading the stats file, please make
sure each line conforms to the above format.

