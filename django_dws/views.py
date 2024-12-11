from django.http import JsonResponse
from django.views import View
from .models import Customer, Location,OrderItem,Order,Product,Supply
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# Customer 视图
class CustomerView(View):
    # 列出所有 Customer（GET）
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                customer = Customer.objects.get(pk=pk)
                customer_data = {
                    "customer_id": customer.customer_id,
                    "customer_name": customer.customer_name,
                    "count_lifetime_orders": customer.count_lifetime_orders,
                    "first_ordered_at": customer.first_ordered_at,
                    "last_ordered_at": customer.last_ordered_at,
                    "lifetime_spend_pretax": customer.lifetime_spend_pretax,
                    "lifetime_tax_paid": customer.lifetime_tax_paid,
                    "lifetime_spend": customer.lifetime_spend,
                    "customer_type": customer.customer_type
                }
                return JsonResponse(customer_data, status=200)
            except Customer.DoesNotExist:
                return JsonResponse({"error": "Customer not found"}, status=404)

        else:
            customers = Customer.objects.all()
            customer_data = [
                {
                    "customer_id": customer.customer_id,
                    "customer_name": customer.customer_name,
                    "count_lifetime_orders": customer.count_lifetime_orders,
                    "first_ordered_at": customer.first_ordered_at,
                    "last_ordered_at": customer.last_ordered_at,
                    "lifetime_spend_pretax": customer.lifetime_spend_pretax,
                    "lifetime_tax_paid": customer.lifetime_tax_paid,
                    "lifetime_spend": customer.lifetime_spend,
                    "customer_type": customer.customer_type
                } for customer in customers
            ]
            return JsonResponse(customer_data, safe=False, status=200)

    # 创建 Customer（POST）
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            customer = Customer.objects.create(
                customer_id=data["customer_id"],
                customer_name=data["customer_name"],
                count_lifetime_orders=data["count_lifetime_orders"],
                first_ordered_at=data["first_ordered_at"],
                last_ordered_at=data["last_ordered_at"],
                lifetime_spend_pretax=data["lifetime_spend_pretax"],
                lifetime_tax_paid=data["lifetime_tax_paid"],
                lifetime_spend=data["lifetime_spend"],
                customer_type=data["customer_type"]
            )
            return JsonResponse({"message": "Customer created", "customer_id": customer.customer_id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

    # 修改 Customer（PUT）
    @method_decorator(csrf_exempt)
    def put(self, request, pk, *args, **kwargs):
        try:
            customer = Customer.objects.get(pk=pk)
            data = json.loads(request.body)

            customer.customer_name = data.get("customer_name", customer.customer_name)
            customer.count_lifetime_orders = data.get("count_lifetime_orders", customer.count_lifetime_orders)
            customer.first_ordered_at = data.get("first_ordered_at", customer.first_ordered_at)
            customer.last_ordered_at = data.get("last_ordered_at", customer.last_ordered_at)
            customer.lifetime_spend_pretax = data.get("lifetime_spend_pretax", customer.lifetime_spend_pretax)
            customer.lifetime_tax_paid = data.get("lifetime_tax_paid", customer.lifetime_tax_paid)
            customer.lifetime_spend = data.get("lifetime_spend", customer.lifetime_spend)
            customer.customer_type = data.get("customer_type", customer.customer_type)

            customer.save()
            return JsonResponse({"message": "Customer updated", "customer_id": customer.customer_id}, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=404)

    # 删除 Customer（DELETE）
    @method_decorator(csrf_exempt)
    def delete(self, request, pk, *args, **kwargs):
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()
            return JsonResponse({"message": "Customer deleted"}, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=404)


# Location 视图
class LocationView(View):
    # 列出所有 Location（GET）
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                location = Location.objects.get(pk=pk)
                location_data = {
                    "location_id": location.location_id,
                    "location_name": location.location_name,
                    "tax_rate": location.tax_rate,
                    "opened_date": location.opened_date
                }
                return JsonResponse(location_data, status=200)
            except Location.DoesNotExist:
                return JsonResponse({"error": "Location not found"}, status=404)

        else:
            locations = Location.objects.all()
            location_data = [
                {
                    "location_id": location.location_id,
                    "location_name": location.location_name,
                    "tax_rate": location.tax_rate,
                    "opened_date": location.opened_date
                } for location in locations
            ]
            return JsonResponse(location_data, safe=False, status=200)

    # 创建 Location（POST）
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            location = Location.objects.create(
                location_id=data["location_id"],
                location_name=data["location_name"],
                tax_rate=data["tax_rate"],
                opened_date=data["opened_date"]
            )
            return JsonResponse({"message": "Location created", "location_id": location.location_id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

    # 修改 Location（PUT）
    @method_decorator(csrf_exempt)
    def put(self, request, pk, *args, **kwargs):
        try:
            location = Location.objects.get(pk=pk)
            data = json.loads(request.body)

            location.location_name = data.get("location_name", location.location_name)
            location.tax_rate = data.get("tax_rate", location.tax_rate)
            location.opened_date = data.get("opened_date", location.opened_date)

            location.save()
            return JsonResponse({"message": "Location updated", "location_id": location.location_id}, status=200)
        except Location.DoesNotExist:
            return JsonResponse({"error": "Location not found"}, status=404)

    # 删除 Location（DELETE）
    @method_decorator(csrf_exempt)
    def delete(self, request, pk, *args, **kwargs):
        try:
            location = Location.objects.get(pk=pk)
            location.delete()
            return JsonResponse({"message": "Location deleted"}, status=200)
        except Location.DoesNotExist:
            return JsonResponse({"error": "Location not found"}, status=404)

class OrderView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                order = Order.objects.get(pk=pk)
                order_data = {
                    "order_id": order.order_id,
                    "location_id": order.location_id,
                    "customer_id": order.customer_id,
                    "subtotal": order.subtotal,
                    "tax_paid": order.tax_paid,
                    "order_total": order.order_total,
                    "ordered_at": order.ordered_at,
                }
                return JsonResponse(order_data, status=200)
            except Order.DoesNotExist:
                return JsonResponse({"error": "Order not found"}, status=404)
        else:
            orders = Order.objects.all()
            order_data = [
                {
                    "order_id": order.order_id,
                    "location_id": order.location_id,
                    "customer_id": order.customer_id,
                    "subtotal": order.subtotal,
                    "tax_paid": order.tax_paid,
                    "order_total": order.order_total,
                    "ordered_at": order.ordered_at,
                } for order in orders
            ]
            return JsonResponse(order_data, safe=False, status=200)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order = Order.objects.create(
                order_id=data["order_id"],
                location_id=data["location_id"],
                customer_id=data["customer_id"],
                subtotal=data["subtotal"],
                tax_paid=data["tax_paid"],
                order_total=data["order_total"],
                ordered_at=data["ordered_at"],
            )
            return JsonResponse({"message": "Order created", "order_id": order.order_id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

    @method_decorator(csrf_exempt)
    def put(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
            data = json.loads(request.body)

            order.location_id = data.get("location_id", order.location_id)
            order.customer_id = data.get("customer_id", order.customer_id)
            order.subtotal = data.get("subtotal", order.subtotal)
            order.tax_paid = data.get("tax_paid", order.tax_paid)
            order.order_total = data.get("order_total", order.order_total)
            order.ordered_at = data.get("ordered_at", order.ordered_at)

            order.save()
            return JsonResponse({"message": "Order updated", "order_id": order.order_id}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)

    @method_decorator(csrf_exempt)
    def delete(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return JsonResponse({"message": "Order deleted"}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)


class OrderItemView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                order_item = OrderItem.objects.get(pk=pk)
                order_item_data = {
                    "order_item_id": order_item.order_item_id,
                    "order_id": order_item.order_id,
                    "product_id": order_item.product_id,
                    "ordered_at": order_item.ordered_at,
                    "product_name": order_item.product_name,
                    "product_price": order_item.product_price,
                    "is_food_item": order_item.is_food_item,
                    "is_drink_item": order_item.is_drink_item,
                    "supply_cost": order_item.supply_cost,
                }
                return JsonResponse(order_item_data, status=200)
            except OrderItem.DoesNotExist:
                return JsonResponse({"error": "Order item not found"}, status=404)
        else:
            order_items = OrderItem.objects.all()
            order_item_data = [
                {
                    "order_item_id": item.order_item_id,
                    "order_id": item.order_id,
                    "product_id": item.product_id,
                    "ordered_at": item.ordered_at,
                    "product_name": item.product_name,
                    "product_price": item.product_price,
                    "is_food_item": item.is_food_item,
                    "is_drink_item": item.is_drink_item,
                    "supply_cost": item.supply_cost,
                } for item in order_items
            ]
            return JsonResponse(order_item_data, safe=False, status=200)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order_item = OrderItem.objects.create(
                order_item_id=data["order_item_id"],
                order_id=data["order_id"],
                product_id=data["product_id"],
                ordered_at=data["ordered_at"],
                product_name=data["product_name"],
                product_price=data["product_price"],
                is_food_item=data["is_food_item"],
                is_drink_item=data["is_drink_item"],
                supply_cost=data["supply_cost"],
            )
            return JsonResponse({"message": "Order item created", "order_item_id": order_item.order_item_id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

    @method_decorator(csrf_exempt)
    def put(self, request, pk, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(pk=pk)
            data = json.loads(request.body)

            order_item.order_id = data.get("order_id", order_item.order_id)
            order_item.product_id = data.get("product_id", order_item.product_id)
            order_item.ordered_at = data.get("ordered_at", order_item.ordered_at)
            order_item.product_name = data.get("product_name", order_item.product_name)
            order_item.product_price = data.get("product_price", order_item.product_price)
            order_item.is_food_item = data.get("is_food_item", order_item.is_food_item)
            order_item.is_drink_item = data.get("is_drink_item", order_item.is_drink_item)
            order_item.supply_cost = data.get("supply_cost", order_item.supply_cost)

            order_item.save()
            return JsonResponse({"message": "Order item updated", "order_item_id": order_item.order_item_id}, status=200)
        except OrderItem.DoesNotExist:
            return JsonResponse({"error": "Order item not found"}, status=404)

    @method_decorator(csrf_exempt)
    def delete(self, request, pk, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(pk=pk)
            order_item.delete()
            return JsonResponse({"message": "Order item deleted"}, status=200)
        except OrderItem.DoesNotExist:
            return JsonResponse({"error": "Order item not found"}, status=404)


class ProductView(View):
    # List all products (GET)
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                product = Product.objects.get(pk=pk)
                product_data = {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_type": product.product_type,
                    "product_description": product.product_description,
                    "product_price": str(product.product_price),
                    "is_food_item": product.is_food_item,
                    "is_drink_item": product.is_drink_item
                }
                return JsonResponse(product_data, status=200)
            except Product.DoesNotExist:
                return JsonResponse({"error": "Product not found"}, status=404)

        else:
            products = Product.objects.all()
            product_data = [
                {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_type": product.product_type,
                    "product_description": product.product_description,
                    "product_price": str(product.product_price),
                    "is_food_item": product.is_food_item,
                    "is_drink_item": product.is_drink_item
                } for product in products
            ]
            return JsonResponse(product_data, safe=False, status=200)

    # Create a product (POST)
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                product_id=data["product_id"],
                product_name=data["product_name"],
                product_type=data["product_type"],
                product_description=data["product_description"],
                product_price=data["product_price"],
                is_food_item=data["is_food_item"],
                is_drink_item=data["is_drink_item"]
            )
            return JsonResponse({"message": "Product created", "product_id": product.product_id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

    # Update a product (PUT)
    @method_decorator(csrf_exempt)
    def put(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
            data = json.loads(request.body)

            product.product_name = data.get("product_name", product.product_name)
            product.product_type = data.get("product_type", product.product_type)
            product.product_description = data.get("product_description", product.product_description)
            product.product_price = data.get("product_price", product.product_price)
            product.is_food_item = data.get("is_food_item", product.is_food_item)
            product.is_drink_item = data.get("is_drink_item", product.is_drink_item)

            product.save()
            return JsonResponse({"message": "Product updated", "product_id": product.product_id}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    # Delete a product (DELETE)
    @method_decorator(csrf_exempt)
    def delete(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return JsonResponse({"message": "Product deleted"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

class SupplyView(View):
    # List all supplies (GET)
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                supply = Supply.objects.get(pk=pk)
                supply_data = {
                    "supply_uuid": supply.supply_uuid,
                    "supply_id": supply.supply_id,
                    "product_id": supply.product_id,
                    "supply_name": supply.supply_name,
                    "supply_cost": str(supply.supply_cost),
                    "is_perishable_supply": supply.is_perishable_supply
                }
                return JsonResponse(supply_data, status=200)
            except Supply.DoesNotExist:
                return JsonResponse({"error": "Supply not found"}, status=404)

        else:
            supplies = Supply.objects.all()
            supply_data = [
                {
                    "supply_uuid": supply.supply_uuid,
                    "supply_id": supply.supply_id,
                    "product_id": supply.product_id,
                    "supply_name": supply.supply_name,
                    "supply_cost": str(supply.supply_cost),
                    "is_perishable_supply": supply.is_perishable_supply
                } for supply in supplies
            ]
            return JsonResponse(supply_data, safe=False, status=200)

    # Create a supply (POST)
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            supply = Supply.objects.create(
                supply_uuid=data["supply_uuid"],
                supply_id=data["supply_id"],
                product_id=data["product_id"],
                supply_name=data["supply_name"],
                supply_cost=data["supply_cost"],
                is_perishable_supply=data["is_perishable_supply"]
            )
            return JsonResponse({"message": "Supply created", "supply_uuid": supply.supply_uuid}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    # Update a supply (PUT)
    @method_decorator(csrf_exempt)
    def put(self, request, pk, *args, **kwargs):
        try:
            supply = Supply.objects.get(pk=pk)
            data = json.loads(request.body)

            supply.product = data.get("product_id", supply.product_id)
            supply.supply_name = data.get("supply_name", supply.supply_name)
            supply.supply_cost = data.get("supply_cost", supply.supply_cost)
            supply.is_perishable_supply = data.get("is_perishable_supply", supply.is_perishable_supply)

            supply.save()
            return JsonResponse({"message": "Supply updated", "supply_uuid": supply.supply_uuid}, status=200)
        except Supply.DoesNotExist:
            return JsonResponse({"error": "Supply not found"}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    # Delete a supply (DELETE)
    @method_decorator(csrf_exempt)
    def delete(self, request, pk, *args, **kwargs):
        try:
            supply = Supply.objects.get(pk=pk)
            supply.delete()
            return JsonResponse({"message": "Supply deleted"}, status=200)
        except Supply.DoesNotExist:
            return JsonResponse({"error": "Supply not found"}, status=404)
