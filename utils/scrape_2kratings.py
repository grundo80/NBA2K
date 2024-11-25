"""
This is the logic for scraping player data from 2Kratings.com.
"""

import cloudscraper
from lxml import html
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

def scrape_player_data(player_url_part):
    """
    Function to scrape data for a specific player.
    """
    BASE_URL = "https://www.2kratings.com/"
    URL = f"{BASE_URL}{player_url_part}"

    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(URL)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": "Failed to retrieve player data due to HTTP error."}
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        return {"error": "An unexpected error occurred while trying to scrape player data."}

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    tree = html.fromstring(response.content)

    try:
        player_name_tag = soup.find("h1", class_="header-title pt-2 mb-0")
        if player_name_tag:
            player_name = player_name_tag.text.strip()
        else:
            raise ValueError("Player name not found on the page.")

        attributes = {}
        attribute_elements = soup.find_all("li", class_="mb-1")

        for attr in attribute_elements:
            raw_attribute_text = attr.text.strip()
            raw_attribute_name = "_".join(raw_attribute_text.split("\n")[0].split(" ")[1:]).lower()
            
            # Check if the attribute name contains a number at the start
            if any(char.isdigit() for char in raw_attribute_name):
                parts = raw_attribute_name.split("_", 1)
                if len(parts) > 1:
                    clean_attribute_name = parts[1]
                else:
                    clean_attribute_name = raw_attribute_name
            else:
                clean_attribute_name = raw_attribute_name

            clean_attribute_name = clean_attribute_name.replace("-", "_")

            try:
                attribute_value = int(attr.find("span", class_="attribute-box").text.strip())
            except AttributeError:
                continue

            if clean_attribute_name.startswith("interior_defense"):
                clean_attribute_name = "interior_defense"

            attributes[clean_attribute_name] = attribute_value

        try:
            intangibles_label = soup.find(lambda tag: tag.name == "h4" and "Intangibles" in tag.text)
            if intangibles_label:
                intangibles_value = int(intangibles_label.find_next("span", class_="attribute-box medium").text.strip())
                attributes["intangibles"] = intangibles_value
            else:
                print("Intangibles label not found.")
        except Exception as e:
            print(f"Error extracting intangibles: {e}")

        # Extract badges
        badges = {}
        badges_section = soup.find("div", class_="tab-pane fade show active rounded-bottom rounded-right bg-white px-3 pt-1 btl-0")
        if badges_section:
            badge_containers = badges_section.find_all("div", class_="row no-gutters badge-card")
            for badge_container in badge_containers:
                badge_img = badge_container.find("img")
                if badge_img:
                    badge_src = badge_img.get("data-src")
                    badge_name = badge_container.find("h4", class_="text-white").text.strip().replace(" ", "_").replace("-", "_").lower()
                    badge_string = badge_src.split("-")[-2]
                    if badge_string == "legendary":
                        badge_level = "Legendary"
                    elif badge_string == "hof":
                        badge_level = "Hall of Fame"
                    elif badge_string == "gold":
                        badge_level = "Gold"
                    elif badge_string == "silver":
                        badge_level = "Silver"
                    elif badge_string == "bronze":
                        badge_level = "Bronze"
                    else:
                        badge_level = "None"

                    badges[badge_name] = badge_level
                else:
                    print(f"Badge image not found for {badge_container}")
    except ValueError as parse_err:
        print(f"Data parsing error: {parse_err}")
        return {"error": f"Failed to parse player data: {parse_err}"}
    except Exception as err:
        print(f"An unexpected error occurred during parsing: {err}")
        return {"error": "An unexpected error occurred while parsing player data."}

    # Create player data dictionary to return
    player_data = {
        "player_name": player_name,
        "attributes": attributes,
        "badges": badges,
    }

    return player_data

if __name__ == "__main__":
    player = input("Enter player URL part: ")
    player_data = scrape_player_data(player)
