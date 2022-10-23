import yaml
import re

#regex for checking a valid ical url
url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#list of keywords for organising the calendars
keyword_list1 = ["Exam", "Lecture", "Practical", "Workshop"]
keyword_list2 = ["Exam", "Lecture", "Tutorial", "Self study supervised", "Practical"]


def make_cfg():
    sort_keywords = []

    print("Welcome, to start please enter the source ical link:")

    ical_src = validate_url_input()
    print("Using", ical_src, "as input.")
    
    print("For what keywords should seperate calendars be created? A misc calendar with all remaining events will always be created.")
    print("Enter the number of the preferred list, or enter 3 to input your own list of keywords")
    print("1: ", keyword_list1)
    print("2: ", keyword_list2)
    print("3: I will enter my own keywordlist")

    sort_choice = validate_input_choice()

    if sort_choice == "1":
        sort_keywords = keyword_list1

    elif sort_choice == "2":
        sort_keywords = keyword_list2

    elif sort_choice == "3":
        print("Please enter your desired keywords here, seperated by ', ':")
        user_input = input().split(", ")
        for i in range(len(user_input)):
            sort_keywords.append(user_input[i])

    print("Creating the following calendars: ") 
    for i in range(len(sort_keywords)):
        print ("- " + sort_keywords[i] + "_cal.ics")
    print ("- Misc_cal.ics")

    yaml_file = {'Calendar_URL' : ical_src, 
                'keywords' : sort_keywords}

    with open(r'config.yml', 'w') as file:
        yaml.dump(yaml_file, file)

    return 1

def validate_input_choice():
    sort_choice = input()

    while sort_choice != "1" and sort_choice != "2" and sort_choice != "3":
        print("Invalid input, try again:")
        sort_choice = input()

    return sort_choice
    
def validate_url_input():
    url = input()

    while not re.match(url_regex, url) is not None:
        print("Invalid URL, try again")
        url = input()

    return url
