_apiKey = None

def getApiKey():
    global _apiKey
    if _apiKey:
        return _apiKey
    _apiKey = input("Cole a sua Gemini API Key: ").strip()
    return _apiKey
