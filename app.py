from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

INGREDIENT_KNOWLEDGE = {
    "palm oil": {
        "why": "Used for texture and shelf stability",
        "tradeoff": "Cheap and stable but linked to higher saturated fat intake",
        "uncertainty": "Health impact depends on quantity and overall diet"
    },
    "refined sugar": {
        "why": "Improves taste and quick energy",
        "tradeoff": "High glycemic load with low nutritional value",
        "uncertainty": "Occasional use differs from habitual intake"
    },
    "sodium benzoate": {
        "why": "Prevents microbial spoilage",
        "tradeoff": "Can form benzene under specific conditions",
        "uncertainty": "Risk depends on storage and formulation"
    },
    "soy lecithin": {
        "why": "Improves texture and emulsification",
        "tradeoff": "May concern people with soy sensitivity",
        "uncertainty": "Most evidence shows low allergenic risk"
    },
    "citric acid": {
        "why": "Enhances flavor and preservation",
        "tradeoff": "Can irritate sensitive stomachs",
        "uncertainty": "Generally safe at low concentrations"
    },
    "artificial flavor": {
        "why": "Creates consistent taste",
        "tradeoff": "Lack of transparency on composition",
        "uncertainty": "Safety depends on specific compounds used"
    },
    "monosodium glutamate": {
        "why": "Enhances umami flavor",
        "tradeoff": "Perceived sensitivity in some individuals",
        "uncertainty": "Scientific evidence is mixed"
    },
    "high fructose corn syrup": {
        "why": "Cheap sweetener with long shelf life",
        "tradeoff": "Linked to metabolic concerns",
        "uncertainty": "Effects depend on overall diet context"
    },
    "hydrogenated oil": {
        "why": "Improves texture and shelf life",
        "tradeoff": "May contain trans fats",
        "uncertainty": "Regulations vary by region"
    },
    "natural flavor": {
        "why": "Enhances taste perception",
        "tradeoff": "Broad labeling hides specifics",
        "uncertainty": "Impact depends on source"
    }
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    user_text = messages[-1]["content"].lower()

    found = []
    for ingredient, info in INGREDIENT_KNOWLEDGE.items():
        if ingredient in user_text:
            found.append(
                f"• **{ingredient.title()}**\n"
                f"Why it matters: {info['why']}\n"
                f"Trade-off: {info['tradeoff']}\n"
                f"Uncertainty: {info['uncertainty']}"
            )

    if not found:
        reply = (
            "I couldn’t confidently map these ingredients to my current knowledge.\n\n"
            "This highlights an important uncertainty: labels often lack clarity, "
            "and impact depends heavily on formulation and quantity."
        )
    else:
        reply = "\n\n".join(found)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




