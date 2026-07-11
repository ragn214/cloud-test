import streamlit as st
import json

# 1. SOFTWARE BACKEND: Initialize Session State (Our temporary database)
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "location": "forest_entrance",
        "health": 100,
        "inventory": [],
        "log": ["You wake up at the edge of a dark, whispering forest."]
    }

state = st.session_state.game_state

# Helper function to append events to the game log
def log_event(text):
    state["log"].append(text)

# 2. GAME DESIGN: The Relational World Map Data Structure
WORLD_MAP = {
    "forest_entrance": {
        "title": "🌲 The Forest Entrance",
        "description": "The trees form a dense canopy overhead. A narrow, dark path winds deep into the woods. A shiny metal object glints in the brush nearby.",
        "choices": [
            {"text": "Search the brush", "action": "search_brush"},
            {"text": "Walk down the dark path", "action": "move_deep_forest"}
        ]
    },
    "deep_forest": {
        "title": "🪵 Deep Forest",
        "description": "It is pitch black here. You hear a low growl from behind a massive oak tree. The air smells heavily of iron and fur.",
        "choices": [
            {"text": "Fight the shadow creature", "action": "fight_monster"},
            {"text": "Run back to the entrance", "action": "move_entrance"}
        ]
    },
    "game_over_defeat": {
        "title": "💀 Game Over",
        "description": "Your adventure has come to an end.",
        "choices": [{"text": "Restart Adventure", "action": "reset_game"}]
    },
    "game_over_victory": {
        "title": "🏆 Victory!",
        "description": "You have triumphed over the shadow creature!",
        "choices": [{"text": "Restart Adventure", "action": "reset_game"}]
    }
}

# 3. BACKEND ROUTING: Handle Player Business Logic
def handle_action(action_type):
    if action_type == "search_brush":
        if "Rusty Sword" not in state["inventory"]:
            state["inventory"].append("Rusty Sword")
            log_event("⚔️ You discovered a Rusty Sword hidden in the leaves!")
        else:
            log_event("You search the brush again but find nothing but dirt.")
            
    elif action_type == "move_deep_forest":
        state["location"] = "deep_forest"
        log_event("🚶 You cautiously venture deeper into the dark woods.")
        
    elif action_type == "move_entrance":
        state["location"] = "forest_entrance"
        log_event("🏃 You flee in panic back to the relative safety of the entrance.")
        
    elif action_type == "fight_monster":
        if "Rusty Sword" in state["inventory"]:
            log_event("⚔️ Defiance! You swing your Rusty Sword. With a loud shriek, the shadow creature dissolves into ash. You win!")
            state["location"] = "game_over_victory"
        else:
            state["health"] -= 50
            log_event("💥 Ouch! You fight bare-handed. The creature slashes your arm (-50 HP).")
            if state["health"] <= 0:
                log_event("💀 Your wounds are fatal. You collapse among the roots.")
                state["location"] = "game_over_defeat"
                
    elif action_type == "reset_game":
        st.session_state.clear()
        st.rerun()

# 4. FRONTEND UI & INTERACTIVE LAYER
st.title("🛡️ Backend Text-RPG Engine")
st.write("A hybrid Game Dev and Backend Engineering proof-of-concept.")

# Render Current Location Data
current_loc = WORLD_MAP[state["location"]]
st.subheader(current_loc["title"])
st.info(current_loc["description"])

# Split layout: Choices on Left, Game Logs & Stats on Right
col1, col2 = st.columns([3, 2])

with col1:
    st.write("### Choose Your Action:")
    for choice in current_loc["choices"]:
        # When a button is clicked, execute the backend routing logic
        if st.button(choice["text"], key=choice["action"]):
            handle_action(choice["action"])
            st.rerun()

with col2:
    st.write("### 📊 Player Status")
    st.metric(label="❤️ Health Points", value=f"{state['health']}/100")
    st.write("**🎒 Inventory:**")
    if state["inventory"]:
        for item in state["inventory"]:
            st.markdown(f"- {item}")
    else:
        st.caption("Your pockets are empty.")

# Render Scrollable Game Activity Feed
st.write("---")
st.write("### 📜 Story Log")
for entry in reversed(state["log"]):
    st.write(entry)

# 5. ADVANCED BACKEND FEATURE: Save State to JSON (Simulated Database Dump)
st.sidebar.header("💾 Core Backend Controls")
json_data = json.dumps(state, indent=2)
st.sidebar.download_button(
    label="Export Save File (JSON)",
    data=json_data,
    file_name="rpg_save_file.json",
    mime="application/json"
)
