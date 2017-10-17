The session stats are output to a comma-separated file "stats.txt" (for the 
default user) or "USERNAME-stats.txt" (for other users) in this directory.  
Detailed per-trial stats, including reaction times, can be found in the 
"USERNAME-sessions.dat" in python's pickle data format.

The rest of this file documents the format of the "stats.txt" files.

NOTE: To specify a different stats file than "stats.txt", either create a new 
user profile, or use the command-line option: --statsfile
Example:
   brainworkshop.exe --statsfile fred.txt
   brainworkshop.exe --statsfile mary.txt

Each line holds the data for one session (about 60 seconds).  To be parsed 
properly by Brain Workshop, a particular format must be maintained.

Example line:

2010-08-17 02:45:38,2xD3B,61,258,3,35,24,0,1,33,75,0,0,0,0,0,0,0,75,0,0,0,0,0,0

0. The date format is as shown: YYYY-MM-DD HH:MM:SS

1. The mode string can be any of the following:
	D#B - dual #-back
	T#B - triple #-back
	A#B - arithmetic #-back
	DC#B - dual combination #-back
	TC#B - triple combination #-back
	QC#B - quad combination #-back
	2x???#B - double-stim ??? #-back
	C???# - crab ??? #-back


2. The percentage score from 0-100.

3. The mode number.  For a more complete listing, see config.ini.
    Some possibilities:
	2 = D#B - dual #-back
	3 = T#B - triple #-back
	4 = DC#B - dual combination #-back
	5 = TC#B - triple combination #-back
	6 = QC#B - quad combination #-back
	? + 128 = C???#B = crab ??? #-back
	? + 256 = 2x???#B = double-stim ??? #-back
	? + 512 = 3x???#B = triple-stim ??? #-back
	? + 768 = 4x???#B = quadruple-stim ??? #-back
    For example, 386 = 2 + 128 + 256 = Double-stim crab dual n-back.

4. The n-back number. for example, 3 = 3-Back

5. Number of 0.1 seconds per trial.
	15 = 1.5 seconds
	30 = 3 seconds
	etc.

6. Number of trials in the session.

7. 0 = Standard mode, 1 = Manual mode.

8. Session number, the number followed by # in game

9-24. The next sixteen numbers are percentage scores for
    each of the input categories.
	9. Position1
	10. Audio
	11. Color
	12. Vis & N-Vis
	13. Audio & N-Vis
	14. Arithmetic
	15. Image
	16. Vis & N-Audio
	17. Audio2
	18. Position2 
	19. Position3
	20. Position4
	21. Color1 or Image1 (multi-stim mode only)
	22. Color2 or Image2
	23. Color3 or Image3
	24. Color4 or Image4

Each column is delimited by the comma character: ,

If there's an error loading the stats file, please make
sure each line conforms to the above format.

