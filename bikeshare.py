# ! python3
'''bikeshare.py - Gives an insight of data related to bike share systems for three major cities in the United States—Chicago, New York City, and Washington.'''
import os
import logging
import pandas as pd
import numpy as np

# ? Change logging mood to CRITICAL to disable all levels of logging
logging.disable(logging.INFO)
# ? To make the logging outputs in the terminal
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


# Debugging sentence with modes (info/Debug). Will be seen throughout the program.
logging.info('Start of the program')


def quit_program(input_value):
    '''Quitting the application if argument equates to one of the quitting_value key words.\n

        will quit if the argument equal to one of these keywords:
            ["close", "cancel", "q", "exit", "quit"]
    Args:\n
        (str) city -- name of the city to analyze
    '''

    logging.info('Start of the quit_program function\n\n')

    # Quitting key words
    quitting_value = ["close", "cancel", "q", "exit", "quit"]
    if str(input_value).lower() in quitting_value:
        exit()


def input_validation(data, message):
    """Validate an input given by the user with the data in a list or dictionary.\n

    Args:\n
        (data structures) data -- Take the data of the correct answer.
        (str) message -- a message given to the user to indicate an input space.
    Returns:\n
        (str) input -- String value specified by the user and has a match in the data given.
        OR
        (str) input -- (Value) of the (Key) specified by the user.
    """

    logging.info('Start of the input_validation function\n\n')

    while True:  # keep the user in the input loop unless quits.
        input_str = str(input(message+"\n"))
        # Allow for quitting interrupt.
        quit_program(input_str)
        # Change the user input to lower case
        input_str = input_str.lower()

        if isinstance(data, list):  # Checks if the data is a list.
            # list comprehension to make all elements in the list lower case.
            data = [x.lower() for x in data]

        if input_str in data:
            break
        else:
            print("There must be a typo in your input.\n")

    if isinstance(data, dict):  # Checks if the data is a dictionary.
        logging.debug("Returned value is: %s\n\n" % (data[input_str]))
        return data[input_str]
    else:
        logging.debug("Returned value is: %s\n\n" % (input_str.capitalize()))
        return input_str.capitalize()


def load_csv_file():
    """Asks user to specify a city to load its data.

    Returns:\n
        (df) - Pandas DataFrame containing city data filtered by month and day
    """
    logging.info('Start of the load_csv_file function\n\n')

    # Allows for entering eather the full name of the city or just its first letter.
    city_data = {'chicago': 'chicago.csv', 'c': 'chicago.csv',
                 'new york city': 'new_york_city.csv', 'nyc': 'new_york_city.csv',
                 'washington': 'washington.csv', 'w': 'washington.csv'}

    message = "Choose between: chicago, new york city, washington"
    # Ask the user to specify a city.
    city = input_validation(city_data, message)

    # Run the file useing by changing the directory if it doesn't run using pd.read_csv(city)
    try:

        logging.debug("currentDirectory: %s" % (os.getcwd()))

        df = pd.read_csv(city)

    except Exception as identifier:
        logging.debug("Exception occurred: %s" % (identifier))

        print('''Oops!\nThe file couldn't be located manually.\n
        Let me try to locate it for you...\n''')

        # Change the working directory to the file directory.
        # Assumes that the data files are in the same folder as the program file.
        os.chdir(os.path.dirname(__file__))

        logging.debug("currentDirectory: %s\n" % (os.getcwd()))

        df = pd.read_csv(city)

    logging.debug("Dataframe of %s:\n%s\n\n" %
                  (city, df.head()))

    # Fills all nan elements with Unknown.
    df = df.fillna("Unknown")

    return df, city


