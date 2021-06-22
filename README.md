# American Predatory Lending Data+ Project - Summer 2021

## Team Members

Authors: [Chavez Cheong](https://github.com/ChavezCheong), Eli Levine

Project Manager: [Malcolm Smith Fraser](https://github.com/malcolmsfraser)

Project Leads: Lee Reiners, Joseph Smith

## Project Description

![American Predatory Lending Logo](https://apl.reclaim.hosting/wp-content/uploads/2021/03/apl_logo-300x261.png)

American Predatory Lending and the Global Financial Crisis is a multi-method interdisciplinary team working under the Bass Connections project within Duke University. Over the past two years, this student-faculty undertaking has explored the state-level dynamics leading up to the 2008 Crisis.

The Summer 2021 Data+ Team is looking to explore a new method of understanding the 2008 Subprime Mortgage Crisis and state-specific legislature leading up to the crisis by examining trends in the text and language of Mortgage Enforcement Actions (MEAs) issues by different states. This unstructured data has traditionally not been accessed nor analyzed.

## Project Phases
### Phase 1 - Data Collection
We extracted MEAs from [Ohio](https://apps2.com.ohio.gov/fiin/enforcementlookup/default.aspx) and [Massachusetts](https://www.mass.gov/info-details/enforcement-actions-issued-by-the-division-of-banks), to be stored in an Amazon S3 Bucket. This required a combination of manual data entry and a Selenium script to automate click-through of a government search portal through XPS path pattern parsing. Following this, we visualized the data to identify macro-level trends in enforcement actions.

> Tech Stack
> - Selenium
> - S3
> - R Markdown
> - Docker
> - Jupyter Notebook
> - Voila


### Phase 2 - Data Extraction and Structuring
#### Massachusetts
As Massachusetts's MEAs were stored on web links or PDFs, we used a mixture of BeautifulSoup and Amazon Textract to extract the MEA text and store it in a CSV.
#### Ohio
With all of Ohio's MEAs on PDFs stored in S3, we built a tech stack with Amazon's cloud infrastructure with Textract to obtain the text from the PDFs and stored it in a CSV.

> Tech Stack
> - S3
> - Boto3
> - IAM
> - Lambda
> - Simple Queue Service (SQS)
> - Simple Notification Service (SNS)
> - Textract
> - BeautifulSoup4

### Phase 3 - Data Visualization and Analysis
With the scraped MEA text stored in CSV files for Massachusetts and Ohio, we will be using LogStash to transfer the data into ElasticSearch for analysis and visualization with Kibana.

> Tech Stack
> - LogStash
> - ElasticSearch
> - Kibana