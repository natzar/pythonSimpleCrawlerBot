def check_domain_availability(domain):
    headers = {"User-Agent": CHROME_USER_AGENT}
    try:
        response = requests.head('http://'+domain, headers=headers, timeout=5)
        # If the response is a client or server error, it might indicate that the domain is available
        if response.status_code >= 400:
            return True
        return False
    except requests.ConnectionError:
        # Connection errors may indicate that the domain is available
        return True
    except Exception as e:
        print(f"Error checking availability for {domain}: {e}")
        return False

