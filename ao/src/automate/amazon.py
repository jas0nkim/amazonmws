from automate.framework.amazon import Workflow


def ordering(paid_price, username, password, asin, **shipping_information):
    service_args = [
        # '--proxy=%s:%d' % (amazonmws_settings.TOR_CLIENT_IP, amazonmws_settings.TOR_CLIENT_PORT),
        # '--proxy-type=%s' % amazonmws_settings.TOR_CLIENT_PORT_TYPE,        
    ]

    Workflow.open_browser(phantomjs_service_args=service_args)
    Workflow.LoginPage.go_to()
    Workflow.LoginPage.login(username=username, password=password)
    Workflow.ItemPage.go_to(asin=asin)
    Workflow.ItemPage.add_to_cart()
    # already on shopping cart page
    Workflow.ShoppingCartPage.proceed_to_checkout()
    # already on checkout select address page
    Workflow.CheckoutNewAddressPage.go_to()
    Workflow.CheckoutNewAddressPage.add_new_address(**shipping_information)
    # already on checkout payment method page
    Workflow.CheckoutSelectPaymentMethodPage.select_gift_card()
    # already on checkout delivery option page
    Workflow.CheckoutSelectDeliveryOptionPage.select_free_two_day_shipping()
    # already on checkout summary page
    Workflow.CheckoutSummaryPage.review(paid_price=paid_price)
    Workflow.CheckoutSummaryPage.place_order()
    Workflow.close_browser()


def order_tracking(order_id):
    service_args = [
        # '--proxy=%s:%d' % (amazonmws_settings.TOR_CLIENT_IP, amazonmws_settings.TOR_CLIENT_PORT),
        # '--proxy-type=%s' % amazonmws_settings.TOR_CLIENT_PORT_TYPE,        
    ]

    Workflow.open_browser(phantomjs_service_args=service_args)
    Workflow.LoginPage.go_to()
    Workflow.LoginPage.login()
    Workflow.OrderHistoryPage.go_to(order_id=order_id)
    Workflow.OrderHistoryPage.click_track_package()
    # already on track package page
    Workflow.TrackPackagePage.get_tracking_number()


def check_order_delivered(order_id):
    service_args = [
        # '--proxy=%s:%d' % (amazonmws_settings.TOR_CLIENT_IP, amazonmws_settings.TOR_CLIENT_PORT),
        # '--proxy-type=%s' % amazonmws_settings.TOR_CLIENT_PORT_TYPE,        
    ]

    Workflow.open_browser(phantomjs_service_args=service_args)
    Workflow.LoginPage.go_to()
    Workflow.LoginPage.login()
    Workflow.OrderHistoryPage.go_to(order_id=order_id)
    Workflow.OrderHistoryPage.check_delivered()
