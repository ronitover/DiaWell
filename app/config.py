import os

# IBM WatsonX Granite API Configuration
# Environment variables take precedence over hardcoded values
IBM_WX_URL = os.getenv("IBM_WX_URL", "https://au-syd.ml.cloud.ibm.com")
IBM_WX_API_KEY = os.getenv("IBM_WX_API_KEY", "tO3VKD0y4vjEa0_8lGdyP81jHbJNuwfuphEqL6SMEnJo")
IBM_WX_PROJECT_ID = os.getenv("IBM_WX_PROJECT_ID", "57bf082e-c759-4b7f-803f-1d92ea56dd3a")
IBM_WX_MODEL_ID = os.getenv("IBM_WX_MODEL_ID", "ibm/granite-13b-instruct")

# Note: If you're still getting 401 errors, you may need to:
# 1. Get a fresh API key from IBM Cloud Console
# 2. Ensure the API key has WatsonX permissions
# 3. Check if the project ID is correct and accessible
