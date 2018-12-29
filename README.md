# Student Assistant Bot
Student Assistant Bot is a Telegram bot for checking a course's website to see if there are any changes. It also allows its user to check a product's price just by typing (this feature can be used for the products of [Teknosa](http://www.teknosa.com), [Hepsiburada](http://www.hepsiburada.com), [GittiGidiyor](http://www.gittigidiyor.com), and [n11](http://www.n11.com)).<br/>
You can find the chatbot on Telegram by searching for 'student_mate_bot'. Following commands can be used with this bot.<br/>

| Command        | Explanation  |
| ------------- |:-------------:|
| /addcourse www.url.com     | adds a course page to database|
| /addproduct www.url.com     | adds a product to database     |
| /checkcourse  | checks the announcements     |
| /checkproduct | checks a product's price      |
| /deletecourse | removes a course website from db    |
| /deleteproduct| removes a product from db     |
| /getcourseurl | returns the url of a course     |
| /getproducturl  | returns the url of a product     |
| /productprice | returns the price of a product from db      |
| /courselastupdate | returns the date of the last update from db     |
| /getchatid | returns the chat id      |
| /updateprice newPrice | changes the price of a product     |
| /updatedate newDate | changes the date of last update of a course     |

## How to Use It?
* Clone the repo.
* Run 'main.py'.
* Add the courses and the products you want.
* Send the commands, and see the results.