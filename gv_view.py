def display_greeting():
	print('\nHello, welcome to Grapevine, the wine recommendation system for your mom.')

def display_no_history_message(default_wines):
	print('\nYou are a new user! \n\nPlease enter a comma-separated list of the numbers associated with your favorite wines below.\n')
	for i in range(len(default_wines)):
		print(str(i+1)+'. \t'+
			default_wines[i][0]['name']+' '+
			default_wines[i][0]['vintage']+', '+
			default_wines[i][0]['country'])
	print('')