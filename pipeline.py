import os
import json
from openai import OpenAI
from saathi.tools.sql_tool import SQLTool
from saathi.tools.rag_tool import RAGTool
from saathi.tools.voice_tool import VoiceTool
from dotenv import load_dotenv

load_dotenv("saathi/.env")

class SaathiPipeline:
    def __init__(self):
        self.client = OpenAI()
        self.sql_tool = SQLTool()
        self.rag_tool = RAGTool()
        self.voice_tool = VoiceTool()
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct" # Use a stable model available in the proxy

    def process_query(self, user_input, is_audio=False):
        # 1. Handle Audio Input
        if is_audio:
            user_input = self.voice_tool.stt(user_input)
            if "STT Error" in user_input:
                return user_input, None

        # 2. Intent Classification & Tool Selection
        system_prompt = f"""
        You are Saathi, a crime intelligence assistant. 
        You have access to two tools:
        1. SQL_TOOL: Use this for structured data queries (e.g., counting crimes, finding specific cases). 
           Schema: {self.sql_tool.get_schema()}
        2. RAG_TOOL: Use this for unstructured data queries (e.g., safety tips, witness reports, general info).
        
        Respond ONLY with a JSON object:
        {{
            "tool": "SQL_TOOL" or "RAG_TOOL" or "NONE",
            "query": "the tool-specific query or SQL statement",
            "thought": "brief reasoning"
        }}
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if not content:
            return "Error: No response from model", None
        decision = json.loads(content)
        tool_data = "No tool used."
        
        # 3. Execute Tool
        if decision["tool"] == "SQL_TOOL":
            tool_data = self.sql_tool.execute_query(decision["query"])
        elif decision["tool"] == "RAG_TOOL":
            tool_data = self.rag_tool.query(decision["query"])

        # 4. Generate Final Response
        final_prompt = f"""
        User Query: {user_input}
        Tool Data: {tool_data}
        Reasoning: {decision['thought']}
        
        Provide a helpful, concise response based on the data.
        """
        
        final_response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model=self.model
        ).choices[0].message.content

        # 5. Generate Audio Output (Optional/Always for multimodal feel)
        try:
            audio_path = self.voice_tool.tts(final_response)
        except:
            audio_path = None
        
        return final_response, audio_path

if __name__ == "__main__":
    pipeline = SaathiPipeline()
    res, audio = pipeline.process_query("How many thefts are there?")
    print(f"Response: {res}")
    print(f"Audio: {audio}")
