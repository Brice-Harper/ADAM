import requests
from bs4 import BeautifulSoup


def fetch_metadata(url):
    """
    Récupère automatiquement les métadonnées d'une page web.
    Retourne un dictionnaire avec title, description et image.
    """
    result = {
        "title": "",
        "description": "",
        "image": "",
    }

    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ADAM-Bot/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Titre — priorité aux balises Open Graph
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            result["title"] = og_title["content"]
        elif soup.title:
            result["title"] = soup.title.string or ""

        # Description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            result["description"] = og_desc["content"]
        else:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                result["description"] = meta_desc["content"]

        # Image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            result["image"] = og_image["content"]

    except Exception:
        pass

    return result
