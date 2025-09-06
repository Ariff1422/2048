from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/trivia")
async def get_trivia_answers():
    """
    Returns answers to the UBS Global Coding Challenge 2025 Trivia questions.
    Handles GET requests and returns the list of 25 answers.
    """
    
    # All 25 trivia answers based on the question analysis
    answers = [
        2,  # Q1: Challenges ending with exclamation mark: 3
        1,  # Q2: Ticketing Agent handles: Concert tickets
        3,  # Q3: Blankety Blanks dataset: 1000 lists x 100 elements
        2,  # Q4: Princess Mia's cat: Fat Louie
        4,  # Q5: MST average nodes: 10
        4,  # Q6: No James Bond theme: Amy Winehouse
        2,  # Q7: Smallest font size: 0.5px
        1,  # Q8: Anagram: "graceful the pet"
        2,  # Q9: UBS GCC locations: Australia, Hong Kong, Japan, Singapore
        3,  # Q10: Trading precision: 4 decimal places
        3,  # Q11: UBS Three Pillars: Capital strength, Simplification, Risk mgmt
        3,  # Q12: Flag prefix: UBS
        1,  # Q13: False statement: Landing on Smoke gives backwards throw
        1,  # Q14: Ancient civilization: Human (Twintacle)
        2,  # Q15: Ethical hacker goal: Identify and fix vulnerabilities
        1,  # Q16: Fog-of-Wall action types: 3
        1,  # Q17: Competition prize: All below
        3,  # Q18: Language NOT in question: Chinese
        2,  # Q19: Max sailing club bookings: 1000
        1,  # Q20: Klein Moretti's tarot: The Fool
        3,  # Q21: Largest 2048 grid: 10
        3,  # Q22: Trading bot trades: 49
        4,  # Q23: Micro-mouse legal moves: 136
        3,  # Q24: UBS no branch in: Uruguay
        2   # Q25: UBS Q2 2025 income: 5,357 million USD
    ]
    
    return {"answers": answers}

@app.get("/")
async def root():
    return {"message": "UBS Trivia API - Use GET /trivia for answers"}

@app.get("/health")
async def health():
    return {"status": "ok", "method": "GET requests supported"}

if __name__ == "__main__":
    # Start on port 8100 first (since that's what your logs show)
    print("Starting UBS Trivia API...")
    print("Endpoint: GET /trivia")
    print("Expected response format: {'answers': [2,1,3,2,4,...]}")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8100, log_level="info")
    except OSError:
        print("Port 8100 not available, trying 5000...")
        try:
            uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
        except OSError:
            print("Port 5000 not available, trying 8000...")
            uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
