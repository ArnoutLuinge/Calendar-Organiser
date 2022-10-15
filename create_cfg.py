import yaml

keyword_list1 = ["Exam", "Lecture", "Project", "Practical", "Workshop"]
keyword_list2 = ["Exam", "Lecture", "Tutorial", "Self study supervised", "Practical"]

sort_keywords = []

def make_cfg():
    print("Welcome, to start please enter ical link:")
    ical_src = input()
    print("Using", ical_src, "as input.")
    print("For what keywords should seperate calendars be created? A misc calendar with all remaining events will always be created.")
    print("Enter the number of the preferred list, or enter 3 to input your own list of keywords")
    print("1: ", keyword_list1)
    print("2: ", keyword_list2)
    print("3: I will enter my own keywordlist")
    sort_choice = input()

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

    yaml_file = {
            'Calendar_URL' : ical_src, 
            'keywords' : sort_keywords
                }

    with open(r'config.yml', 'w') as file:
        yaml.dump(yaml_file, file)
