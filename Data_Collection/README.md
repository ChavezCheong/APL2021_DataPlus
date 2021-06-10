# Phase 1: Building the Data Pipeline
Navigating through unstructured data (web pages and PDFs) and extracting textual data.
## Collecting Data and Building a Data Lake on Amazon S3
Going to the site and collecting web links/PDF files to be assigned to individual cases on the Mortgage Enforcement Actions (MEA) spreadsheet.
### [Massachusetts](https://www.mass.gov/info-details/enforcement-actions-issued-by-the-division-of-banks)
- Collecting links to the web and inserting into corresponding MEA.
### [Ohio](https://apps2.com.ohio.gov/fiin/enforcementlookup/terms.aspx)
- Selenium script to automate downloading of over 6000 PDF files from Ohio's web database and fill in names of downloaded files.
- Identifying relevant patterns in XPaths on page to facilitate automation.

## Preliminary Analysis of MEA Data
### Massachusetts [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ChavezCheong/APL2021_DataPlus/main?urlpath=voila%2Frender%2FData_Collection%2FMA_analysis.ipynb)
- Cleaning of Data (Amending Entity Types and Entity Names)
- Extracting Additional Data (States and Months)
- Creation of Interactive Visualizations with Seaborn and iPyWidget, containerized and presented remotely with Voila and MyBinder
