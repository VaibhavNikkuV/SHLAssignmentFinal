import re
import json

# Your JSON string
data = {
  "markdown": "Search\n\n### Outdated browser detected\n\nWe recommend upgrading to a modern browser.\n\nIf you choose to continue with your current browser we cannot guarantee your experience.\n\nI understand and wish to continue\n\n[Latest browser options](https://browsehappy.com/)\n\n# Find assessments that best meet your needs.\n\n##### Browse through our extensive product catalog for science-backed assessments that evaluate cognitive ability, personality, behavior, skills, and more, by role and organizational level, by industry, and by language.\n\n## Search by keyword...\n\nKeyword\n\nSearchReset all\n\n## Search by choosing one or more...\n\nJob Family\n\nSelect...\n\n\nSelect...\n\n\nSelect...\n\n\nBusiness\n\n\nClerical\n\n\nContact Center\n\n\nCustomer Service\n\n\nInformation Technology\n\n\nSafety\n\n\nSales\n\n\nJob Level\n\nSelect...\n\n\nSelect...\n\n\nSelect...\n\n\nDirector\n\n\nEntry-Level\n\n\nExecutive\n\n\nFront Line Manager\n\n\nGeneral Population\n\n\nGraduate\n\n\nManager\n\n\nMid-Professional\n\n\nProfessional Individual Contributor\n\n\nSupervisor\n\n\nIndustry\n\nSelect...\n\n\nSelect...\n\n\nSelect...\n\n\nBanking/Finance\n\n\nHealthcare\n\n\nHospitality\n\n\nInsurance\n\n\nManufacturing\n\n\nOil & Gas\n\n\nRetail\n\n\nTelecommunications\n\n\nLanguage\n\nSelect...\n\n\nSelect...\n\n\nSelect...\n\n\nArabic\n\n\nBulgarian\n\n\nChinese Simplified\n\n\nChinese Traditional\n\n\nCroatian\n\n\nCzech\n\n\nDanish\n\n\nDutch\n\n\nEnglish (Australia)\n\n\nEnglish (Canada)\n\n\nEnglish International\n\n\nEnglish (Malaysia)\n\n\nEnglish (Singapore)\n\n\nEnglish (South Africa)\n\n\nEnglish (USA)\n\n\nEstonian\n\n\nFinnish\n\n\nFlemish\n\n\nFrench\n\n\nFrench (Belgium)\n\n\nFrench (Canada)\n\n\nGerman\n\n\nGreek\n\n\nHungarian\n\n\nIcelandic\n\n\nIndonesian\n\n\nItalian\n\n\nJapanese\n\n\nKorean\n\n\nLatin American Spanish\n\n\nLatvian\n\n\nLithuanian\n\n\nMalay\n\n\nNorwegian\n\n\nPolish\n\n\nPortuguese\n\n\nPortuguese (Brazil)\n\n\nRomanian\n\n\nRussian\n\n\nSerbian\n\n\nSlovak\n\n\nSpanish\n\n\nSwedish\n\n\nThai\n\n\nTurkish\n\n\nVietnamese\n\n\nSearchReset all\n\n## Search by job by title...\n\nJob Category\n\nSelect...\n\n\nSelect...\n\n\nSelect...\n\n\nArchitecture and Engineering\n\n\nArts, Design, and Media\n\n\nBuilding and Grounds Cleaning and Maintenance\n\n\nBusiness and Financial Operations\n\n\nCommunity and Social Services\n\n\nComputer and Mathematical\n\n\nConstruction and Extraction\n\n\nContact Center and Customer Service\n\n\nEducation, Training, and Library\n\n\nFarming, Fishing, and Forestry\n\n\nFood Preparation and Serving Related\n\n\nHealth and Environmental Science\n\n\nHealthcare Practitioners and Technical\n\n\nHealthcare Support\n\n\nLegal\n\n\nManagement and Leadership\n\n\nOffice and Administrative Support\n\n\nPersonal Care and Service\n\n\nProduction\n\n\nProtective Service\n\n\nSales and Related\n\n\nSkilled Electrical, Mechanical, and Industrial\n\n\nTransportation and Material Moving\n\n\nJob Title\n\nSelect...\n\n\nSearchReset all\n\n| Pre-packaged Job Solutions | Remote Testing | Adaptive/IRT | Test Type |\n| --- | --- | --- | --- |\n| [Account Manager Solution](https://www.shl.com/solutions/products/product-catalog/view/account-manager-solution/) |  |  | CPAB |\n| [Administrative Professional - Short Form](https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/) |  |  | AKP |\n| [Agency Manager Solution](https://www.shl.com/solutions/products/product-catalog/view/agency-manager-solution/) |  |  | ABPS |\n| [Apprentice + 8.0 Job Focused Assessment](https://www.shl.com/solutions/products/product-catalog/view/apprentice-8-0-job-focused-assessment-4261/) |  |  | BP |\n| [Apprentice 8.0 Job Focused Assessment](https://www.shl.com/solutions/products/product-catalog/view/apprentice-8-0-job-focused-assessment/) |  |  | BP |\n| [Bank Administrative Assistant - Short Form](https://www.shl.com/solutions/products/product-catalog/view/bank-administrative-assistant-short-form/) |  |  | ABKP |\n| [Bank Collections Agent - Short Form](https://www.shl.com/solutions/products/product-catalog/view/bank-collections-agent-short-form/) |  |  | ABP |\n| [Bank Operations Supervisor - Short Form](https://www.shl.com/solutions/products/product-catalog/view/bank-operations-supervisor-short-form/) |  |  | ABPS |\n| [Bilingual Spanish Reservation Agent Solution](https://www.shl.com/solutions/products/product-catalog/view/bilingual-spanish-reservation-agent-solution/) |  |  | BPSA |\n| [Bookkeeping, Accounting, Auditing Clerk Short Form](https://www.shl.com/solutions/products/product-catalog/view/bookkeeping-accounting-auditing-clerk-short-form/) |  |  | PSKBA |\n| [Branch Manager - Short Form](https://www.shl.com/solutions/products/product-catalog/view/branch-manager-short-form/) |  |  | ABP |\n| [Cashier Solution](https://www.shl.com/solutions/products/product-catalog/view/cashier-solution/) |  |  | BAP |\n\n- Previous\n- 1\n- [2](https://www.shl.com/solutions/products/product-catalog/?start=12&type=2)\n- [3](https://www.shl.com/solutions/products/product-catalog/?start=24&type=2)\n- …\n- [12](https://www.shl.com/solutions/products/product-catalog/?start=132&type=2)\n- [Next](https://www.shl.com/solutions/products/product-catalog/?start=12&type=2)\n\n| Individual Test Solutions | Remote Testing | Adaptive/IRT | Test Type |\n| --- | --- | --- | --- |\n| [Global Skills Development Report](https://www.shl.com/solutions/products/product-catalog/view/global-skills-development-report/) |  |  | AEBCDP |\n| [.NET Framework 4.5](https://www.shl.com/solutions/products/product-catalog/view/net-framework-4-5/) |  |  | K |\n| [.NET MVC (New)](https://www.shl.com/solutions/products/product-catalog/view/net-mvc-new/) |  |  | K |\n| [.NET MVVM (New)](https://www.shl.com/solutions/products/product-catalog/view/net-mvvm-new/) |  |  | K |\n| [.NET WCF (New)](https://www.shl.com/solutions/products/product-catalog/view/net-wcf-new/) |  |  | K |\n| [.NET WPF (New)](https://www.shl.com/solutions/products/product-catalog/view/net-wpf-new/) |  |  | K |\n| [.NET XAML (New)](https://www.shl.com/solutions/products/product-catalog/view/net-xaml-new/) |  |  | K |\n| [Accounts Payable (New)](https://www.shl.com/solutions/products/product-catalog/view/accounts-payable-new/) |  |  | K |\n| [Accounts Payable Simulation (New)](https://www.shl.com/solutions/products/product-catalog/view/accounts-payable-simulation-new/) |  |  | S |\n| [Accounts Receivable (New)](https://www.shl.com/solutions/products/product-catalog/view/accounts-receivable-new/) |  |  | K |\n| [Accounts Receivable Simulation (New)](https://www.shl.com/solutions/products/product-catalog/view/accounts-receivable-simulation-new/) |  |  | S |\n| [ADO.NET (New)](https://www.shl.com/solutions/products/product-catalog/view/ado-net-new/) |  |  | K |\n\n- Previous\n- 1\n- [2](https://www.shl.com/solutions/products/product-catalog/?start=12&type=1)\n- [3](https://www.shl.com/solutions/products/product-catalog/?start=24&type=1)\n- …\n- [32](https://www.shl.com/solutions/products/product-catalog/?start=372&type=1)\n- [Next](https://www.shl.com/solutions/products/product-catalog/?start=12&type=1)\n\n- A\nAbility & Aptitude\n\n- B\nBiodata & Situational Judgement\n\n- C\nCompetencies\n\n- D\nDevelopment & 360\n\n- E\nAssessment Exercises\n\n- K\nKnowledge & Skills\n\n- P\nPersonality & Behavior\n\n- S\nSimulations\n\n\n## Explore SHL’s Wide Range of Assessment Solutions\n\nLooking to discover more about SHL’s broader solution offerings, rather than browsing this assessments catalog?\n\n[See Our Solutions](https://www.shl.com/solutions/)",
  "metadata": {
    "og:image:width": "1200",
    "twitter:card": "summary_large_image",
    "title": "Talent Assessments Catalog | SHL",
    "description": "Browse through our product assessment catalog for unrivalled employee assessments that evaluate cognitive ability, personality, behavior, skills, and more.",
    "viewport": "width=device-width, initial-scale=1.0",
    "ogDescription": "SHL Talent Assessment Catalog",
    "og:description": "SHL Talent Assessment Catalog",
    "og:image:height": "630",
    "twitter:image": "https://www.shl.com/assets/logos/Logo-SHL-1200.png",
    "twitter:site": "",
    "og:title": "SHL Talent Assessment Catalog",
    "language": "en-US",
    "theme-color": "#ffffff",
    "ogSiteName": "SHL",
    "ogImage": "https://www.shl.com/assets/logos/Logo-SHL-1200.png",
    "og:site_name": "SHL",
    "og:image": "https://www.shl.com/assets/logos/Logo-SHL-1200.png",
    "og:type": "article",
    "twitter:title": "SHL Talent Assessment Catalog",
    "twitter:description": "SHL Talent Assessment Catalog",
    "position": [
      "1",
      "2",
      "3"
    ],
    "favicon": "https://www.shl.com/favicon.ico",
    "ogTitle": "SHL Talent Assessment Catalog",
    "ogUrl": "https://www.shl.com/solutions/products/product-catalog/",
    "msapplication-TileColor": "#da532c",
    "og:url": "https://www.shl.com/solutions/products/product-catalog/",
    "scrapeId": "e463b0c9-5292-4bcc-ac07-e4a7b70be7b7",
    "sourceURL": "https://www.shl.com/solutions/products/product-catalog/",
    "url": "https://www.shl.com/solutions/products/product-catalog/",
    "statusCode": 200
  },
  "scrape_id": "e463b0c9-5292-4bcc-ac07-e4a7b70be7b7"
}  # Replace this with your actual JSON (as a Python dictionary)

# Convert JSON dictionary to string (if it's not already)
json_str = json.dumps(data)

# Regular expression to match SHL product catalog view URLs
urls = re.findall(r"https:\/\/www\.shl\.com\/solutions\/products\/product-catalog\/view\/[a-z0-9\-]+\/", json_str)

# Optional: remove duplicates
unique_urls = list(set(urls))

# Print result
# for url in unique_urls:
#     print(url,"\n")

# print(len(unique_urls))


# Convert JSON to string if needed
json_str = json.dumps(data)

# Regex pattern for SHL paginated catalog URLs
pagination_urls = re.findall(
    r"https:\/\/www\.shl\.com\/solutions\/products\/product-catalog\/\?start=\d+&type=\d+",
    json_str
)

# Remove duplicates
unique_pagination_urls = list(set(pagination_urls))

# Print results
for url in unique_pagination_urls:
    print(url)

print(len(unique_pagination_urls))