from django.http import JsonResponse
from django.views import View
from .models import Customer, Location
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
