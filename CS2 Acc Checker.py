import streamlit as st
import re
import requests
import webbrowser

def extract_steamid(steam_url):
    match = re.search(r"steamcommunity\.com/id/([\w\d_]+)", steam_url)
    if match:
        username = match.group(1)
        steamid = get_steamid_from_html(f"https://steamcommunity.com/id/{username}")
        if steamid:
            return steamid
    match = re.search(r"steamcommunity\.com/profiles/(\d+)", steam_url)
    if match:
        return match.group(1)
    return None

def get_steamid_from_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        match = re.search(r'g_rgProfileData = ({.*?});', response.text, re.DOTALL)
        if match:
            profile_data = match.group(1)
            steamid_match = re.search(r'"steamid":"(\d+)"', profile_data)
            if steamid_match:
                return steamid_match.group(1)
    except requests.exceptions.RequestException:
        pass
    return None

def open_links(urls, site):
    if not urls:
        st.warning("Введите хотя бы одну ссылку!")
        return

    steamids = []
    for url in urls:
        steamid = extract_steamid(url)
        if steamid:
            steamids.append(steamid)
        else:
            st.warning(f"SteamID не найден для {url}")

    if steamids:
        if site == "all":
            for steamid in steamids:
                webbrowser.open(f"https://faceitanalyser.com/stats/{steamid}/cs2")
                webbrowser.open(f"https://csstats.gg/player/{steamid}")
        elif site == "csstats":
            for steamid in steamids:
                webbrowser.open(f"https://csstats.gg/player/{steamid}")
        elif site == "faceitanalyser":
            for steamid in steamids:
                webbrowser.open(f"https://faceitanalyser.com/stats/{steamid}/cs2")

def main():
    st.title("CS2 Acc Checker")
    st.write("Введите до 5 ссылок на Steam-профили:")

    urls = [st.text_input("", key=f"url_{i}", placeholder="Введите ссылку...", label_visibility="collapsed") for i in range(5)]
    urls = [url for url in urls if url.strip()]

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Открыть все", use_container_width=True):
            open_links(urls, "all")

    with col2:
        if st.button("CSStats", use_container_width=True):
            open_links(urls, "csstats")

    with col3:
        if st.button("FaceitAnalyzer", use_container_width=True):
            open_links(urls, "faceitanalyser")

    if st.button("Очистить", use_container_width=True):
        st.experimental_rerun()


if __name__ == "__main__":
    main()
