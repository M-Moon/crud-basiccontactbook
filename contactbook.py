import sys, getopt
import sqlite3
import traceback

# globals, since db connection will persist during execution and the program is rather small
dbconn = sqlite3.connect('contactbook.db')
cursor = dbconn.cursor()

# making sure db is properly configured with table
cursor.execute('''CREATE TABLE IF NOT EXISTS ContactBook (Id INTEGER PRIMARY KEY \
, Name TEXT, Phone TEXT, Email TEXT)''')


# Will be able to take commandline arguments for quick access, such as viewing a contact's details

def process_arguments(dbconn):
    print('-'*80)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvaedf', [])
    except getopt.GetoptError:
        print('Arguments input incorrectly')
        sys.exit(2)
    #print(opts, args)

    for opt, arg in opts:
        #print(opt)
        if opt == '-h': # help
            print('contactbook.py -v [View] -a [Add] -e [Edit] -d [Delete] -f [ViewAll] -h [Help]')
            sys.exit()
        elif opt == '-v': #view
            cursor.execute('SELECT * FROM ContactBook')
            column_names = list(map(lambda x: x[0], cursor.description))

            print()
            print('On which column would you like to search?')
            print('---' + ', '.join(map(str,column_names)) + '---')
            column_to_search = input()

            print()
            print('What value would you like to search for? Type it exactly')
            value_to_search = input()

            if value_to_search.isnumeric():
                cursor.execute(f'SELECT * FROM ContactBook WHERE {column_to_search} = {value_to_search}')
            else:
                cursor.execute(f'SELECT * FROM ContactBook WHERE {column_to_search} = "{value_to_search}"')

            print()
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        elif opt == '-f': # viewall
            cursor.execute('SELECT * FROM ContactBook')
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        elif opt == '-a': # add
            name = input('What\'s their name? ')
            number = input('What\'s their number? ')
            email = input('What\'s their email address? ')

            cursor.execute(f'INSERT INTO ContactBook (Name, Phone, Email) VALUES("{name}", "{number}", "{email}")')
        elif opt == '-e': # edit
            print('Type the ID of the contact you would like to edit')
            id_to_edit = input()

            try:
                cursor.execute('SELECT * FROM ContactBook WHERE Id = ' + id_to_edit)
                column_names = list(map(lambda x: x[0], cursor.description))[1:]
            except sqlite3.OperationalError as e:
                print('Error selecting from database!')
                print(e)
                sys.exit(2)

            print()
            print('That contact\'s details are as follows:')
            rows = cursor.fetchall()
            for row in rows:
                print(row)

            print()
            print('Which column would you like to edit?')
            print('---' + ', '.join(map(str,column_names)) + '---')
            column_to_edit = input()

            if not column_to_edit in column_names:
                print('Column name not found!')
                sys.exit(2)

            print()
            print('What would you like to change it to?')
            value_to_insert = input()

            try:
                cursor.execute(f'UPDATE ContactBook set {column_to_edit} = "{value_to_insert}" where Id = {id_to_edit}')
            except sqlite3.OperationalError as e:
                print('Failure during update!')
                print(e)
                sys.exit(2)

            print()
            print('Entry successfully updated!')
        elif opt == '-d': # delete
            print('Type the ID of the contact you would like to delete')
            id_to_delete = input()

            try:
                cursor.execute('SELECT count(*) FROM ContactBook WHERE Id = ' + id_to_delete)
                selection = cursor.fetchone()[0]
                if selection == 0:
                    print()
                    print('That ID/Record does not exist. Exiting.')
                    sys.exit(2)
                cursor.execute('DELETE FROM ContactBook WHERE Id = ' + id_to_delete)
            except sqlite3.OperationalError as e:
                print('Error deleting from database!')
                print(e)
                traceback.print_exc()
                sys.exit(2)

            print()
            print('ID successfully deleted!')




if __name__ == '__main__':
    process_arguments(dbconn)
    dbconn.commit()
    dbconn.close()
