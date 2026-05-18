from dotenv import load_dotenv
import os

load_dotenv()

# ============================================
# TEST 1 - GROQ (Llama 3.3 70B)
# ============================================
def test_groq():
    print("\n🔵 Testing Groq (Llama 3.3 70B)...")
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a security tool. Reply only with THREAT or SAFE."
                },
                {
                    "role": "user",
                    "content": "normal user login at 9am"
                }
            ]
        )

        result = response.choices[0].message.content
        print(f"✅ Groq works! Response: {result}")

    except Exception as e:
        print(f"❌ Groq failed: {e}")


# ============================================
# TEST 2 - GROQ (Gemma2 9B — Google model, free)
# ============================================
def test_gemini():
    print("\n🟢 Testing Groq (Gemma2 9B)...")
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a security tool. Reply only with THREAT or SAFE."
                },
                {
                    "role": "user",
                    "content": "normal user login at 9am"
                }
            ]
        )

        result = response.choices[0].message.content
        print(f"✅ Gemma2 9B works! Response: {result}")

    except Exception as e:
        print(f"❌ Gemma2 9B failed: {e}")


# ============================================
# TEST 3 - GROQ (Llama 3.1 8B) — replaces Anthropic
# ============================================
def test_mixtral():
    print("\n🟣 Testing Groq (Llama 3.1 8B)...")
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a security tool. Reply only with THREAT or SAFE."
                },
                {
                    "role": "user",
                    "content": "normal user login at 9am"
                }
            ]
        )

        result = response.choices[0].message.content
        print(f"✅ Llama 3.1 8B works! Response: {result}")

    except Exception as e:
        print(f"❌ Mixtral failed: {e}")


# ============================================
# RUN ALL TESTS
# ============================================
print("=" * 40)
print("   API CONNECTION TESTS")
print("=" * 40)

test_groq()
test_gemini()
test_mixtral()

print("\n" + "=" * 40)
print("Done! Fix any ❌ before moving forward.")
print("=" * 40)
