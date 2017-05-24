import scrapy
import getpass
import datetime


class MoodleSpider(scrapy.Spider):
    name = "moodle"
    start_urls = [
        'https://moodle.nu.edu.kz/login/index.php',
    ]

    def parse(self, response):
        username = getattr(self, 'u', None)
        password = getattr(self, 'p', None)
        if username is None:
            username = input("Username: ")
        if password is None:
            password = getpass.getpass()
        
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username' : username, 'password': password},
            callback=self.after_login
        )
    
    def after_login(self, response):
        if b"Invalid login" in response.body:
            self.logger.error("Login failed")
            return
        
        cal_page = 'https://moodle.nu.edu.kz/calendar/view.php'
        return scrapy.Request(cal_page, callback=self.get_info)
    
    def get_info(self, response):
        for event in response.css('div.event'):
            yield{
                'name': event.css('h3.referer a::text').extract_first(),
                'course': event.css('div.course a::text').extract_first(),
                'description': event.css('div.description p::text').extract_first(),
                'date': event.css('span.date a::attr(href)').extract_first()[-10:],
            }
