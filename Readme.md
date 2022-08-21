# Flight Club
#### Video Demo:  https://youtu.be/B1WGwaM6QEk
#### Description:
TDLR; A Heroku hosted website that lets users create an account to choose destinations, 
price ceilings, and specific travel preferences. Flight Club then uses these to 
search (via Tequila Kiwi API) for weekly flight deals that meet the user's criteria and send these to the user via email.

---

Full Description:

Flight Club is essentially a flight deal finder. Users create an account, save their travel preferences, desired destinations, and the highest amount they would consider a 'deal' (price ceiling) for a flight to that destination, and Flight CLub takes care of the rest.
An extensive list (1400+) of possible airports around the world is available via jQuery autocomplete for the user to type and select. This simultaneously provides a better experience for the user, while also controlling user input to ensure that the destination is a valid and recognizable airport. 
Users can dynamically add or delete destinations if they so choose (however there is minimum of 3 and maximum of 10 destinations). The user's current data is prepopulated into the form when editing their preferences/destinations/price ceilings for a better UX.

Flight Club utilizes the Tequila Kiwi flight search API (https://partners.kiwi.com/our-solutions/tequila/) for all flight deal finding operations. Most of the user's preferences are simply parameters used in the Kiwi API call. Flight Club is hosted on Heroku, using the Heroku Postgres to handle data storage and Heroku Scheduler to run the flight_search.py once a day. 
The flight searcher checks each user's email day preference (which day of the week they want to receive the deals), as well as email frequency preference (weekly, biweekly, or monthly) and then proceeds with flight searches for those that matched. The RoadGoat API (https://developer.roadgoat.com/) is used after a deal is found to attempt to obtain a picture of the destination. 
The destination image, flight deal details, and a formatted url link (for https://www.kiwi.com/en/) with all of the filters/search parameters pre-set are all sent to the user via email using Sendinblue (https://www.sendinblue.com/). 
Sendinblue emails are also used for all account related actions, such as account confirmation, password reset, email/password changes, and when a user submits a report to Flight Club. Flight Club did not cost any money to make or maintain as all of the external services used to help create Flight Club (Heroku, Tequila Kiwi API, Sendinblue Email, RoadGoat API, etc.) utilized free accounts

In addition to the services that help Flight Club function, credit must be given to Dr.Angela Yu and her outstanding Udemy course '100 Days of Python' (https://www.udemy.com/course/100-days-of-code/). This project was the culmination of all the skills I learned during the course, and it was the first project that I built on my own. 
The combination of three separate projects in the course gave me the idea and jumpstart in making my version of Flight Club a reality. Thank you Angela! 


