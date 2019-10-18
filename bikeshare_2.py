import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington dc': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply 
        no month filter
        (str) day - name of the day of week to filter by, or "all" to 
        apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = str(input('Enter a city (Chicago, New York City, or Washington DC): ').lower())

    while city not in ['chicago', 'new york city', 'washington dc']:
        print('-'*40)
        print('\n\nYou did not enter a valid city.')
        city = str(input('Enter a city (Chicago, New York City, or Washington DC): ').lower())


    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = str(input('Enter a month (January - June). Enter \"All\" for all months: ').lower())

    while month not in months:
        print('-'*40)
        print('\n\nYou did not enter a valid month.')
        month = str(input(
        'Enter a month (January - June). Enter \"All\" for all months: ').lower())

    if month != 'all':
            month = months.index(month) + 1


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    day = str(input(
    'Enter a day of the week (Sunday - Saturday). Enter \"All\" for all months: ').lower())

    while day not in days:
        print('-'*40)
        print('\n\nYou did not enter a valid day of the week.')
        day = str(input(
        'Enter a day of the week (Sunday - Saturday). Enter \"All\" for all months: ').lower())

   
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if 
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
        no month filter
        (str) day - name of the day of week to filter by, or "all" to
        apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month
        and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    print('\nFor the time period of January - June 2017...')

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Common Month:', popular_month)


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Common Day of Week:', popular_day)


    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    
    print('Most Frequent Start Hour: {}:00'.format(popular_hour))    
    
    
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    print('Most Common Start Station: \'{}\''.format(popular_start))


    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    print('Most Common End Station: \'{}\''.format(popular_end))


    # display most frequent combination of start station and end station trip
    df['trip'] = '\'' + df['Start Station'] + '\' to \'' + df['End Station'] + '\''
    popular_trip = df['trip'].mode()[0]
    
    print('Most Common Trip:', popular_trip)


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trav = df['Trip Duration'].sum()
    total_trav_hrs = (total_trav / 60) / 60

    print('Total Travel Time: {} hours'.format(round(total_trav_hrs, 2)))


    # display mean travel time
    avg_trav = df['Trip Duration'].mean()
    avg_trav_min = avg_trav / 60

    print('Average Travel Time: {} minutes'.format(round(avg_trav_min, 2)))
    

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print('\nCounts of User Types:\n\n', user_types.to_string())


    # Display counts of gender
    # Solution adopted from Ronak M's suggestion for question #55524
    # link: https://knowledge.udacity.com/questions/55524
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print('\n\nCounts of User Gender:\n\n', user_gender.to_string())
    else:
        print('\n\nUser Gender data not available for this city')


    # Display earliest, most recent, and most common year of birth
    # Solution adopted from Ronak M's suggestion for question #55524
    # link: https://knowledge.udacity.com/questions/55524
    if 'Birth Year' in df.columns:
        min_by = df['Birth Year'].min()
        print('\n\nEarliest Birth Year:', int(min_by))
        max_by = df['Birth Year'].max()
        print('Most Recent Birth Year:', int(max_by))
        popular_by = df['Birth Year'].mode()[0]
        print('Most Common Birth Year:', int(popular_by))
    else:
        print('\n\nUser Birth Year data not available for this city')


    print('\n\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def data_disp(df):
    """
    Asks user if they would like to see the data used for their analysis.

    Returns:
        Number of rows in the DataFrame and what rows are displayed at a given time.
        DataFrame used for the anaysis, displayed 5 rows at a time.
    """ 
    interval = 5
    start_line = 0
    df_size = df.shape[0]

    disp_df = input(
    '\nThis query resulted in {} rows of data. Would you like to see the data? Enter yes or no: '
    .format(df_size)).lower()

    while disp_df not in ['no', 'yes']:
        print('-'*40)
        print('\n\nYou did not enter a valid response.')
        disp_df = input(
        'This query resulted in {} rows of data. Would you like to see the data? Enter yes or no: '
        .format(df_size)).lower()

    while disp_df == 'yes':
        print(df.iloc[start_line:start_line + interval])
        line_num1 = start_line + 1
        line_num2 = (line_num1 + interval) - 1
        print('\n\nDisplaying rows {} through {} of {}.'.format(line_num1, line_num2, df_size))
        start_line += interval
        disp_df = input('Would you like to continue?: ').lower()
        if disp_df == 'no':
            break
        while disp_df not in ['no', 'yes']:
            print('-'*40)
            print('\n\nYou did not enter a valid response.')
            disp_df = input('Would you like to continue?: ').lower()
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_disp(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
