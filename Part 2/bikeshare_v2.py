import os
import datetime
import pandas as pd

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def openTerminal():
    '''
    adjust terminal size for easy reading
    '''
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    os.system('mode con: cols=165 lines=50')

def getCity():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    print('-' * 60)
    global city
    city = input('\nEnter a city to view it\'s statistics: Chicago, New York, or Washington\n\n')
    city = city.lower()
    while True:
    #select city_data
        if city == 'chicago':
            print('\nThe Windy City it is!')
            return 'chicago'
        elif city == 'new york':
            print('\nThe Big Apple it is!')
            return 'new york'
        elif city == 'washington':
            print('\nCapitol City it is!')
            return 'washington'
        else:
            #second chance
            print('\nInvalid input\n')
            city = input('Please enter Chicago, New York, or Washington\n\n')
            city = city.lower()
    return city

def getMonth():
    '''
    Gets user input to filter by month, i.e. none, january, february, etc
    '''
    print('\nWould you like to see a particular month?')
    month = input('\nEnter January, February, March, April, May, June, or None for no month filter\n\n')
    month = month.lower()
    global monthFilter
    monthFilter = month
    while True:
        if month == 'january':
            return '1'
        elif month == 'february':
            return '2'
        elif month == 'march':
            return '3'
        elif month == 'april':
            return '4'
        elif month == 'may':
            return '5'
        elif month == 'june':
            return '6'
        elif month == 'none':
            return 'noMonth'
        else:
            #second chance
            print('\nInvalid input')
            month = input('\nPlease enter the full name of a month from above or "none"\n\n')
            month = month.lower()
    return month

def getDay():
    '''
    Gets user input to filter the data by day of the week, i.e. none, monday, tuedays, etc
    '''

    print('\nWould you like to see a particular day of the week?\n')
    day = input('Enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or None for no day of the week filter\n\n')
    day = day.lower()
    global dayFilter
    dayFilter = day
    while True:
        if day == 'sunday':
            return 6
        elif day == 'monday':
            return 0
        elif day == 'tuesday':
            return 1
        elif day == 'wednesday':
            return 2
        elif day == 'thursday':
            return 3
        elif day == 'friday':
            return 4
        elif day == 'saturday':
            return 5
        elif day == 'none':
            return 'noDay'
        else:
            #second chance
            print('\nInvalid input\n')
            day = input('Please enter the full name of a day of the week or "none".\n\n')
            day = day.lower()
    return day

def loadData(city, month, day):
    '''
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    '''

    print('\n' + ('-' * 60))
    #load the data
    while True:
        if city == 'chicago':
            df = pd.read_csv('chicago.csv')
            print('\nLoading Chicago statistics...\n')
            break
        elif city == 'new york':
            df = pd.read_csv('new_york_city.csv')
            print('\nLoading New York statistics...\n')
            break
        elif city == 'washington':
            df = pd.read_csv('washington.csv')
            print('\nLoading Washington statistics...\n')
            break
        else:
            print('\nSomething is wrong in loadData().') 
            break
    #filter by month 
    while True:
        if month != 'noMonth':
            df = df[df['Start Time'].str.contains('2017-0*' + month)]
            print('\nFiltering data by month...\n')
            break
        else:
            print('\nNo month filter seleted...\n')
            break
    #filter weekday
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    while True:
        if day != 'noDay':
            print('\nFiltering data by weekday...\n')
            df = df[df['Start Time'].dt.weekday == day] 
            break
        else:
            print('\nNo weekday filter selected...\n')
            break     
    return (df)
        
