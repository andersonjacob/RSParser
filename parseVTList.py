import csv

fname = r'C:\Users\candi\Documents\MarchRSVT.csv'
outname = fname.replace('.csv','_reporting.csv')
with open(fname) as csv_file:
	with open(outname, 'w', newline='') as report_file:
		reader = csv.reader(csv_file)
		writer = csv.writer(report_file)
		writer.writerow(['companion1','email1','companion2','email2','companion3','email3','visitees'])
		comps = []
		visits = []
		for row in reader:
			blank_line = all([len(x) < 1 for x in row])
			new_comp = ((len(row[0]) > 0) and (len(visits) > 0))
			new_comp = blank_line or new_comp
			if new_comp:
				comps.extend(['']*(6-len(comps)))
				print(comps, visits)
				if len(visits) > 0:
					writer.writerow(comps + visits)
				comps = []
				visits = []
		
			if (len(row[0]) > 0) and (len(row[1]) > 0):
				comps.extend(row[0:2])
		
			if (len(comps) > 0) and (len(row[0]) == 0) and (len(row[1]) > 0):
				visits.append(row[1])

		if len(visits) > 0:
			comps.extend(['']*(6-len(comps)))
			print(comps, visits)
			writer.writerow(comps + visits)
			comps = []
			visits = []
