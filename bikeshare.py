import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,"july":7,
                "august":8,"september":9, "october":10, "november":11, "december":12}
days = {"sunday":1, "monday":2, "tuesday":3, "wednesday":4,
            "thursday":5, "friday":6, "saturday":7}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    m = ("january", "february", "march", "april","may","june","july","august","september", "october", "november", "december")
    d = ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday")
    while(True):
        try:
            city = input("\n Which cities bikeshare data do you want to analyze (Chicago, New York City, or Washington):")
            if city.lower() in ("chicago", "new york city", "washington"):
                print("\n Looks like you want to hear about {}, if this is not true end the program now.".format(city))
                break
            else:
                print("\n I'm sorry it looks like you input a city to which we do not have data for.\n")
                raise Exception("Invalid Input for city")
        except:
            continue
    # TO DO: get user input for month (all, january, february, ... , june)
    while(True):
        try:
            filter = input("\n Would you like to filter by Month (M), Weekday (w), Both (B) or none (N):")
            if filter.lower() == "m" or filter.lower() == "month":
                month = input("\n Which month of the year are you interested in:")
                day = 'all'
                if month.lower() in m:
                    break
                else:
                    print("\n I'm sorry it looks like you didn't input a month, please try again.\n")
                    raise Exception("Invalid Input for month")
            elif filter.lower() == "w" or filter.lower() == "weekday":
                    month = 'all'
                    day = input("\n Which day of the week are you interested, input a day (sunday, monday, etc.):")
                    if day.lower() in d:
                        break
                    else:
                        print("\n I'm sorry it looks like you didn't input a day or all, please try again.\n")
                        raise Exception("invalid input for day")
            elif filter.lower() == "b" or filter.lower() == "both":
                    month = input("\n Which month of the year are you interested in:")
                    if month.lower() in m:
                        day = input("\n Which day of the week are you interested, input a day (sunday, monday, etc.):")
                        if day.lower() in d:
                            break
                        else:
                            print("\n I'm sorry it looks like you didn't input a valid weekday, please try again.\n")
                            raise Exception("Invalid input for day")
                    else:
                        print("\n I'm sorry it looks like you didn't input a valid month, please try again.\n")
                        raise Exception("Invalid Input for month")
            else:
                month = 'all'
                day = 'all'
                break
        except:
            continue
    print('-'*50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df["Start Time"], errors='coerce')
    if month.lower() != 'all':
        df = df[df['Start Time'].dt.month == months[month.lower()]]
    if day.lower() != 'all':
        df = df[df['Start Time'].dt.dayofweek == days[day.lower()]]
    if df.isnull().values.any():
        df = df.replace(np.nan, "unknown")
        df['Birth Year'].replace({'unknown':0}, inplace=True)
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (df) data frame - bike share data for a city during a window of time

    Returns:
        No returned data.
        Data is output directly to the user screen.
    """

    months = df['Start Time'].dt.month.to_numpy()
    days = df['Start Time'].dt.dayofweek.to_numpy()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('-'*50)
    start_time = time.time()
    if df.empty:
        print("Unfortunately there is no data to support your query, please try again.")
    else:
        # TO DO: display the most common month
        print("Calculating the most common month for bike share use.... \n")
        if (months[0] == months).all():
            print("The data frame provided only has data for a single month")
            print("Printing the month which data is available: {}".format(months[0]))
            print("-"*50)
        elif (days[0] == days).all():
            print("You filtered the data for a specific weekday.")
            mc = df.groupby(df['Start Time'].dt.month.rename('month')).agg({'count'})
            row = mc.loc[mc['Start Time'].idxmax()]
            print("The most frequent month for bike share use during weekday {}, is month: {}".format(days[0],row.index[0]))
            print("-"*50)
        else:
            mc = df.groupby(df['Start Time'].dt.month.rename('month')).agg({'count'})
            row = mc.loc[mc['Start Time'].idxmax()]
            print("The most frequent month for bike share use is: {}".format(row.index[0]))
            print("-"*50)
        # TO DO: display the most common day of week
        print("Calculating the most common weekday for bike share use..... \n")
        if (days[0] == days).all():
            print("The data frame provided is filtered by a specific weekday")
            print("Printing the weekday for which data is available: {}".format(days[0]))
            print("-"*50)
        elif (months[0] == months).all():
            print("The data frame provided is filtered for activities in only month: {}".format(months[0]))
            dc = df.groupby(df['Start Time'].dt.dayofweek.rename('dayofweek')).agg({'count'})
            row = dc.loc[dc['Start Time'].idxmax()]
            print("The most common day of the week for bike share during month {} is: {}".format(months[0], row.index[0]))
            print("-"*50)
        else:
            dc = df.groupby(df['Start Time'].dt.dayofweek.rename('dayofweek')).agg({'count'})
            row = dc.loc[dc['Start Time'].idxmax()]
            print("The most common day of the week for bikeshare use is: {}".format(row.index[0]))
            print("-"*50)
        # TO DO: display the most common start hour
        print("Calculating the most common hour for bike sharing...\n")
        if (days[0] ==days).all() and (months[0] == months).all():
            print("The data frame provided is filtered for the weekday {} and month {}".format(days[0], months[0]))
            dc = df.groupby(df['Start Time'].dt.hour.rename('starthour')).agg({'count'})
            row = dc.loc[dc['Start Time'].idxmax()]
            print("The most common start hour for weekday {} in month {} is:{}".format(days[0], months[0], row.index[0]))
            print('-'*50)
        elif (days[0] ==days).all() and not (months[0] == months).all():
            print("The data frame provided is filtered for the weekday {}".format(days[0]))
            dc = df.groupby(df['Start Time'].dt.hour.rename('starthour')).agg({'count'})
            row = dc.loc[dc['Start Time'].idxmax()]
            print("The most common start hour for weekday {} is: {}".format(days[0],row.index[0]))
            print('-'*50)
        elif not (days[0] ==days).all() and (months[0] == months).all():
            print("The data frame provided is filtered for month {}".format(months[0]))
            dc = df.groupby(df['Start Time'].dt.hour.rename('starthour')).agg({'count'})
            row = dc.loc[dc['Start Time'].idxmax()]
            print("The most common start hour in month {} is: {}".format(months[0], row.index[0]))
            print('-'*50)
        else:
            dc = df.groupby(df['Start Time'].dt.hour.rename('starthour')).agg({'count'})
            row = dc.loc[dc['Start Time'].idxmax()]
            print("The most common start hour is: {}".format(row.index[0]))
            print('-'*50)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        (df) data frame - bike share data for a city during a window of time

    Returns:
        No returned data.
        Data is output directly to the user screen. 
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if df.empty:
        print("Unfortunately there is no data to support your query, please try again.")
    else:
    # TO DO: display most commonly used start station
        dc = df.groupby(['Start Station']).count()
        row = dc.loc[dc['Start Time'].idxmax()]
        print("The most commonly used start station is {}, with a count of {}".format(row.name, row[0]))

    # TO DO: display most commonly used end station
        dc = df.groupby(['End Station']).count()
        row = dc.loc[dc['End Time'].idxmax()]
        print("The most commonly used end station is {}, with a count of {}".format(row.name, row[0]))

    # TO DO: display most frequent combination of start station and end station trip
        dc = df.groupby(['Start Station', 'End Station']).count()
        row = dc.loc[dc['Start Time'].idxmax()]
        print("The most common combination of start and stop stations is {}, with a count of {}".format(row.name, row[0]))
        print('-'*50)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if df.empty:
        print("Unfortunately there is no data to support your query, please try again.")
    else:
        # TO DO: display total travel time
        total = dt.timedelta(seconds = (df['Trip Duration'].sum()).item())
        print("What is the total time traveled by bike share users?")
        print("Total time traveled: {}".format(total))

        # TO DO: display mean travel time
        mean = dt.timedelta(seconds = (df['Trip Duration'].mean()).item())
        print("What is the mean time traveled by bike share users? ")
        print("Mean time traveled: {}".format(mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if df.empty:
        print("Unfortunately there is no data to support your query, please try again.")
    else:
        # TO DO: Display counts of user types
        try:
            dc = df.groupby(['User Type']).count()
            print("\nWhat is the count of the different types of users using bike shares?")
            for i in range(0, len(dc.index)):
                print("{}:{}".format(dc.index[i], dc.iloc[i,0]))
        except:
            print("There was no data for user types")

        # TO DO: Display counts of gender
        try:
            dc = df.groupby(['Gender']).count()
            print("\nWhat is the count of the different genders using bike shares? ")
            for i in range(0, len(dc.index)):
                print("{}:{}".format(dc.index[i], dc.iloc[i,0]))
        except:
            print("There was no data available for gender")

        # TO DO: Display earliest, most recent, and most common year of birth
        try:
            df1 = df.sort_values('Birth Year').groupby(['Birth Year']).count()
            df2 = df.sort_values('Birth Year', ascending=False)
            row = df1.loc[df1['End Time'].idxmax()]
            print('\nWhat is the earliest, most recent, and most common year of birth?')
            if df1.index[0] == 0:
                print("The most common answer was to provide no birth year.")
                print("Accounting for this and removing results that did not provide a response...\n")
                df1 = df1.loc[df1.index[1]:]
                row = df1.loc[df1['End Time'].idxmax()]
            print('Earliest birth year: {}'.format(round(df1.index[0])))
            print('Most recent birth year: {}'.format(round(df2.loc[df2.index[0], 'Birth Year'])))
            print('Most common birth year: {}'.format(round(row.name)))
        except:
            print("There was no data available for Birth Years")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data(df):
    """Displays user data in batches of 5"""
    while True:
        answer = input("Would you like to see individual trip data (yes or no):")
        if answer.lower() == 'no':
            break
        elif answer.lower() == 'yes':
            break
        else:
            print('please input a valid response')
    ind = 0
    counter = 0
    batch_size = 5
    while answer.lower() == 'yes':
        for i in range(ind, ind+batch_size):
            print(df.loc[df.index[i],:])
            print(" ")
            counter += 1
        ind += batch_size
        if (len(df.index) - ind) <= batch_size:
            batch_size = len(df.index) - ind
        if ind >= len(df.index) and counter == len(df.index):
            print("You have reached the end of the data")
            ind = 0
            batch_size = 5
        while True:
            ans = input("Would you like to continue viewing individual trip data (yes or no):")
            if ans.lower() == 'no':
                answer = 'no'
                break
            elif ans.lower() == 'yes':
                answer = 'yes'
                break
            else:
                print('please input a valid response')
        if answer.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip_data(df)
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes' and restart.lower() == 'no':
                break
            elif restart.lower() == 'yes' and restart.lower() != 'no':
                break
            else:
                print("Please input a valid input")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
