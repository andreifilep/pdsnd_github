import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        input_city = input("Enter city name! Select from Chicago, New York, Washington: ")
        # check if input coresponds to desired cities. Accept both possible answers for New York
        if input_city.lower() not in ('chicago', 'new york', 'new york city', 'washington'):
            print("You have chosen a wrong city or misspelled. Please choose from Chicago, New York, Washington!")
            continue
        else:
            # check if user happy with selection
            user_city = input("You have selected {}! Confirm? [Y / N]  ".format(input_city.upper()))

        # input validation
        if user_city.lower() in ('y', 'yes'):  # if user is happy with selection
            if input_city.lower() == "new york city" or input_city.lower() == "new york":  # change input new york city to new york
                city = "new_york_city"  # set city to new york
            else:
                city = input_city.lower()  # set city to chosen city
            break
        else:
            # go back to beginning of function and start over with input
            print("Restart!")
            continue
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        input_month = input("Select month! Available options - all, january, february, march, april, may, june: ")
        # check if input coresponds to given list
        if input_month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("You have not chosen a listed month! Select: all, january, february, march, april, may, june")
            continue
        else:
            # check if user happy with selection
            user_month = input("You have selected {}! Confirm? [Y / N] ".format(input_month.upper()))

        # input validation
        if user_month.lower() in ('y', 'yes'):  # if user is happy with selection
            month = input_month.lower()  # set month to chosen month
            break
        else:
            # go back to beginning of function and start over with input
            print("Restart!")
            continue
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        input_day = input("Select day! Available options -  all, weekdays: ")
        # check if input coresponds to given list
        if input_day.lower() not in (
        'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("Check spelling!")
            continue
        else:
            # check if user happy with selection
            user_day = input("You have selected {}! Confirm? [Y / N]  ".format(input_day.upper()))

        # input validation
        if user_day.lower() in ('y', 'yes'):  # if user is happy with selection
            day = input_day.lower()  # set day to chosen day
            break
        else:
            # go back to beginning of function and start over with input
            print("Restart!")
            continue
            break

    print('-' * 40)
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
    filename = "./" + city + ".csv"  # generate filename string
    raw_data = pd.read_csv(filename,
                           parse_dates=["Start Time", "End Time"])  # read file and convert times to correct format

    # extend data frame by hour, month and day name
    raw_data['start_hour'] = raw_data["Start Time"].dt.hour  # Start_Time hour
    # raw_data['weekday'] = raw_data["Start Time"].dt.dayofweek # day of week
    raw_data['weekday_name'] = pd.DatetimeIndex(raw_data['Start Time']).day_name()  # Start Time name of weekday
    raw_data['month_name'] = pd.DatetimeIndex(raw_data['Start Time']).month_name()  # Start Time name of month

    # set filter for month according to input
    if month == "all":
        df = raw_data
    else:
        df = raw_data.loc[raw_data['month_name'] == month.capitalize()]

    # set filter for day according to input
    if day != "all":
        df = df.loc[df['weekday_name'] == day.capitalize()]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    # convert city to capitalized city name
    city_name = city.replace("_", " ").title()

    print('\nCalculating The Most Frequent Times of Travel for {}.\n'.format(city_name))
    start_time = time.time()
    # check if all month or days selected for first 2 values
    # display the most common month
    if month == "all":
        if df['month_name'].isnull().values.any() == False:
            popular_month = df['month_name'].mode()[0]
            print("Most popular month is: ", popular_month.upper())
        else:
            rows_dropped = df['month_name'].isnull().values.any().sum()
            print("Month data contained errors.\n Droped {} lines".format(rows_dropped))
            df_month = df.dropna(subset=['month_name'])
            popular_month = df_month['month_name'].mode()[0]
            print("Most popular month is: ", popular_month.upper())

    # display the most common day of week
    if day == "all":
        if df['weekday_name'].isnull().values.any() == False:
            popular_day = df['weekday_name'].mode()[0]
            print("Most popular day is:   ", popular_day.upper())
        else:
            rows_dropped = df['weekday_name'].isnull().values.any().sum()
            print("Day data contained errors.\n Droped {} lines".format(rows_dropped))
            df_day = df.dropna(subset=['weekday_name'])
            popular_day = df_day['weekday_name'].mode()[0]
            print("Most popular day is:   ", popular_day.upper())

    # display the most common start hour
    if df['start_hour'].isnull().values.any() == False:
        popular_hour = df['start_hour'].mode()[0]
        print("Most popular hour is:  ", popular_hour)
    else:
        rows_dropped = df['start_hour'].isnull().values.any().sum()
        print("Day data contained errors.\n Droped {} lines".format(rows_dropped))
        df.dropna(subset=['start_hour'])
        popular_hour = df['start_hour'].mode()[0]
        print("Most popular hour is:  ", popular_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    # convert city to capitalized city name
    city_name = city.replace("_", " ").title()

    print('\nCalculating The Most Popular Stations and Trip in {}\n'.format(city_name))
    start_time = time.time()

    # display most commonly used start station
    if df['Start Station'].isnull().values.any() == False:
        popular_start = df['Start Station'].mode()[0]
        print("Most commonly used start station is: ", popular_start)
    else:
        rows_dropped = df['Start Station'].isnull().values.any().sum()
        print("Day data contained errors.\n Droped {} lines".format(rows_dropped))
        df.dropna(subset=['Start Station'])
        popular_start = df['Start Station'].mode()[0]
        print("Most commonly used start station is: ", popular_start)

    # display most commonly used end station
    if df['End Station'].isnull().values.any() == False:
        popular_end = df['End Station'].mode()[0]
        print("Most commonly used end station is:   ", popular_end)
    else:
        rows_dropped = df['End Station'].isnull().values.any().sum()
        print("Day data contained errors.\n Droped {} lines".format(rows_dropped))
        df.dropna(subset=['End Station'])
        popular_end = df['End Station'].mode()[0]
        print("Most commonly used end station is:   ", popular_end)

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most popular trip is from {} to {}. ".format(popular_combination[0], popular_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    # convert city to capitalized city name
    city_name = city.replace("_", " ").title()

    print('\nCalculating Trip Duration in {}.\n'.format(city_name))
    start_time = time.time()

    # display total travel time
    sum_travel_time = df['Trip Duration'].sum()
    days = int(sum_travel_time // (24 * 3600))  # get number of days
    leftover_days = sum_travel_time % (24 * 3600)  # seconds left over days
    hours = int(leftover_days // 3600)  # number of hours
    leftover_hours = leftover_days % 3600  # leftover_hours
    minutes = int(leftover_hours // 60)  # number of minutes
    seconds = int(leftover_hours % 60)  # number of seconds

    print("Total travel time is {} seconds.".format(sum_travel_time))
    print("Total travel time is: {} Days - {} Hours - {} Minutes - {} Seconds".format(days, hours, minutes, seconds))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print("Mean rental duration is {} seconds.".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    # convert city to capitalized city name
    city_name = city.replace("_", " ").title()

    print('\nCalculating User Stats in {}.\n'.format(city_name))
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("There have been {} subscribers and {} ocasional customers".format(user_types['Subscriber'], user_types['Customer']))

    # Display counts of gender and respective proportion
    if 'Gender' in df.columns:  # check if Gender column exists
        user_gender = df['Gender'].value_counts()
        print("There have been {} male and {} female customers".format(user_gender['Male'], user_gender['Female']))
        male_percent = round((user_gender[0]/df['Gender'].count())*100, 2)
        female_percent = round(100 - male_percent, 2)
        print("Percentage of male customer is {} %".format(male_percent))
        print("Percentage of female customer is {} %".format(female_percent))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        youngest = int(df['Birth Year'].max())
        youngest_idx = df['Birth Year'].idxmax()
        rent_year_youngest = df.at[df.index[youngest_idx], 'Start Time'].year
        rent_age_youngest = rent_year_youngest - youngest
        oldest = int(df['Birth Year'].min())
        oldest_idx = df['Birth Year'].idxmin()
        rent_year_oldest = df.at[df.index[oldest_idx], 'Start Time'].year
        rent_age_oldest = rent_year_oldest - oldest
        common = int(df['Birth Year'].mode()[0])

        print("Youngest customer was born in {}. He was {} year old.".format( youngest, rent_age_youngest))
        print("Oldest customer was born in {}. He was {} year old.".format(oldest, rent_age_oldest))
        print("Most common year of birth is:  ", common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """
    Ask user if he would like to see 5 rows of raw data.
    If yes - show first 5 rows than prompt for next 5 rows.
    Loop question until user inputs no.

    Args:
        df - data frame to be shown
            """

    input_view = input("Would you like to view 5 rows of individual trip data? Enter [Y / N] ")

    if input_view.lower() not in ('n', 'no'):  # ask user if wants to see data
        start_loc = 0  # define start line
        while (input_view.lower() not in ('n', 'no')):  # loop until user input n or no
            print(df.iloc[start_loc:(start_loc + 5)])  # print 5 rows of data
            start_loc += 5  # increment start row
            input_view = input("Do you wish to continue? Enter [Y / N] ").lower()  # ask user if wish to continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df, city, month, day)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
