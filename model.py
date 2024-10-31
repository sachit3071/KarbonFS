from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, iscr, borrowing_to_revenue_flag
import json
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    lastest_financial_index_value = latest_financial_index(data)

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, lastest_financial_index_value
    )

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, lastest_financial_index_value
    )

    iscr_flag_value = iscr_flag(data, lastest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }

@app.route("/", methods = ["GET"])
def input_file():
    return render_template("index.html")



@app.route(f"/admin/{rno}", methods = ["GET"])
def get_admin():
    try:
        return render_template("admin.html", rno=rno)
    except Exception as e:
        return jsonify({"error": str(e)}, status_code=500)

@app.route("/", methods = ["POST"])
def output_result():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}, status_code=400)
    file = request.files["file"]
    content = file.read()
    data = json.loads(content)
    result = probe_model_5l_profit(data["data"])
    return render_template("results.html", result=result)

if __name__ == "__main__":
    data = json.loads("t.json")
    print(data)
    with open("./data.json", "r") as file:
        content = file.read()
        # convert to json
        data = json.loads(content)
        print(data["data"])
        print(probe_model_5l_profit(data["data"]))
        print(data["data"].get("financials")[0].get("bs").get("liabilities").get("long_term_borrowings"))