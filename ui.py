import organizer
print("Enter ical link:")
ical_src = input()
print("Using", ical_src, "as input.")
print("How to sort events?")
print("1: Lecture, practical, misc")

sort_choice = input()

if sort_choice == 1:
    sort_keywords =  ["Exam", "Lecture", "Project", "Practical"]
    organizer.organise(ical_src, sort_keywords)