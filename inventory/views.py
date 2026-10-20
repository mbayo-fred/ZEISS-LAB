from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import StockItem, Invoice, Supplier
from .forms import StockItemForm, InvoiceForm, SupplierForm, RestockForm

@login_required
def inventory_dashboard(request):
    stock_list = StockItem.objects.all()
    paginator = Paginator(stock_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    stock_form = StockItemForm()
    invoice_form = InvoiceForm()
    supplier_form = SupplierForm()
    restock_form = RestockForm()

    if request.method == 'POST':
        # 1. Add New Stock Item & Link Tests
        if 'add_stock' in request.POST:
            stock_form = StockItemForm(request.POST)
            if stock_form.is_valid():
                # Save the stock item first
                stock_item = stock_form.save()
                
                # Manually link the tests to the stock item
                selected_tests = stock_form.cleaned_data.get('required_stock')
                if selected_tests:
                    for test in selected_tests:
                        test.required_stock.add(stock_item)
                
                messages.success(request, "New item added and successfully linked to tests!")
                return redirect('inventory_dashboard')
            else:
                messages.error(request, "Error adding item. Please check the form.")
                
        # 2. Restock Existing Item
        elif 'restock_stock' in request.POST:
            restock_form = RestockForm(request.POST)
            if restock_form.is_valid():
                item = restock_form.cleaned_data['item']
                qty = restock_form.cleaned_data['quantity_added']
                price = restock_form.cleaned_data['unit_price']
                invoice = restock_form.cleaned_data['invoice']
                
                item.quantity_in_stock += qty
                item.unit_price = price
                if invoice:
                    item.invoice = invoice
                item.save()
                messages.success(request, f"Restocked {qty} units of {item.name}!")
                return redirect('inventory_dashboard')

        # 3. Edit Quantity
        elif 'edit_quantity' in request.POST:
            item_id = request.POST.get('item_id')
            new_qty = request.POST.get('new_quantity')
            item = get_object_or_404(StockItem, id=item_id)
            item.quantity_in_stock = new_qty
            item.save()
            messages.success(request, f"Updated quantity for {item.name}!")
            return redirect('inventory_dashboard')

        # 4. Delete Item
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(StockItem, id=item_id)
            item.delete()
            messages.success(request, "Item deleted successfully!")
            return redirect('inventory_dashboard')
                
        # 5. Add Invoice
        elif 'add_invoice' in request.POST:
            invoice_form = InvoiceForm(request.POST)
            if invoice_form.is_valid():
                invoice_form.save()
                return redirect('inventory_dashboard')
                
        # 6. Add Supplier
        elif 'add_supplier' in request.POST:
            supplier_form = SupplierForm(request.POST)
            if supplier_form.is_valid():
                supplier_form.save()
                return redirect('inventory_dashboard')

    context = {
        'page_obj': page_obj,
        'stock_form': stock_form,
        'invoice_form': invoice_form,
        'supplier_form': supplier_form,
        'restock_form': restock_form,
    }
    return render(request, 'inventory/dashboard.html', context)
