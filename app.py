from flask import Flask, render_template, request, redirect
from logic import LogisticsSystem

app = Flask(__name__)
logistics = LogisticsSystem()

amount_per_delivery = 20
days_per_delivery = 2
max_amount_in_warehouse = 1000

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/point-log')
def point_log():
    return render_template('point-log.html')

@app.route('/login-point', methods=["POST"])
def point():
    raw_id = request.form.get('point_id')
    point_id = int(raw_id) if raw_id else 1 
    
    return render_template('point.html', 
                           ID=point_id, 
                           number=logistics.truck_capacity)

@app.route('/admin')
def admin():
    warehouses_data = []
    for w_id, data in logistics.warehouses.items():
        points_str = ", ".join([f"Точка {p}" for p in data["points"]])
        warehouses_data.append({
            "id": w_id, 
            "points": points_str, 
            "stock": data["stock"]
        })

    return render_template('manager.html', 
                           amount=logistics.truck_capacity, 
                           days=logistics.delivery_days, 
                           warehouse_capacity=logistics.warehouse_capacity,
                           warehouses=warehouses_data,
                           deliveries=logistics.active_deliveries, 
                           drivers=logistics.active_drivers)

@app.route('/set-term', methods=["POST"])
def set_term():
    raw_amount = request.form.get('term')
    raw_id = request.form.get('point_id')
    
    amount = int(raw_amount) if raw_amount else 0
    point_id = int(raw_id) if raw_id else 1
    
    logistics.update_demand(point_id, urgent=amount)
    return redirect('/point-log')

@app.route('/set-reg', methods=["POST"])
def set_reg():
    raw_amount = request.form.get('reg')
    raw_id = request.form.get('point_id')
    
    amount = int(raw_amount) if raw_amount else 0
    point_id = int(raw_id) if raw_id else 1
    
    logistics.update_demand(point_id, regular=amount)
    return redirect('/point-log')

if __name__ == '__main__':
    app.run(debug=True)