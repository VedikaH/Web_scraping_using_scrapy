import scrapy

class CourseDetSpider(scrapy.Spider):
    name = "course_det"
    allowed_domains = ["talentedge.com"]
    start_urls = ["https://talentedge.com/golden-gate-university/doctor-of-business-administration","https://talentedge.com/iim-kozhikode/professional-certificate-programme-in-hr-management-and-analytics","https://talentedge.com/opjindal-global-business-school/masters-of-business-administration-opj-global-university","https://talentedge.com/esgci-school-of-management-paris/doctorate-of-business-administration-esgci","https://talentedge.com/goa-institute-of-management/exectuive-pg-program-in-health-care-management","https://talentedge.com/iim-lucknow/supply-chain-management","https://talentedge.com/iim-lucknow/advanced-program-in-strategic-management-for-business-excellence","https://talentedge.com/iim-raipur/post-graduate-executive-certification-in-human-resource-management-iimr-hr","https://talentedge.com/iim-kozhikode/professional-certificate-program-in-strategic-management","https://talentedge.com/iim-kozhikode/applied-financial-risk-management-course"]
    
    def parse(self, response):
        faculty_members = response.css('div.facutly-card')
        faculty_data = {}
        
        for index, faculty in enumerate(faculty_members, 1):
            faculty_name = faculty.css('h4.best-fname::text').get().strip()
            faculty_designation = faculty.css('p.best-fdesingnation::text').get().strip()
            faculty_description = faculty.css('a.showFacultyDescription::attr(data-description)').get().strip()
            
            faculty_data.update({
                f'Faculty {index} Name': faculty_name,
                f'Faculty {index} Designation': faculty_designation,
                f'Faculty {index} Description': faculty_description,
            })
        
        yield {
            'course link': response.url,
            'title': response.css('h1.pl-title::text').get(default='').strip() + response.css('h1.pl-title b::text').get(default='').strip(),
            'description': response.css('div.desc > p::text').get(default=''),
            'duration': response.css('div.duration-of-course ul li:nth-of-type(1) p strong::text').get(default='').strip(),
            'Timing': response.css('div.duration-of-course ul li:nth-of-type(1) p::text').get(default='').strip(),
            'start_date': response.css('div.duration-of-course ul li:nth-of-type(2) p strong::text').get(default='').strip(),
            'What you will learn': list(set([li.strip() for li in response.css('div.pl-deeper-undstnd.to_flex_ul ul li::text').getall()])),
            'skills': [skill.strip() for skill in response.css('div.key-skills-sec ul li::text').getall()],
            'target students': response.css('div.cs-content h4.cs-titlec::text').get(default='').replace('\n', '').strip(),
            'Prerequisites / Eligibility criteria': " ".join(response.css('div.eligible-right-top-list *::text').getall()).replace("\r", " ").replace("\n", " ").replace("\t", " ").strip(),
            'Content': [item.strip() for item in response.css('div.sylab-tab-ul ul.syl-ul li a::text').getall()],
            'university': response.css('h4.about-ititle::text').get(default=''),
            **faculty_data,
            'fee in inr': response.css('div.program-details-total-pay-amt.ruppes div.program-details-total-pay-amt-right::text ').get(default='').replace('\n', '').strip(),
            'fee in usd': response.css('div.program-details-total-pay-amt.dolor div.program-details-total-pay-amt-right::text ').get(default='').replace('\n', '').strip()
        }