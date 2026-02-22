from backend.openai_helper import OpenAIHelper

try:
    helper = OpenAIHelper()
    reply = helper.test_connection()

    print("\n✅ OpenAI GPT-3.5 Connection Successful!")
    print("Response:")
    print(reply)

except Exception as e:
    print("\n❌ OpenAI API Test Failed")
    print("Error:", e)
