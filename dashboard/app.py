from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from tradingagents.graph.trading_graph import TradingAgentsGraph

app = Flask(__name__)

ta_graph = TradingAgentsGraph(debug=False)

def analyze_symbol(symbol: str, trade_date: str):
    """Run TradingAgents on a single ticker and return relevant info."""
    _, decision = ta_graph.propagate(symbol, trade_date)
    final_state = ta_graph.curr_state
    risk_judge = final_state["risk_debate_state"]["judge_decision"]
    investment_plan = final_state["investment_plan"]
    return {
        "symbol": symbol,
        "decision": decision,
        "risk_judge": risk_judge,
        "plan": investment_plan,
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return redirect(url_for('index'))
    df = pd.read_csv(file)
    symbols = df.iloc[:,0].astype(str).tolist()
    results = []
    for sym in symbols:
        results.append(analyze_symbol(sym, '2024-05-10'))
    return render_template('results.html', results=results)

@app.route('/api/analyze')
def api_analyze():
    symbol = request.args.get('symbol')
    date = request.args.get('date', '2024-05-10')
    if not symbol:
        return jsonify({'error': 'symbol is required'}), 400
    result = analyze_symbol(symbol, date)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