def format_df(df):
    '''
    Formats columns flow for easier reading of the display data
    and separates the time columns for further analysis.
    '''
    #formats the filtered dataframe
    print('\nFormatting data, please wait...\n')
    print('\n' + ('-' * 60))
    df[['Start Time']] = df[['Start Time']].astype(str)
    df.rename(columns={'Start Time' : 'Start_Time'}, inplace = True)
    df['Start_Date'] = df.Start_Time.str.split(' ').str.get(0)
    df['Start_Time'] = df.Start_Time.str.split(' ').str.get(1) 
    df.rename(columns={'End Time' : 'End_Time'}, inplace = True)
    df['End_Date'] = df.End_Time.str.split(' ').str.get(0)
    df['End_Time'] = df.End_Time.str.split(' ').str.get(1)
    df.rename(columns={'Start_Time' : 'Start Time'}, inplace = True)
    df.rename(columns={'Start_Date' : 'Start Date'}, inplace = True)
    df.rename(columns={'End_Time' : 'End Time'}, inplace = True)
    df.rename(columns={'End_Date' : 'End Date'}, inplace = True)
    df.drop(['Unnamed: 0'], axis = 1, inplace = True)
    if 'Gender' in df.columns:
        df = df[['Start Date', 
                'Start Time', 
                'Start Station', 
                'Trip Duration', 
                'End Station', 
                'End Time', 
                'End Date',  
                'Birth Year', 
                'Gender',
                'User Type']]
    else:
        df = df[['Start Date', 
                'Start Time', 
                'Start Station', 
                'Trip Duration', 
                'End Station', 
                'End Time', 
                'End Date',  
                'User Type']]
    return df

def timeStats(df):
    """
    Displays statistics on the most frequent times of travel.
    Filters are taken into effect
    """
    # most popular month
    dfDate = df.loc[:, 'Start Date']
    SplitDates = [x for x in dfDate.str.split('-')]
    dfSplitDates = pd.DataFrame(SplitDates, columns=['year', 'month', 'day'])
    month = int(dfSplitDates.loc[:, 'month'].mode()) 
    if month == 1:
        month = 'January'
    elif month == 2:
        month = 'February'
    elif month == 3:
        month = 'March'
    elif month == 4:
        month = 'April'
    elif month == 5:
        month = 'May'
    else:
        month = 'June'
    # most popular day of the week
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['Day of Week'] = df['Start Date'].dt.weekday_name
    #day = df['Day of Week'].mode().astype(str)
    day = df['Day of Week'].mode()[0]
    # most popular starting hour
    dfTime = df.loc[:, 'Start Time']
    splitTimes = [x for x in dfTime.str.split(':')]
    dfSplitTimes = pd.DataFrame(splitTimes, columns=['hour', 'minute', 'second'])
    hour = dfSplitTimes.loc[:, 'hour'].mode()[0]
    if int(hour) < 12:
        hour = (hour + ' A.M.')
    else:
        hour = (str(int(hour) - 12) + ' P.M.')
    # output
    if monthFilter == 'none':
        print('\nThe most popular month to bike is ' + month + '.')
    else:
        print('\nYou\'ve selected a month filter, the mode does not apply.')
    if dayFilter == 'none':   
        print('\nThe most popular weekday to bike is ' + day + '.')
    else:
        print('\nYou\'ve selected a day filter, the mode does not apply.')
    print('\nThe most popular hour to bike is ' + hour + '.')
    print('\n' + ('-' * 60))

