import requests
import streamlit as st

def fetch_data(page=1):
    """
    Fetch data from the API for a specific page.

    Args:
        page (int): The page number to fetch.

    Returns:
        dict: The JSON response from the API if successful, None otherwise.
    """
    url = f"https://devapi.beyondchats.com/api/get_message_with_sources?page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_all_data():
    """
    Retrieve all pages of data from the API.

    Returns:
        list: A list of all data items from the API.
    """
    all_data = []
    page = 1
    while True:
        result = fetch_data(page)
        if result and result['status_code'] == 200:
            data = result['data']['data']
            all_data.extend(data)
            if page >= result['data']['last_page']:
                break
            page += 1
        else:
            break
    return all_data

def identify_citations(data):
    """
    Identify the sources that contributed to each response.

    Args:
        data (list): A list of data items.

    Returns:
        list: A list of citation dictionaries for each data item.
    """
    citations = []
    for item in data:
        response_text = item.get('response', '')
        sources = item.get('sources', [])
        item_citations = []
        for source in sources:
            if source['context'] in response_text:
                item_citations.append({
                    'id': source['id'],
                    'link': source.get('link', '')
                })
        citations.append(item_citations)
    return citations

def main():
    """
    Main function to fetch data, identify citations, and display results using Streamlit.
    """
    st.title("API Data Fetching and Citation Identification")

    data = get_all_data()
    if data:
        st.write("Fetched Data:", data)
        
        # Identify citations
        citations = identify_citations(data)
        st.write("Citations:", citations)
    else:
        st.write("No data fetched from the API.")

if __name__ == "__main__":
    main()
