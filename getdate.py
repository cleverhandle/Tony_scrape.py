import csv

with open('C:\\Users\\12544\\Documents\\scrape dates.csv', 'r') as read_obj: # read csv file as a list of lists
    csv_reader = csv.reader(read_obj) # pass the file object to reader() to get the reader object
    list_of_rows = list(csv_reader) # Pass reader object to list() to get a list of lists

#makes sure every digit has two digits
for days in range(len(list_of_rows)):
    for i in range(2):
        if len(list_of_rows[days][i]) < 2:
            list_of_rows[days][i] = '0' + list_of_rows[days][i]

print(list_of_rows)

#make a list of all the urls
urllist = []
for days in range(len(list_of_rows)):
    newurl = 'https://www.austinchronicle.com/events/' + list_of_rows[days][2] + '-' + list_of_rows[days][0] + '-' + list_of_rows[days][1] + '/'
    urllist.append(newurl)

print(urllist)


