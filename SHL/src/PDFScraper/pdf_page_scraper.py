import re

# Sample scraped response (only the markdown part is needed for URL extraction)
markdown_text = {
  "markdown": "Search\n\n### Outdated browser detected\n\nWe recommend upgrading to a modern browser.\n\nIf you choose to continue with your current browser we cannot guarantee your experience.\n\nI understand and wish to continue\n\n[Latest browser options](https://browsehappy.com/)\n\n# Agency Manager Solution\n\n#### Description\n\nThe Agency Manager solution is for mid-level sales management positions that include front line management and sales responsibilities. Sample tasks for this job include, but are not limited to: directing and coordinating financial activities of workers in a branch, office, or department of an establishment, such as branch bank, brokerage firm, risk and insurance department, or credit department. Potential job titles that use this solution are: Agency Manager, Brokerage Manager. Multiple configurations of this solution are available.\n\n#### Job levels\n\nFront Line Manager, Manager, Supervisor,\n\n#### Languages\n\nEnglish (USA),\n\n#### Assessment length\n\nApproximate Completion Time in minutes = 51\n\nTest Type:\nABPS\n\nRemote Testing:\n\n#### Downloads\n\n- [Product fact sheet](https://service.shl.com/docs/Fact%20Sheet_%20Agency%20Manager%20Solution%20One%20Sitting_USE.pdf)\n\nEnglish (USA)\n\n\n### Accelerate Your Talent Strategy\n\nSpeak to our team today to see how our products transform talent strategy.\n\n[Book a Demo](https://www.shl.com/about/company/contact/book-a-demo/)\n\n[Back to Product Catalog](https://www.shl.com/solutions/products/product-catalog/)\n\n- A\nAbility & Aptitude\n\n- B\nBiodata & Situational Judgement\n\n- C\nCompetencies\n\n- D\nDevelopment & 360\n\n- E\nAssessment Exercises\n\n- K\nKnowledge & Skills\n\n- P\nPersonality & Behavior\n\n- S\nSimulations",
  "metadata": {
    "msapplication-TileColor": "#da532c",
    "twitter:title": "Agency Manager Solution | SHL",
    "ogTitle": "Agency Manager Solution | SHL",
    "og:url": "https://www.shl.com/solutions/products/product-catalog/view/agency-manager-solution/",
    "title": "Agency Manager Solution | SHL",
    "ogDescription": "Agency Manager Solution: The Agency Manager solution is for mid-level sales management positions that include front line management and sales responsibilities. Sample tasks for this…",
    "theme-color": "#ffffff",
    "ogUrl": "https://www.shl.com/solutions/products/product-catalog/view/agency-manager-solution/",
    "description": "Agency Manager Solution: The Agency Manager solution is for mid-level sales management positions that include front line management and sales responsibilities. Sample tasks for this…",
    "og:type": "article",
    "viewport": "width=device-width, initial-scale=1.0",
    "language": "en-US",
    "ogSiteName": "SHL",
    "twitter:card": "summary_large_image",
    "twitter:site": "",
    "favicon": "https://www.shl.com/favicon.ico",
    "og:title": "Agency Manager Solution | SHL",
    "og:image:height": "630",
    "twitter:description": "Agency Manager Solution: The Agency Manager solution is for mid-level sales management positions that include front line management and sales responsibilities. Sample tasks for this…",
    "og:site_name": "SHL",
    "og:image:width": "1200",
    "og:description": "Agency Manager Solution: The Agency Manager solution is for mid-level sales management positions that include front line management and sales responsibilities. Sample tasks for this…",
    "twitter:image": "https://www.shl.com/assets/logos/Logo-SHL-1200.png",
    "position": [
      "1",
      "2",
      "3"
    ],
    "ogImage": "https://www.shl.com/assets/logos/Logo-SHL-1200.png",
    "og:image": "https://www.shl.com/assets/logos/Logo-SHL-1200.png",
    "scrapeId": "593d743d-c590-42dd-bc48-a07d12966b18",
    "sourceURL": "https://www.shl.com/solutions/products/product-catalog/view/agency-manager-solution/",
    "url": "https://www.shl.com/solutions/products/product-catalog/view/agency-manager-solution/",
    "statusCode": 200
  },
  "scrape_id": "593d743d-c590-42dd-bc48-a07d12966b18"
}


# Regex pattern to match SHL service PDF URLs
pattern = r"https://service\.shl\.com/docs/[^\s)]+\.pdf"

# Extract all matching URLs
pdf_urls = re.findall(pattern, markdown_text)

# Print results
print("Extracted PDF URLs:")
for url in pdf_urls:
    print(url)
