```mermaid
C4Context
    title System Context diagram for AI Gaming Assistant

    Person(user, "Player", "Uses the assistant to get gameplay advice.")
    System_Ext(game, "Game", "The game being played.")
    System(ai_assistant, "AI Gaming Assistant", "Provides AI-powered gameplay assistance.")
    System_Ext(local_llm, "Local LLM (Future)", "Commercial LLM running on Windows 11 for advanced analysis.")

    Rel(user, ai_assistant, "Uses")
    Rel(ai_assistant, game, "Observes (via Screenshot)")
    Rel_Back(user, game, "Plays")
    Rel(ai_assistant, local_llm, "Sends data for analysis (Future)", "Image, Text")

    UpdateRelStyle(user, ai_assistant, $textColor="white", $lineColor="gray", $offsetX="-40")
    UpdateRelStyle(ai_assistant, game, $textColor="white", $lineColor="gray", $offsetX="-40")
    UpdateRelStyle(user, game, $textColor="white", $lineColor="gray", $offsetX="0")
    UpdateRelStyle(ai_assistant, local_llm, $textColor="white", $lineColor="gray", $offsetX="-40")
```
