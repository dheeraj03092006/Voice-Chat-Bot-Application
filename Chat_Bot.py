from dotenv import load_dotenv
import os
from groq import Groq
import sys

load_dotenv()

class LanguageModelProcessor:
    def __init__(self):
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please set one.")
        
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.1-8b-instant"
        
        # Load Bot prompt
        try:
            with open('Bot_prompt.txt', 'r') as file:
                self.bot_prompt = file.read().strip()
        except FileNotFoundError:
            self.bot_prompt = "You are a helpful AI assistant. Respond in a friendly and helpful manner."
        
        # Store conversation history
        self.conversation_history = []

    def process(self, text):
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": text})
            
            # Create messages for the API call
            messages = [
                {"role": "system", "content": self.bot_prompt}
            ] + self.conversation_history
            
            # Keep only last 10 messages to avoid token limits
            if len(messages) > 11:  # 1 system + 10 conversation messages
                messages = [messages[0]] + messages[-10:]
                self.conversation_history = self.conversation_history[-10:]
            
            # Get response from GROQ
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"


class ConversationManager:
    def __init__(self):
        self.llm_processor = LanguageModelProcessor()
        print()
        print("Chatbot initialized. Type 'goodbye' to end.")
        print()

    def main(self):
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "goodbye"]:
                print("Bot: Goodbye!")
                break

            llm_response = self.llm_processor.process(user_input)
            print(f"🤖  : {llm_response}")
            print()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # API mode: process the first argument as the user message
        user_message = ' '.join(sys.argv[1:])
        processor = LanguageModelProcessor()
        response = processor.process(user_message)
        print(response)
    else:
        # Interactive mode
        manager = ConversationManager()
        manager.main()
