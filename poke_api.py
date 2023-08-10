import os
import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI."""
    pokemon = str(pokemon).strip().lower()
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def get_all_pokemon_names():
    """Returns a list of all Pokémon names."""
    url = "https://pokeapi.co/api/v2/pokemon/?limit=1200"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve Pokémon list.")
        return []

    data = response.json()
    return [poke["name"] for poke in data["results"]]

def download_pokemon_artwork(pokemon_name, save_dir="."):
    """Downloads and saves the artwork of a specified Pokémon."""
    info = get_pokemon_info(pokemon_name)

    if not info:
        return None

    image_url = info["sprites"]["other"]["official-artwork"]["front_default"]
    image_response = requests.get(image_url, stream=True)

    if image_response.status_code != 200:
        print(f"Failed to download artwork for {pokemon_name}.")
        return None

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, f"{pokemon_name}.png")

    with open(file_path, "wb") as image_file:
        for chunk in image_response.iter_content(chunk_size=8192):
            image_file.write(chunk)

    return file_path

def main():
    # Test out the get_pokemon_info() function
    poke_info = get_pokemon_info("Rockruff")
    print(poke_info)

    # Test get_all_pokemon_names
    all_names = get_all_pokemon_names()
    print(all_names[:10])  # Print first 10 names

    # Test download_pokemon_artwork
    file_path = download_pokemon_artwork("Rockruff", "downloads")
    print(f"Downloaded to: {file_path}")

if __name__ == '__main__':
    main()
