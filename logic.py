import math

class LogisticsSystem:
    def __init__(self):
        self.truck_capacity = 20 
        self.delivery_days = 2  
        self.warehouse_capacity = 1000

        self.total_drivers = 10  
        
        self.total_delivered = 12

        self.warehouses = {
            1: {"points": ["1", "2", "3"], "stack": 1000},
            2: {"points": ["4", "5"], "stack": 1000},
            3: {"points": ["6", "7", "8"], "stack": 1000}    
        }

        self.points = {
            i: {"regular_amount": 0, "urgent_amount": 0} for i in range(1, 9)
        }

        self.active_drivers = []
        self.active_deliveries = []

    def get_warehouse_id(self, point_id):
        for w_id, data in self.warehouses.items():
            if point_id in data["points"]:
                return w_id
        return 1
    
    def update_demand(self, point_id, regular=None, urgent=None):

        if regular is not None:
            self.points[point_id]["regular_amount"] = regular
        if urgent is not None:
            self.points[point_id]["urgent_amount"] = urgent
            
        self.rebalance_routes()

    def rebalance_routes(self):

        self.active_drivers = []
        available_drivers = self.total_drivers
        driver_id_counter = 101

        for w in self.warehouses.values():
            w["stock"] = self.warehouse_capacity

        queue = []
        
        for p_id, demands in self.points.items():
            w_id = self.get_warehouse_id(p_id)

            if demands["urgent_amount"] > 0:
                trips = math.ceil(demands["urgent_amount"] / self.truck_capacity)
                for _ in range(trips):
                    queue.append({"priority": 1, "point": p_id, "warehouse": w_id, "type": "Критично"})
                    
            if demands["regular_amount"] > 0:
                trips = math.ceil(demands["regular_amount"] / self.truck_capacity)
                for _ in range(trips):
                    queue.append({"priority": 2, "point": p_id, "warehouse": w_id, "type": "Регулярно"})

        queue.sort(key=lambda x: x["priority"])

        for trip in queue:
            if available_drivers <= 0:
                break 
                
            self.warehouses[trip["warehouse"]]["stock"] -= self.truck_capacity
            
            status = "В дорозі (Критично)" if trip["type"] == "Критично" else "В дорозі"
            self.active_drivers.append({
                "id": driver_id_counter,
                "from": f"Склад {trip['warehouse']}",
                "to": f"Точка {trip['point']}",
                "status": status
            })
            
            driver_id_counter += 1
            available_drivers -= 1

        self.active_deliveries = []
        for w_id, data in self.warehouses.items():
            if data["stock"] < (self.warehouse_capacity * 0.3) and available_drivers > 0:
                self.active_deliveries.append({
                    "warehouse_id": w_id, 
                    "drivers": 1, 
                    "amount": self.truck_capacity
                })
                self.active_drivers.append({
                    "id": driver_id_counter,
                    "from": "Постачальник",
                    "to": f"Склад {w_id}",
                    "status": "Завантаження"
                })
                driver_id_counter += 1
                available_drivers -= 1