def stationStats(df): 
    """
    Displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...')
    print('\n' + ('-' * 60))
    
    # display most commonly used start station
    dfStartStation = df.loc[:, 'Start Station']
    popStartStation = dfStartStation.mode()[0]
    # display most commonly used end station
    dfEndStation = df.loc[:, 'End Station']
    popEndStation = dfEndStation.mode()[0]
    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    dfTrip = df.loc[:, 'Trip']
    Trip = dfTrip.mode()[0]
    print('\nThe most popular station to start from is ' + popStartStation + '.\n')
    print('The most popular station to end at is ' + popEndStation + '.\n')
    print('The most popular trip is ' + Trip + '.')
    #print('The most popular trip is ' + Trip + '.\n')
    print('\n' + ('-' * 60))

def tripDurationStats(df): 
    """
    Displays statistics on the total and average trip duration.
    """

    print('\nCalculating Trip Duration...')
    print('\n' + ('-' * 60))
    # display total travel time
    tripDuration = df['Trip Duration'].sum()
    tripWeeks, tripDuration = divmod(tripDuration, 604800)
    tripDays, tripDuration = divmod(tripDuration, 86400)
    tripHours, tripDuration = divmod(tripDuration, 3600)
    tripMinutes, tripDuration = divmod(tripDuration, 60)
    tripDuration = int(tripDuration)
    print('\nThe sum of all the selected trips has been ' + str(tripWeeks) + ' weeks, ' + str(tripDays) + ' days, ' + str(tripHours) + ' hours, ' + str(tripMinutes) + ' minutes, and ' + str(tripDuration) + ' seconds.')
    # display mean travel time
    tripMean = df['Trip Duration'].mean()
    tripWeeks, tripMean = divmod(tripMean, 604800)
    tripDays, tripMean = divmod(tripMean, 86400)
    tripHours, tripMean = divmod(tripMean, 3600)
    tripMinutes, tripMean = divmod(tripMean, 60)
    tripMean = int(tripMean)
    print('\nThe average duration of the selected trips is ' + str(tripWeeks) + ' weeks, ' + str(tripDays) + ' days, ' + str(tripHours) + ' hours, ' + str(tripMinutes) + ' minutes, and ' + str(tripMean) + ' seconds.')
    print('\n' + ('-' * 60))

def userStats(df):
    """
    Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...')
    print('\n' + ('-' * 60))
    userTypes = df['User Type'].value_counts()
    print('\nQuantity of user types in selected trips:\n')
    print(userTypes)
    if city != 'washington':
        # Display counts of gender
        print('\nGender counts in the selected trips:\n')
        genderCount = df['Gender'].value_counts()
        print(genderCount)
        print('\n' + ('-' * 60))
        # Display earliest, most recent, and most common year of birth
        youngestUser = int(df['Birth Year'].mode()) 
        #youngestUser = df['Birth Year'].max() 
        oldestUser = int(df['Birth Year'].min())
        mostCommonBirthYear = int(df['Birth Year'].mode()[0])
        print('\nThe youngest user was born in ' + str(youngestUser) + ', the oldest in ' + str(oldestUser) + ', and the most common birth year is ' + str(mostCommonBirthYear) + '.')
    else:
        print('\nWashington has no data for gender or birth year.')
    print('\n' + ('-' * 60))

def displayRawData(df):
    '''
    Displays raw data in table format at the user's request.
    '''
    df.drop(['Trip'], axis=1, inplace = True)
    start = 0
    rawData = input("\nWould you like to view a table of raw data? Type yes or no.\n\n").lower()
    while True:
        if rawData == 'no':
            break
        elif rawData == 'yes':
            rows = input('\nHow many lines of data would you like to see?\n\n')
            print(df[int(start) : int(rows)])
            rows = int(start) + int(rows)
            rawData = input("\nWould you like to see more raw data? Type yes or no.\n\n").lower()
            while rawData == 'yes':
                moreRows = input('\nHow many more lines of data would you like to see?\n')
                print(df[int(rows) : (int(rows) + int(moreRows))])
                rows = int(rows) + int(moreRows)
                rawData = input("\nWould you like to see more raw data? Type yes or no.\n\n").lower()
        else:
            print('\nInvalid input\n')
            rawData = input('\nPlease type yes or no.\n\n')
            rawData = rawData.lower()

def main():
    while True:
        openTerminal()
        city = getCity()
        month = getMonth()
        day = getDay()
        df = loadData(city, month, day)
        df = format_df(df)
        timeStats(df)
        input("\nPress Enter to view more data...")
        stationStats(df)
        input("\nPress Enter to view more data...")
        tripDurationStats(df)
        input("\nPress Enter to view more data...")
        userStats(df)
        displayRawData(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()