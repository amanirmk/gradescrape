# Gradescrape

Wishing that Gradescope (a platform for grading used by many colleges) had some information more readily available, I decided to “improve” it with a webscraping project. Essentially, I wrote a core program that collects the resources associated with a webpage, displays it, and feeds redirects back through the same process. This allows one to more or less move around an entire website through an intermediate page. Then on specific Gradescope pages I collect additional information and modify the original HTML to display it to the user.

This project is published [here](https://gradescrape.herokuapp.com) and is functional, but not perfected. **DO NOT** use Gradescrape for important actions such as taking tests or submitting assignments — Gradescrape is meant for viewing rather than doing.

Note: Better experience on Safari

### To do

- Add features to assignment viewing page
- Parse and correctly display json response from Gradescope when attempting to view PDF submissions
- Be able to display code submissions for programming assignments
- Test submitting assignments and taking exams
- Fix certain icons on Chrome
