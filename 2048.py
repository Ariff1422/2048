import math
import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# In-memory storage for game states
games = {}

# Pydantic models for request and response validation
class NewGameResponse(BaseModel):
    game_id: str
    grid: List[List[int]]
    score: int
    game_over: bool

class MoveRequest(BaseModel):
    game_id: str
    direction: str

class MoveResponse(BaseModel):
    game_id: str
    grid: List[List[int]]
    score: int
    game_over: bool

# --- Game Logic Functions ---

def add_new_tile(grid):
    empty_cells = []
    for row in range(4):
        for col in range(4):
            if grid[row][col] == 0:
                empty_cells.append((row, col))
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 2 if random.random() < 0.9 else 4

def rotate_grid(grid, num_rotations):
    rotated_grid = [row[:] for row in grid]
    for _ in range(num_rotations):
        rotated_grid = [list(col) for col in zip(*rotated_grid[::-1])]
    return rotated_grid

def compress_and_merge(grid, score):
    new_grid = [[0]*4 for _ in range(4)]
    moved = False
    
    for row in range(4):
        col_idx = 0
        for col in range(4):
            if grid[row][col] != 0:
                new_grid[row][col_idx] = grid[row][col]
                if col_idx != col:
                    moved = True
                col_idx += 1
    
    merged = False
    for row in range(4):
        for col in range(3):
            if new_grid[row][col] == new_grid[row][col+1] and new_grid[row][col] != 0:
                new_grid[row][col] *= 2
                score += new_grid[row][col]
                new_grid[row][col+1] = 0
                merged = True
    
    if merged:
        moved = True
        temp_grid = new_grid
        new_grid = [[0]*4 for _ in range(4)]
        for row in range(4):
            col_idx = 0
            for col in range(4):
                if temp_grid[row][col] != 0:
                    new_grid[row][col_idx] = temp_grid[row][col]
                    col_idx += 1
    
    return new_grid, score, moved

def is_game_over(grid):
    for row in range(4):
        for col in range(4):
            if grid[row][col] == 0:
                return False
            if col < 3 and grid[row][col] == grid[row][col+1]:
                return False
            if row < 3 and grid[row][col] == grid[row+1][col]:
                return False
    return True

# --- API Endpoints ---

@app.post("/api/new_game", response_model=NewGameResponse)
async def new_game():
    game_id = str(random.randint(1000, 9999))
    grid = [[0]*4 for _ in range(4)]
    add_new_tile(grid)
    add_new_tile(grid)
    
    games[game_id] = {'grid': grid, 'score': 0, 'game_over': False}
    return NewGameResponse(game_id=game_id, grid=grid, score=0, game_over=False)

@app.post("/api/move", response_model=MoveResponse)
async def handle_move(req: MoveRequest):
    game = games.get(req.game_id)
    if not game:
        # In a real app, you would handle a 404 error here.
        # For simplicity, we'll return a basic error.
        return {"error": "Game not found"}
    
    current_grid = game['grid']
    current_score = game['score']
    
    rotations = {'left': 0, 'up': 1, 'right': 2, 'down': 3}
    rotated_grid = rotate_grid(current_grid, rotations.get(req.direction, 0))
    
    # Check if a move is possible before processing
    temp_grid, _, _ = compress_and_merge(rotated_grid, 0)
    if temp_grid == rotated_grid:
        return MoveResponse(game_id=req.game_id, grid=current_grid, score=current_score, game_over=is_game_over(current_grid))

    updated_grid, updated_score, moved = compress_and_merge(rotated_grid, current_score)
    final_grid = rotate_grid(updated_grid, (4 - rotations.get(req.direction, 0)) % 4)

    if moved:
        add_new_tile(final_grid)

    game['grid'] = final_grid
    game['score'] = updated_score
    game['game_over'] = is_game_over(final_grid)

    return MoveResponse(game_id=req.game_id, grid=final_grid, score=updated_score, game_over=game['game_over'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
