import json  # استيراد مكتبة json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .models import Product, Cart, CartItem, Order, OrderItem

def products(request):
    products = Product.objects.all()
    return render(request, 'pages/products.html', {'products': products})

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'pages/product.html', {'product': product})

def contact_us (request):
    return render(request, 'pages/contactus.html')

def filter_products(request):
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    products = Product.objects.filter(active=True)
    if min_price.isnumeric() and max_price.isnumeric():
        products = products.filter(price__range=(float(min_price), float(max_price)))
    return render(request, 'pages/products.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل.')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'تم إنشاء الحساب بنجاح!')
        return redirect('products')

    return render(request, 'pages/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح!')
            return redirect('products')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
            return redirect('login')

    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح!')
    return redirect('products')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')

        product = get_object_or_404(Product, id=product_id)

        if not size:
            return JsonResponse({'success': False, 'message': 'برجاء اختيار المقاس.'})

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        cart_count = cart.items.aggregate(total=models.Sum('quantity'))['total'] or 0

        return JsonResponse({
            'success': True,
            'message': f'تم إضافة {product.name} إلى السلة!',
            'cart_count': cart_count
        })

    return JsonResponse({'success': False, 'message': 'طلب غير صالح.'})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'pages/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.error(request, 'السلة فارغة. لا يمكن إتمام الشراء.')
        return redirect('view_cart')

    total_price = sum(item.get_total_price() for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        status='Pending'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            size=item.size,
            price=item.product.price
        )

    # تحضير بيانات الطلب للإرسال بالإيميل
    items_text = "\n".join([
        f"- {item.product.name} (المقاس: {item.size}) - الكمية: {item.quantity} - السعر: {float(item.price)} جنيه"
        for item in order.items.all()
    ])
    order_data = {
        'order_id': order.id,
        'order_date': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'order_status': order.status,
        'order_total': float(order.total_price),  # تحويل Decimal إلى float
        'order_items': items_text,
        'user_name': request.user.username,
        'user_email': request.user.email,
    }

    # تحويل order_data إلى JSON string
    order_data_json = json.dumps(order_data)

    # تفريغ السلة بعد إتمام الشراء
    cart.items.all().delete()

    # توجيه المستخدم لصفحة التأكيد مع بيانات الطلب
    return render(request, 'pages/order_confirmation.html', {
        'order': order,
        'order_data_json': order_data_json  # نمرر order_data كـ JSON string
    })

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pages/orders.html', {'orders': orders})


from django.core.files.storage import FileSystemStorage
import json

@login_required
def custom_order(request):
    return render(request, 'pages/custom_order.html')

@login_required
def submit_custom_order(request):
    if request.method == 'POST':
        # استخراج البيانات من الفورم
        right_length = request.POST.get('right_length')
        right_width = request.POST.get('right_width')
        right_circumference = request.POST.get('right_circumference')
        left_length = request.POST.get('left_length')
        left_width = request.POST.get('left_width')
        left_circumference = request.POST.get('left_circumference')
        shoe_type = request.POST.get('shoe_type')
        notes = request.POST.get('notes')

        # تحضير بيانات الطلب للإيميل
        custom_order_data = {
            'user_name': request.user.username,
            'user_email': request.user.email,
            'right_length': right_length,
            'right_width': right_width,
            'right_circumference': right_circumference,
            'left_length': left_length,
            'left_width': left_width,
            'left_circumference': left_circumference,
            'shoe_type': shoe_type,
            'notes': notes,
        }

        # التعامل مع الصور المرفوعة (اختياري)
        images = request.FILES.getlist('foot_images')
        image_urls = []
        if images:
            fs = FileSystemStorage()
            for image in images:
                filename = fs.save(f'custom_orders/{image.name}', image)
                image_urls.append(fs.url(filename))

        # تحويل البيانات لـ JSON string للإيميل
        custom_order_data['image_urls'] = image_urls
        custom_order_data_json = json.dumps(custom_order_data)

        # إرسال الإيميل لصاحب المحل (نفس الطريقة اللي استخدمناها قبل كده)
        return render(request, 'pages/custom_order_confirmation.html', {
            'custom_order_data_json': custom_order_data_json
        })

    return redirect('custom_order')










import requests
from django.shortcuts import render

def customer_service(request):
    response = None
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            try:
                # افتراضي: استدعاء API بتاع Grok (ده مثال افتراضي لأن Grok ما عندوش API حقيقي)
                api_url = "https://api.xai.com/grok/answer"  # رابط افتراضي
                api_key = "your-api-key"  # مفتاح API افتراضي
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "question": question,
                    "language": "ar"  # لأننا عايزين الرد بالعربي
                }
                api_response = requests.post(api_url, json=data, headers=headers)
                api_response.raise_for_status()  # لو فيه خطأ في الطلب، هيطلع Exception
                response_data = api_response.json()
                response = response_data.get('answer', 'عذرًا، ما قدرتش أرد على سؤالك دلوقتي.')
            except requests.exceptions.RequestException as e:
                response = f"فيه مشكلة في الاتصال بالـ API: {str(e)}"

    return render(request, 'pages/customer_service.html', {'response': response})




