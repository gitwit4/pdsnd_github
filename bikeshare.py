import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input("\nWhich city would you like to analyze? New York City, Chicago, or Washington?\n")
        if city.title() not in ('New York City', 'Chicago', 'Washington'):
            print("Sorry. Please enter a valid city.")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to analyze? Please enter a month between (January and June) or enter 'all'.\n")
        if month.title() not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
            print("Please enter a valid month or 'all'.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhat day of week are you looking for? Please enter the day of week or enter 'all'.\n")
        if day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All'):
            print("Please enter a valid day of week or 'all'.")
            continue
        else:
            break

    print('-'*40)
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
    # load file into dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day to new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if entered
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1
        # filter by month for new dataframe
        df = df[df['month'] == month]

    # filter by day if entered
    if day != 'all':
        # filter by day for new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("Most Popular Month:", popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most Popular Day:", popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most Popular Starting Hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("Most Common Start Station:", start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print("\nMost Common End Station:", end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combination_trip = df['Start Station'].astype(str) + " to " + df['End Station'].astype(str)
    most_frequent_trip = combination_trip.value_counts().idxmax()
    print("\nMost Frequent Trip is:", most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print("Total Travel Time:", round(Total_Travel_Time/86400, 2), "days.")

    # TO DO: display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print("Mean Travel Time:", round(Mean_Travel_Time/60, 2), "minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:\n", str(user_types))

    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("\nGender Types:\n", str(gender_types))
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print("\nEarliest Year:\n", int(earliest_year))
    except KeyError:
        print("\nEarliest Year:\nNo data available for this month.")

    try:
        most_recent_year = df['Birth Year'].max()
        print("\nMost Recent Year:\n", int(most_recent_year))
    except KeyError:
        print("\nMost Recent Year:\nNo data available for this month.")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print("\nMost Common Year:\n", int(most_common_year))
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks user to see lines of raw data from the current dataset.
       If yes, displays first 5 rows. Then asks user again to see the next 5 rows.
       Continues asking until they say no.
    """
    # row_block represents the interval of 5, row_start and row_end are used for the index
    row_block = 5
    row_start = 0
    row_end = row_block - 1

    print("\nWould you like to see some raw data from the selected dataset?")

    while True:
        answer = input("Yes or No?: ")
        if answer.lower() == "yes":
            # prints out the actual row numbers
            print("\nDisplaying rows {} to {}:".format(row_start + 1, row_end + 1))
            # displays dataframe rows using the index
            print("\n", df.iloc[row_start:row_end+1])
            # adds 5 to row_start and row_end for next block
            row_start += row_block
            row_end += row_block

            print("\nWould you like to see the next 5 rows?")
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