def filtered_df(df):
    ''' Take a DataFrame and returns a new DataFrame (from the original) after applying a filter.'''

    logging.info('Start of the filtered_df function\n\n')

    # Allows for entering eather the full name of the filter or just its first words letter.
    filter_by = {"no filter": "No Filter", "nf": "No Filter",
                 "month": "Month", "m": "Month",
                 "day of week": "Day of Week", "dow": "Day of Week",
                 "gender": "Gender", "g": "Gender",
                 "user type": "User Type", "ut": "User Type"}

    message = "Choose your filter: No Filter, Month, Day of Week, Gender, User Type.\nNote: you could type first letters like: NF, M, DOW, G, UT."

    if city == "washington.csv":  # Remove the gender filter option from washington city.
        del filter_by["gender"]
        del filter_by["g"]
        # New massage for washington
        message = "Choose your filter: No Filter, Month, Day of Week, User Type.\nNote: you could type first letters like: NF, M, DOW, UT."

    # Ask the user for its filter of choice.
    filter_str = input_validation(filter_by, message)

    logging.debug("User input is: %s" % filter_str)

    if filter_str == "Month":  # Do analsis base on specific month name

        # Convert column start time to datetime
        df["Start Time"] = pd.to_datetime(df["Start Time"])
        # Add a numbered month column to the DataFrame
        df[filter_str] = df["Start Time"].dt.month

        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))

        # Sort the months in ascending order.
        existing_months = sorted(df[filter_str].unique().tolist())
        month = input_validation(str(existing_months),
                                 "Choose a month from the list: %s\n(Only existing months can be chosen.)" % (existing_months))

        # Filter the new month column with the month chosen by user.
        df = df.loc[df[filter_str] == int(month)]
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))

        # Drop the created month column.
        df = df.drop(filter_str, axis=1)
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))
        return df

    elif filter_str == "Day of Week":  # Do analsis base on specific week day
        # Convert column start time to datetime
        df["Start Time"] = pd.to_datetime(df["Start Time"])
        # Add a week day column to the DataFrame
        df[filter_str] = df["Start Time"].dt.weekday

        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))
        # Sort weekdays in ascending order.
        week_days = sorted(df[filter_str].unique().tolist())
        # Asks the user for a day to filter.
        week_day = input_validation(
            str(week_days), "Choose a day from 0 to 6 :\nWith Monday=0, Sunday=6")
        # Filter the new Day of Week column with the day specified by the user
        df = df.loc[df[filter_str] == int(week_day)]
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))

        # Drop the created month column.
        df = df.drop(filter_str, axis=1)
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))
        return df

    elif filter_str == "Gender":  # Do analsis based on the gender given information.

        # Create a list of all the unique existing genders and pass it to the user to chose.
        genders = df[filter_str].unique().tolist()
        gender = input_validation(
            genders, "Choose a gender from the following list: %s" % (genders))

        # Fillter the DataFrame to the chosen filter
        df = df.loc[df[filter_str] == gender]
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))

        # Drop the gender column, to help reduce time.
        df = df.drop(filter_str, axis=1)
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))
        return df

    elif filter_str == "User Type":  # Do analsis based on user type

        # Create a list of all the unique existing user_type and pass it to the user to chose.
        user_types = df[filter_str].unique().tolist()
        user_type = input_validation(
            user_types, "Choose a user_type from the following list: %s" % (user_types))

        # Fillter the DataFrame to the chosen filter
        df = df.loc[df[filter_str] == user_type]
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))

        # Drop the user_type column, to help reduce time.
        df = df.drop(filter_str, axis=1)
        logging.debug("New Dataframe is:\n%s\n\n" % (df.head()))
        return df

    else:
        return df


def general_info(df):
    """Takes a DataFrame and return a general overview of the data.\n

       In function print:\n
       Most Popular Start Hour.\n
       Most Popular End Hour.\n
       Most Popular day for traveling.\n
       Most Popular month for traveling.
    """

    logging.info('Start of the some_info function\n\n')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract hour from the End Time column to create an hour column
    df['hour'] = df['End Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular End Hour:', popular_hour)

    # Convert column start time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # Add a week day column to the DataFrame
    df["Day"] = df["Start Time"].dt.weekday_name
    popular_day = df['Day'].mode()[0]
    print('Most Popular day for traveling:', popular_day)

    df["Month"] = df["Start Time"].dt.month_name()
    popular_month = df['Month'].mode()[0]
    print('Most Popular month for traveling:', popular_month)


def sample_table(table_name='', df=pd.DataFrame()):
    ''' Print 5 rows at a time and wait for user inputs. When the user asks for more results, print the next five lines.\n
    Args:\n
    (str) table_name: name of the table.
    (df) df: data frame to be shown in sample rows.
    Returns:
    No returns, but print a sample table of 5 minimum rows upon the user request.
    '''

    logging.info('Start of the sample_table function\n\n')

    # Sets an initial row number for the sample table
    row_num = 5
    # Create a dict of all posable answers to the question
    yes_no_dict = {"y": "yes", "yes": "yes", "no": "no", "n": "no"}
    # Ask the user for an input from a multiple choice (yes or no).
    table = input_validation(yes_no_dict,
                             "\nWould you like to see a sample of the city data %s table? Enter Yes or No." % (table_name))
    while table == "yes":  # it wouldn't leave till the user is satisfied by saying "No" more lol ;)
        print(df.head(row_num))
        # Increment the sample row number by 5.
        row_num += 5
        # Ask the user for an input from a multiple choice (yes or no).
        table = input_validation(
            yes_no_dict, "\nWould you like to show more rows of this sample? Enter Yes or No.")


def main(df):
    '''The main function takes the DataFrame, 
       filter it, and provied a general info about the data.'''

    logging.info('Start of the main function\n\n')

    # Create a filtered df from the original DataFrame
    new_df = filtered_df(df)
    # Provides some general info to the filtered DataFrame
    general_info(new_df)

    return new_df


if __name__ == '__main__':

    while True:
        # Alternative solution: couldn't use city as a global value
        df, city = load_csv_file()
        # Shows a sample table of the dataframe
        sample_table("", df)
        new_df = main(df)
        # Shows a sample table of the new dataframe
        sample_table('new', new_df)

        # Restart the program if the user input ("yes", or "y"), otherwise exit.
        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        logging.debug("User input: %s" % (restart))
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

    message = 'Rate your experience from 1 to 5:\n(1 being "So bad", and 5 being "The best")'
    rating = input_validation(str([1, 2, 3, 4, 5]), message)
    ratings = {"1": "SO BAD (-_-)", "2": "NOT SO GOOD :d",
               "3": "OK :/", "4": "AWESOME (^_-)", "5": "THE BEST! (^O^)"}
    print("\n\n\n\nThank you for your rating.\n We also find you %s\n\n\n\n" %
          (ratings[rating]))

logging.info('End of the program')
