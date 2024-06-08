# LinkedIn Scraper

A selenium based LinkedIn Scraper that can scrape Name, Role, Emails, Phone Number from URLs or GOOGLE.

```
   __ _       _            _  _____         __
  / /(_)_ __ | | _____  __| | \_   \_ __   / _\ ___ _ __ __ _ _ __   ___ _ __
 / / | | '_ \| |/ / _ \/ _` |  / /\/ '_ \  \ \ / __| '__/ _` | '_ \ / _ \ '__|
/ /__| | | | |   <  __/ (_| /\/ /_ | | | | _\ \ (__| | | (_| | |_) |  __/ |
\____/_|_| |_|_|\_\___|\__,_\____/ |_| |_| \__/\___|_|  \__,_| .__/ \___|_|
                                                             |_|
```

## Features

- Scrape LinkedIn profiles and job postings based on occupation and location.
- Option to use a links file for scraping.
- Support for creating and using cookies.
- Configurable VPN location for accessing LinkedIn.
- Customizable number of pages to scrape.

## Usage

You can use Google to find users on LinkedIn by specifying the occupation and location you want to search. Note that you need to create cookies before using this feature.

Alternatively, you can use a links file that contains URLs of LinkedIn profiles, each separated by a newline.

    python app.py -o OCC [OCC] -l LOC [--limit LIMIT] [--cc CC] [--links LINKS] [--vpn VPN]

Arguments

    -o, --occ: Enter the occupation(s) (required if --links is not used).
    -l, --loc: Enter the location (required if --links is not used).
    --limit: Enter the number of page searches (default: 1).
    --cc: Create cookies (default: False).
    --links: Use links file (default: False).
    --vpn: Enter the location of VPN.

## Examples

1.  Scrape profiles for "Software Engineer" in "San Francisco":

        python script.py -o "Software Engineer" -l "San Francisco" --limit 5

2.  Use a links file for scraping:

        python script.py --links True --limit 5

3.  Create cookies before scraping:

        python script.py -o "Software Engineer" -l "San Francisco" --cc True

4.  Use a VPN for scraping:

        python script.py -o "Software Engineer" -l "San Francisco" --vpn "US"

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

    1. Fork the repository.
    2. Create your feature branch (git checkout -b feature/your-feature).
    3. Commit your changes (git commit -am 'Add some feature').
    4. Push to the branch (git push origin feature/your-feature).
    5. Create a new Pull Request.

## Developer

👤 Anmol Malik

    Twitter: @anmolmalik01
    Instagram: @anmolmalik01
