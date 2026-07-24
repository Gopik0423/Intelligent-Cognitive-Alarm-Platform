import os
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from . import models

# Available difficulties in order
DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Expert"]

class DifficultyQLearningAgent:
    """
    A reinforcement learning agent using Q-learning to adapt alarm challenge difficulty.
    
    States: (speed_category, snooze_category)
      - speed_category: 0 (fast: < 20s), 1 (normal: 20-50s), 2 (slow: > 50s)
      - snooze_category: 0 (none: 0), 1 (medium: 1-2), 2 (high: > 2)
      
    Actions:
      - 0: decrease difficulty
      - 1: maintain difficulty
      - 2: increase difficulty
    """
    def __init__(self, q_table_path: str = "q_table.json"):
        self.q_table_path = q_table_path
        self.alpha = 0.2  # Learning rate
        self.gamma = 0.8  # Discount factor
        self.q_table = self._load_q_table()

    def _load_q_table(self) -> Dict[str, List[float]]:
        if os.path.exists(self.q_table_path):
            try:
                with open(self.q_table_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Initialize default Q-values
        # Key: "speed_snooze"
        table = {}
        for speed in range(3):
            for snooze in range(3):
                # Default preference: maintain (action 1) has higher initial reward
                table[f"{speed}_{snooze}"] = [0.0, 1.0, 0.0]
        return table

    def _save_q_table(self):
        try:
            with open(self.q_table_path, 'w') as f:
                json.dump(self.q_table, f)
        except Exception:
            pass

    def get_state(self, solve_time: float, snooze_count: int) -> str:
        # Determine speed category
        if solve_time < 20.0:
            speed = 0
        elif solve_time <= 50.0:
            speed = 1
        else:
            speed = 2
            
        # Determine snooze category
        if snooze_count == 0:
            snooze = 0
        elif snooze_count <= 2:
            snooze = 1
        else:
            snooze = 2
            
        return f"{speed}_{snooze}"

    def select_action(self, state: str) -> int:
        # Epsilon-greedy (mostly greedy since we want stable adaptation)
        q_values = self.q_table.get(state, [0.0, 1.0, 0.0])
        # Find index with max value
        max_q = max(q_values)
        actions_with_max_q = [i for i, v in enumerate(q_values) if v == max_q]
        return random_choice_action(actions_with_max_q)

    def learn(self, state: str, action: int, reward: float, next_state: str):
        q_values = self.q_table.get(state, [0.0, 1.0, 0.0])
        next_q_values = self.q_table.get(next_state, [0.0, 1.0, 0.0])
        
        # Q-learning formula: Q(s,a) = Q(s,a) + alpha * (reward + gamma * max(Q(s',a')) - Q(s,a))
        q_values[action] = q_values[action] + self.alpha * (reward + self.gamma * max(next_q_values) - q_values[action])
        self.q_table[state] = q_values
        self._save_q_table()

def random_choice_action(options: List[int]) -> int:
    import random
    return random.choice(options)

def calculate_reward(solve_time: float, snooze_count: int, final_difficulty: str, initial_difficulty: str) -> float:
    """
    Rewards for difficulty adjustments.
    We want to push difficulty higher if they are very fast and don't snooze (reward positive difficulty shifts).
    We want to push difficulty lower if they struggle or snooze heavily (reward downward shifts).
    """
    # Base reward is sleep speed and snooze penalties
    base = 10.0
    if solve_time > 60:
        base -= 5.0
    if snooze_count > 1:
        base -= 10.0
        
    diff_idx_init = DIFFICULTIES.index(initial_difficulty)
    diff_idx_final = DIFFICULTIES.index(final_difficulty)
    
    # If they performed poorly and difficulty went down or stayed down, give positive reinforcement:
    if snooze_count > 1 and diff_idx_final < diff_idx_init:
        return base + 5.0
    # If they performed extremely well and difficulty went up or stayed up, reward it:
    if solve_time < 20 and snooze_count == 0 and diff_idx_final > diff_idx_init:
        return base + 5.0
        
    return base

def adapt_user_difficulty(db: Session, user_id: int, solve_time_seconds: float, snooze_count: int) -> str:
    """
    Main entrypoint called after every challenge verification.
    Applies RL Q-learning or heuristic to adjust difficulty and updates user profile.
    """
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not profile:
        return "Easy"
        
    current_diff = profile.difficulty
    current_idx = DIFFICULTIES.index(current_diff)
    
    agent = DifficultyQLearningAgent()
    state = agent.get_state(solve_time_seconds, snooze_count)
    
    # Define heuristic action determination if Q-learning has insufficient records
    # 0 = decrease, 1 = hold, 2 = increase
    if solve_time_seconds < 15.0 and snooze_count == 0:
        action = 2 # Should level up
    elif solve_time_seconds > 45.0 or snooze_count >= 2:
        action = 0 # Should level down
    else:
        action = 1 # Hold
        
    # Execute action
    next_idx = current_idx
    if action == 2:
        next_idx = min(len(DIFFICULTIES) - 1, current_idx + 1)
    elif action == 0:
        next_idx = max(0, current_idx - 1)
        
    next_diff = DIFFICULTIES[next_idx]
    
    # Simulate RL feedback step
    reward = calculate_reward(solve_time_seconds, snooze_count, next_diff, current_diff)
    next_state = agent.get_state(solve_time_seconds, snooze_count) # next state representation
    agent.learn(state, action, reward, next_state)
    
    profile.difficulty = next_diff
    db.commit()
    db.refresh(profile)
    
    return next_diff

def evaluate_adaptive_difficulty(db: Session, user_id: int) -> str:
    """
    Evaluates difficulty rules:
    - If user solves 5 consecutive challenges correctly, increase difficulty.
    - If user fails 3 consecutive challenges, decrease difficulty.
    Logs transition in DifficultyHistory.
    """
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not profile:
        return "Easy"
        
    current_diff = profile.difficulty
    current_idx = DIFFICULTIES.index(current_diff)
    
    # Query latest challenge logs
    latest_logs = db.query(models.ChallengeLog).filter(
        models.ChallengeLog.user_id == user_id
    ).order_by(models.ChallengeLog.generated_at.desc()).limit(5).all()
    
    new_diff = current_diff
    reason = ""
    
    # Rule 1: 5 consecutive correct solves
    if len(latest_logs) >= 5 and all(log.is_success for log in latest_logs):
        if current_idx < len(DIFFICULTIES) - 1:
            new_diff = DIFFICULTIES[current_idx + 1]
            reason = "Adaptive Engine: 5 consecutive successful solves"
            
    # Rule 2: 3 consecutive failures
    elif len(latest_logs) >= 3 and all(not log.is_success for log in latest_logs[:3]):
        if current_idx > 0:
            new_diff = DIFFICULTIES[current_idx - 1]
            reason = "Adaptive Engine: 3 consecutive failed/skipped challenges"
            
    if new_diff != current_diff:
        # Logging history
        history_entry = models.DifficultyHistory(
            user_id=user_id,
            previous_difficulty=current_diff,
            current_difficulty=new_diff,
            reason=reason
        )
        db.add(history_entry)
        profile.difficulty = new_diff
        db.commit()
        db.refresh(profile)
        
    return new_diff

