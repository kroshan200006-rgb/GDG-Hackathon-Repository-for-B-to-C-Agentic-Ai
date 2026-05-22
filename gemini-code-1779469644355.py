import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

class StyleAgent:
    def __init__(self):
        # Initialize the LLM (Requires OPENAI_API_KEY in .env)
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
        # Load mock inventory for context
        try:
            with open("data/inventory.json", "r") as f:
                self.inventory = json.load(f)
        except FileNotFoundError:
            self.inventory = []
            print("Warning: data/inventory.json not found.")

        self.prompt = PromptTemplate(
            input_variables=["user_input", "inventory"],
            template=\"\"\"
            You are an expert AI fashion stylist for Lucknow ethnic wear D2C brands.
            Your goal is to drive conversions by providing highly personalized recommendations.
            
            Available Inventory:
            {inventory}
            
            User Request: "{user_input}"
            
            Analyze the user's occasion, budget, and preferences. 
            Recommend 1-2 exact items from the inventory that create a perfect synergy with their needs. 
            Explain WHY this fits their style and provide the purchase link. Be polite, professional, and persuasive.
            If nothing fits exactly, suggest the closest alternative.
            
            Recommendation:
            \"\"\"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_recommendation(self, user_input: str):
        # Pass the localized inventory as context to the LLM
        inventory_str = json.dumps(self.inventory, indent=2)
        response = self.chain.run(user_input=user_input, inventory=inventory_str)
        return response