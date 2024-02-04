from shop.models import Order

class OrderMiddleware:
    """Middleware to get the order object from the last visited order-detail-view. Populates request.order"""
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        order_id = request.session.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order_obj = order
            except Order.DoesNotExist:
                order_obj = None
            request.order = order_obj
        return self.get_response(request)