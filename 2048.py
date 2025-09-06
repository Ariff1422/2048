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
        4,  // Q1: Only one challenge title ends with an exclamation mark
    1,  // Q2: Ticketing Agent handles Concert tickets
    3,  // Q3: 1000 lists × 100 elements
    2,  // Q4: Princess Mia’s cat is Fat Louie
    4,  // Q5: MST average number of nodes is 10
    4,  // Q6: Amy Winehouse did not have a James Bond theme song
    4,  // Q7: Smallest font size is 1.5px
    5,  // Q8: “patch after glue” is the anagram of “Capture The Flag”
    2,  // Q9: The challenge has been held in Australia, Hong Kong, Japan, Singapore
    3,  // Q10: Ensure precision to 4 decimal places
    3,  // Q11: UBS Three Pillars: Capital strength, Simplification and efficiency, Risk management
    3,  // Q12: Flags are prefixed with “UBS”
    4,  // Q13: Output is not the number of players and dice rolls (false statement)
    1,  // Q14: The ancient civilization preceding Octupusini is Human
    2,  // Q15: Ethical hackers aim to identify and fix security vulnerabilities
    1,  // Q16: There are 3 possible action types
    1,  // Q17: Prize: All of the listed benefits
    3,  // Q18: Chinese is not in the Duolingo Sorting question
    2,  // Q19: Maximum sailing club bookings: 1000
    1,  // Q20: Klein Moretti is represented by “The Fool”
    3,  // Q21: Largest 2048 grid is 10×10
    3,  // Q22: Trading bot executes 49 trades
    4,  // Q23: Micro‑mouse has 136 legal move combinations
    3,  // Q24: UBS does not have a branch office in Uruguay
    1   // Q25: UBS’s total comprehensive income for Q2 2025 was 5,335 million USD
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
