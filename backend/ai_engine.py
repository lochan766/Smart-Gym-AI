import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_plan(data):
    prompt = f"""
    Create a full gym plan.

    Weight: {data['weight']}
    Height: {data['height']}
    Goal: {data['goal']}

    Include workout + diet + tips.
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"result": res.choices[0].message.content}
    except Exception as e:
        print(e)
        return {"result": "Basic plan: Pushups + Eggs + Rice"}


def generate_workout(goal, level):
    prompt = f"Workout plan for {goal}, level {level}"

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print(e)
        return "Pushups, Squats, Cardio"


def generate_diet(weight, goal):
    prompt = f"Diet plan for {weight}kg person with goal {goal}"

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print(e)
        return f"{int(weight)*2}g protein, eggs, rice"