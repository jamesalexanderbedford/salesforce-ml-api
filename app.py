from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from Salesforce
        data = request.get_json()
        
        company = data.get('company', '')
        industry = data.get('industry', '')
        revenue = data.get('annual_revenue', 0)
        employees = data.get('employee_count', 0)
        lead_source = data.get('lead_source', '')
        
        # Simple scoring (replace with your ML model later)
        score = 0.5
        
        if revenue and revenue > 1000000:
            score += 0.2
        if employees and employees > 50:
            score += 0.15
        if industry in ['Technology', 'Healthcare', 'Finance']:
            score += 0.1
            
        # Determine likelihood
        if score >= 0.7:
            likelihood = 'High'
            action = 'Schedule demo call within 24 hours'
        elif score >= 0.5:
            likelihood = 'Medium'
            action = 'Send product information'
        else:
            likelihood = 'Low'
            action = 'Add to nurture campaign'
        
        return jsonify({
            'prediction_score': round(score, 2),
            'likelihood': likelihood,
            'recommended_action': action
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'ML API is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)