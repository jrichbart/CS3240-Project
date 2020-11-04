from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from userAccount.models import userAccount

def index(request):
    # latest_account_list = userAccount.objects.all()

    template = loader.get_template('find/index.html')

    user_account = {
        "major": "CS"
    }

    user_courses = [
        {
            "mnemonic": "CS",
            "number": "2150"
        },
        {
            "mnemonic": "APMA",
            "number": "3080"
        },
        {
            "mnemonic": "STS",
            "number": "2500"
        },
        {
            "mnemonic": "MATH",
            "number": "3620"
        }
    ]

    user_courses = sorted(user_courses, key=lambda c: c['mnemonic'])

    # Filter to include all accounts with at least one course match
    filtered_buddy_list = [
        {
            "user": {
                "email": "michaelscott@dundermifflin.com"
            },
            "firstName": "Michael",
            "lastName": "Scott",
            "major": "CS",
            "bio": "Do I need to be liked? Absolutely not. I like to be liked. I enjoy being liked. I have to be liked. But it’s not like this compulsive need like my need to be praised.",
            "courses": [
                {
                    "mnemonic": "CS",
                    "number": "2150"
                },
                {
                    "mnemonic": "APMA",
                    "number": "3080"
                },
                {
                    "mnemonic": "STS",
                    "number": "2500"
                }
            ],
            "availability": "",
            "numBuddies": 3
        },
        {
            "user": {
                "email": "dwightkschrute@dundermifflin.com"
            },
            "firstName": "Dwight",
            "lastName": "Schrute",
            "major": "CS",
            "bio": "When my mother was pregnant with me, they did an ultrasound and found she was having twins. When they did another ultrasound a few weeks later, they discovered that I had adsorbed the other fetus. Do I regret this? No.",
            "courses": [
                {
                    "mnemonic": "CS",
                    "number": "2150"
                },
                {
                    "mnemonic": "APMA",
                    "number": "3080"
                }
            ],
            "availability": "",
            "numBuddies": 0
        },
        {
            "user": {
                "email": "kevin@dundermifflin.com"
            },
            "firstName": "Kevin",
            "lastName": "Malone",
            "major": "Math",
            "bio": "The only problem is whenever I try to make a taco, I get too excited and crush it.",
            "courses": [
                {
                    "mnemonic": "CPE",
                    "number": "2090"
                },
                {
                    "mnemonic": "MATH",
                    "number": "3620"
                },
                {
                    "mnemonic": "CS",
                    "number": "2150"
                },
                {
                    "mnemonic": "APMA",
                    "number": "3080"
                },
                {
                    "mnemonic": "STS",
                    "number": "2500"
                }
            ],
            "availability": "",
            "numBuddies": 6
        },
        {
            "user": {
                "email": "angelamartin@dundermifflin.com"
            },
            "firstName": "Angela",
            "lastName": "Martin",
            "major": "Math",
            "bio": "I am proud to announce that there is a new addition to the Martin family. She’s hypoallergenic. She doesn’t struggle when you try to dress her. She’s a third-generation show cat.",
            "courses": [
                {
                    "mnemonic": "CS",
                    "number": "1110"
                },
                {
                    "mnemonic": "MATH",
                    "number": "3620"
                },
                {
                    "mnemonic": "MSE",
                    "number": "1110"
                },
                {
                    "mnemonic": "APMA",
                    "number": "3080"
                },
                {
                    "mnemonic": "STS",
                    "number": "4200"
                }
            ],
            "availability": "",
            "numBuddies": 6
        },
        {
            "user": {
                "email": "pamhalpert@dundermifflin.com"
            },
            "firstName": "Pam",
            "lastName": "Halpert",
            "major": "CS",
            "bio": "I can tell Michael's mood by which comedy routine he chooses to do. The more infantile, the more upset he is. And he just skipped the Ace Ventura talking butt thing. He never skips it. This is bad.",
            "courses": [
                {
                    "mnemonic": "CS",
                    "number": "1110"
                },
                {
                    "mnemonic": "APMA",
                    "number": "3080"
                }
            ],
            "availability": "",
            "numBuddies": 1
        },
    ]

    for buddy in filtered_buddy_list:
        buddy['courses'] = sorted(buddy['courses'], key=lambda c: c['mnemonic'])

    context = {
        'filtered_buddy_list': filtered_buddy_list,
        'userAccount': user_account,
        'userCourses': user_courses
        }
    return HttpResponse(template.render(context, request))