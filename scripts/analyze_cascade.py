##################################################################################################analyze the social cascades###################################################################################################################
import os
cascade_dir = "/home/twitterBollen/xshuai/science_social_media/twitter/dat/nature.com/doi_tweets/" 


index_seq = range(1, 361)
for i in index_seq:
    cascade = {}
    infile = open(os.path.join(cascade_dir, 'social_cascade', str(i) + '.cas'), 'r')
    for line in infile:
	content = line.split()
	time = content[0]
	users = content[1]
	size = len(users.split(','))
	try:
	   # print users
	    cascade[size].add(users)
	except KeyError:
#	    print users
	    cascade[size] = set([users])

    cascade_size = sorted(cascade.keys(), reverse=True)
    write_lines = []
    for size in cascade_size:
	cascade_list = list(cascade[size])
	for cas in cascade_list:
	    newline = cas + '\n'
	    write_lines.append(newline)
    outfile = open(os.path.join(cascade_dir, "cascade_size", str(i) + '.size'), 'w')
    outfile.writelines(write_lines)
    outfile.close()
    