def customer_service(request):
    response = None
    if request.method == 'POST':
        question = request.POST.get('question', '').lower().strip()
        
        if question:
            # قسم الأسعار والخصومات
            if any(word in question for word in ["سعر", "السعر", "بكام", "الأسعار", "غالي", "رخيص"]):
                response = """
                أسعار منتجاتنا تتراوح بين:
                - الجزم الرياضية: من 250 جنيه
                - الجزم الجلد الطبيعي: من 400 جنيه
                - الجزم الشتوية: من 350 جنيه
                
                العروض الحالية:
                🎉 خصم 20% على الطلبات فوق 1000 جنيه
                🔥 عرض 1+1 مجاناً على تشكيلة الصيف
                
                يمكنك رؤية جميع المنتجات والأسعار في products
                """
            
            # قسم الطلبات والتوصيل
            elif any(word in question for word in ["طلب", "اطلب", "شراء", "اشتري", "التوصيل", "الشحن"]):
                response = """
                خطوات الطلب:
                1. اختر المنتجات من products
                2. أضفها لعربة التسوق
                3. اكمل عملية الدفع
                4. استلم طلبك خلال 2-3 أيام
                
                خيارات الدفع:
                💳 بطاقات ائتمانية
                📱 محافظ رقمية (فودافون كاش - أورانج موني)
                💰 الدفع عند الاستلام
                
                للطلبات المخصصة: <a href="/custom-orders" class="text-blue-500">اضغط هنا</a>
                """
            
            # قسم المقاسات
            elif any(word in question for word in ["مقاس", "المقاس", "مقاسات", "حجم"]):
                response = """
                المقاسات المتوفرة:
                - رجالي: من 39 إلى 45
                - نسائي: من 35 إلى 40
                - أطفال: من 28 إلى 34
                
                إذا كنت غير متأكد من مقاسك:
                📏 استخدم <a href="/size-guide" class="text-blue-500">دليل المقاسات</a>
                🔄 يمكنك استبدال المقاس خلال 7 أيام
                """
            
            # قسم الإرجاع والضمان
            elif any(word in question for word in ["إرجاع", "استبدال", "ضمان", "عيب"]):
                response = """
                سياسة الإرجاع والضمان:
                - يمكنك إرجاع المنتج خلال 14 يوم
                - استبدال المقاس خلال 7 أيام
                - ضمان سنة ضد عيوب الصناعة
                
                شروط الإرجاع:
                ✓ المحافظة على الفاتورة الأصلية
                ✓ المنتج بحالته الأصلية
                ✓ عدم استخدام المنتج
                
                
                """
            
            # قسم العناية بالمنتجات
            elif any(word in question for word in ["نظافة", "تنظيف", "العناية", "حفاظ"]):
                response = """
                نصائح العناية بالجزم:
                1. نظف الجلد بفرشاة ناعمة أسبوعياً
                2. استخدم معطر الأحذية الخاص
                3. احفظها في مكان جاف
                4. استخدم كريم الجلد شهرياً
                
                لدينا خدمة تنظيف احترافية بـ 50 جنيه فقط!
                """

            elif any(word in question for word in ["معاق", "اعاقه", "خاص", "خاصه" ,"معوق"]):
                response = """
                لدينا خدمة تفصيل احذيه مقاسات خاصه او اشكال خاصه برجاء التوجه ل Order Custom Shoes و اتباع الخطوات!
                """
            
            # قسم الفروع ومواعيد العمل
            elif any(word in question for word in ["فرع", "فروع", "عنوان", "مواعيد", "يفتح"]):
                response = """
                فروعنا:
                🏬 القاهرة: مدينة نصر - شارع مصطفى النحاس
                🏬 الجيزة: الدقي - شارع جامعة القاهرة
                🏬 الإسكندرية: سموحة - شارع 45
                🏬 دمنهور: العباره - امام بن النشار 
                
                مواعيد العمل:
                ⏰ من السبت إلى الخميس
                🕘 من 10 صباحاً إلى 10 مساءً
                🕌 الجمعة من 1 ظهراً إلى 10 مساءً
                
                للتواصل: 📞 01203661364
                """
            
            # قسم المساعدة العامة
            else:
                response = """
                شكراً لتواصلك مع أشور شوز! 
                كيف يمكنني مساعدتك اليوم؟ يمكنك اختيار أحد المواضيع التالية:
                
                • الأسعار والعروض
                • كيفية الطلب
                • دليل المقاسات
                • سياسة الإرجاع
                • الفروع ومواعيد العمل
                
                أو اكتب سؤالك بشكل أكثر تفصيلاً وسأجيبك بأسرع وقت ممكن!
                او تواصل مع احد ممثلي خدمه العملاء من خلال contact us
                """

    return render(request, 'pages/customer_service.html', {'response': response})
